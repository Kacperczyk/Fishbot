------------------------------------------------------------------------------------------------------------------------------
----ZMIANA HASLA
--QUERY:
DO $$
DECLARE
    v_new_password TEXT := 'Test1.';
    v_salt TEXT;
    v_hash TEXT;
BEGIN
    v_salt := gen_salt('bf', 12);
    v_hash := crypt(v_new_password, v_salt);
    
    UPDATE users
    SET 
        password_salt = v_salt,
        password_hash = v_hash,
        last_password_change_date = CURRENT_TIMESTAMP
    WHERE 
        login = 'Test';
    
    RAISE NOTICE 'Nowe hasło dla użytkownika: %', v_new_password;
END $$;

----FUNCKJA
CREATE OR REPLACE FUNCTION change_user_password(
    p_user_login VARCHAR(50),
    p_new_password TEXT
) RETURNS TEXT AS $$
DECLARE
    v_user_exists BOOLEAN;
    v_salt TEXT;
    v_hash TEXT;
BEGIN
    -- Sprawdź, czy użytkownik istnieje
    SELECT EXISTS(SELECT 1 FROM users WHERE login = p_user_login) INTO v_user_exists;
    
    IF NOT v_user_exists THEN
        RAISE NOTICE 'Użytkownik "%", nie istnieje.', p_user_login;
        RETURN 'Użytkownik nie istnieje';
    END IF;
    
    -- Wygeneruj nową sól i hash dla hasła
    v_salt := gen_salt('bf', 12);
    v_hash := crypt(p_new_password, v_salt);
    
    -- Zaktualizuj hasło użytkownika
    UPDATE users
    SET 
        password_salt = v_salt,
        password_hash = v_hash,
        last_password_change_date = CURRENT_TIMESTAMP
    WHERE login = p_user_login;
    
    RAISE NOTICE 'Hasło dla użytkownika "%", zostało pomyślnie zmienione.', p_user_login;
    RETURN 'Hasło zostało pomyślnie zmienione';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;



--DROP
;DROP FUNCTION public.change_user_password;

--Przyklad uzycia
select change_user_password ('Test', 'Test1.');




