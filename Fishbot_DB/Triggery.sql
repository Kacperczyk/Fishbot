--SPRAWDZENIE WSZYSTKIE TRIGGERROW
SELECT trigger_name, 
       event_manipulation AS event,
       action_timing AS timing,
       action_statement AS function
FROM information_schema.triggers
WHERE event_object_table = 'users';

DROP TRIGGER IF EXISTS trg_user_insert_activation ON users;
DROP TRIGGER IF EXISTS trg_user_update_activation ON users;
DROP TRIGGER IF EXISTS trg_user_after_insert ON users;

--------------------------------------------------------------------------------------------


-- 1) FUNCKJA [update_expiration_on_activation]
--Rola: Dla INSERT (nowy użytkownik):
--		Jeśli is_active = true → ustawia expiration = now + 1 miesiąc
--		Nie dodaje jeszcze wpisu do historii (bo użytkownik jeszcze nie istnieje w bazie)
--		Dla UPDATE (zmiana statusu):
--		Jeśli is_active zmienia się na true → ustawia expiration i dodaje wpis do historii


CREATE OR REPLACE FUNCTION update_expiration_on_activation()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT' AND NEW.is_active = true) OR 
       (TG_OP = 'UPDATE' AND NEW.is_active = true AND 
       (OLD.is_active = false OR OLD.is_active IS DISTINCT FROM NEW.is_active)) THEN
        
        NEW.expiration := CURRENT_TIMESTAMP + INTERVAL '1 month';
        
        -- Dla INSERT tylko ustaw expiration, historia zostanie dodana przez AFTER INSERT
        IF TG_OP = 'INSERT' THEN
            RETURN NEW;
        END IF;
        
        -- Dla UPDATE dodaj wpis do historii
        INSERT INTO users_expiration_history (
            id_user,
            activation_date,
            expiration_date
        ) VALUES (
            NEW.id,
            CURRENT_TIMESTAMP,
            NEW.expiration
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--2) FUNKCJA [handle_new_user_activation()]
--	 Rola:	Uzupełnia brakujący wpis historyczny dla nowych użytkowników
--			Wywoływana po utworzeniu użytkownika (AFTER INSERT)
--			Jeśli konto jest aktywne (is_active = true) → dodaje wpis do historii

--			ALTERNATYWNIE MOZNA:
--			ALTER TABLE users_expiration_history
--			ALTER CONSTRAINT users_expiration_history_id_user_fkey DEFERRABLE INITIALLY DEFERRED;
--			To pozwoli na odroczenie sprawdzania klucza obcego do końca transakcji.
CREATE OR REPLACE FUNCTION handle_new_user_activation()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_active = true THEN
        INSERT INTO users_expiration_history (
            id_user,
            activation_date,
            expiration_date
        ) VALUES (
            NEW.id,
            CURRENT_TIMESTAMP,
            NEW.expiration
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--TRIGGERY
-- BEFORE INSERT/UPDATE
--1) TRIGGER [trg_user_insert_activation]
CREATE TRIGGER trg_user_insert_activation
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION update_expiration_on_activation();

--2) TRIGGER [trg_user_update_activation]
CREATE TRIGGER trg_user_update_activation
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_expiration_on_activation();

-- AFTER INSERT
--3) TRIGGER [trg_user_after_insert]
CREATE TRIGGER trg_user_after_insert
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION handle_new_user_activation();


--------------------------
--TO NA DOLE DO PRZEMYSLENIA
--3) Trigger sprawdzający ważność konta (uruchamiany okresowo lub przy próbie logowania logowaniu)

	