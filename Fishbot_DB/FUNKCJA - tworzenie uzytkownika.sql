--Tworzenie nowego uzytkownika:
--QUERY:
DO $$
DECLARE
    v_salt TEXT;
    v_hash TEXT;
    v_user_id INTEGER;
    v_password TEXT := 'MojeSilneHasło123!'; -- Zmień to na prawdziwe hasło
    v_creator_id INTEGER; -- ID istniejącego użytkownika który tworzy nowe konto
BEGIN
    -- Znajdź ID istniejącego użytkownika (np. admina)
    SELECT id INTO v_creator_id FROM users WHERE login = 'adm_kkacperczyk' LIMIT 1;
    
    IF v_creator_id IS NULL THEN
        RAISE EXCEPTION 'Nie znaleziono użytkownika tworzącego (np. admina)';
    END IF;

    -- Generowanie soli i hasha
    v_salt := gen_salt('bf', 12); -- Algorytm Blowfish, koszt 12
    v_hash := crypt(v_password, v_salt);
    
    -- Wstawianie nowego użytkownika
    INSERT INTO users (
        login,
        email,
        password_salt,
        password_hash,
        id_create_user,
        is_active,
        forename,
        surname,
        phone_number,
        description
    ) VALUES (
        'nowy_uzytkownik', -- Zmień login
        'nowy@example.com', -- Zmień email
        v_salt,
        v_hash,
        v_creator_id,
        TRUE, -- Czy konto aktywne
        'Jan', -- Imię
        'Kowalski', -- Nazwisko
        '+48123456789', -- Telefon
        'Nowe konto testowe' -- Opis
    ) RETURNING id INTO v_user_id;
    
    RAISE NOTICE 'Utworzono użytkownika ID: %, Login: %, Hasło: %', 
        v_user_id, 'nowy_uzytkownik', v_password;
END $$;

--FUNCKJA
CREATE OR REPLACE FUNCTION create_new_user(
    p_login VARCHAR(50),
    p_email VARCHAR(50),
    p_password TEXT,
    p_creator_login VARCHAR(50), -- Login użytkownika tworzącego nowego
    p_is_active BOOLEAN DEFAULT TRUE,
    p_expiration TIMESTAMP DEFAULT NULL, -- Data wygaśnięcia (opcjonalna)
    p_forename VARCHAR(50) DEFAULT NULL,
    p_surname VARCHAR(50) DEFAULT NULL,
    p_phone_number VARCHAR(20) DEFAULT NULL,
    p_description TEXT DEFAULT NULL
) RETURNS TEXT AS $$
DECLARE
    v_creator_id INTEGER;
    v_user_id INTEGER;
    v_salt TEXT;
    v_hash TEXT;
    v_current_timestamp TIMESTAMP := CURRENT_TIMESTAMP;
BEGIN
    -- Znajdź ID użytkownika tworzącego (np. admina)
    SELECT id INTO v_creator_id
    FROM users
    WHERE login = p_creator_login;

    IF v_creator_id IS NULL THEN
        RAISE NOTICE 'Nie znaleziono użytkownika tworzącego (np. admina) z loginem "%".', p_creator_login;
        RETURN 'Błąd: Brak użytkownika tworzącego';
    END IF;

    -- Walidacja loginu
    IF EXISTS (SELECT 1 FROM users WHERE login = p_login) THEN
        RAISE NOTICE 'Użytkownik z loginem "%" już istnieje.', p_login;
        RETURN 'Błąd: Login już istnieje';
    END IF;

    -- Walidacja emaila
    IF EXISTS (SELECT 1 FROM users WHERE email = p_email) THEN
        RAISE NOTICE 'Użytkownik z emailem "%" już istnieje.', p_email;
        RETURN 'Błąd: Email już istnieje';
    END IF;

    -- Generowanie soli i hasha
    v_salt := gen_salt('bf', 12);
    v_hash := crypt(p_password, v_salt);

    -- Tworzenie użytkownika
    INSERT INTO users (
        login,
        email,
        password_salt,
        password_hash,
        id_create_user,
        is_active,
        expiration,
        forename,
        surname,
        phone_number,
        description
    ) VALUES (
        p_login,
        p_email,
        v_salt,
        v_hash,
        v_creator_id,
        p_is_active,
        p_expiration, -- Może być NULL
        p_forename,
        p_surname,
        p_phone_number,
        p_description
    ) RETURNING id INTO v_user_id;

    -- Dodanie do historii, jeśli ustawiono wygaśnięcie
    IF p_expiration IS NOT NULL THEN
        INSERT INTO users_expiration_history (
            id_user,
            activation_date,
            expiration_date
        ) VALUES (
            v_user_id,
            v_current_timestamp,
            p_expiration
        );
        RAISE NOTICE 'Historia wygaśnięcia dla użytkownika ID=% została zapisana.', v_user_id;
    END IF;

    -- Powiadomienia o utworzeniu użytkownika
    RAISE NOTICE 'Utworzono użytkownika: ID=%, Login="%", Email="%"', v_user_id, p_login, p_email;

    -- Zwrócenie prostego komunikatu
    RETURN 'Użytkownik został pomyślnie utworzony';

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Błąd podczas tworzenia użytkownika: %', SQLERRM;
        RETURN 'Błąd podczas tworzenia użytkownika';
END;
$$ LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public;



--DROP
;DROP FUNCTION public.create_new_user;

--WYWOLANIE FUNKCJI
SELECT create_new_user(
    'nowy_login2',
    'nowy_email2@example.com',
    'MojeSilneHaslo123!12', -- HASLO
    'adm_kkacperczyk', -- Login użytkownika tworzącego nowego użytkownika
    TRUE, -- Konto aktywne
    NULL, -- Brak daty wygaśnięcia
    'Jan', -- Imię
    'Kowalski', -- Nazwisko
    '222222223', -- Telefon
    'Opis użytkownika' -- Opis
);


