--WERYFIKACJA HASLA

--QUERY
SELECT 
    id,
    login,
    (password_hash = crypt('xd', password_hash)) AS is_password_correct
FROM 
    users 
WHERE 
    login = 'adm_kkacperczyk';

--FUNCKJA
CREATE OR REPLACE FUNCTION verify_user_password(
    p_login VARCHAR(50),
    p_password TEXT
) RETURNS TABLE (
    user_id INTEGER,
    is_password_valid BOOLEAN,
    is_active BOOLEAN,
    message TEXT
) AS $$
BEGIN
    -- Sprawdź, czy użytkownik istnieje
    IF NOT EXISTS (SELECT 1 FROM users WHERE login = p_login) THEN
        RAISE NOTICE 'Użytkownik "%", nie istnieje.', p_login;
        RETURN QUERY 
        SELECT 
            NULL::INTEGER AS user_id, 
            FALSE AS is_password_valid, 
            FALSE AS is_active, 
            'Użytkownik nie istnieje' AS message;
        RETURN;
    END IF;

    -- Pobierz dane użytkownika i sprawdź hasło
    RETURN QUERY
    SELECT 
        u.id::INTEGER AS user_id,
        (u.password_hash = crypt(p_password, u.password_hash)) AS is_password_valid,
        u.is_active,
        CASE
            WHEN NOT u.is_active THEN 'Konto nieaktywne'
            WHEN (u.password_hash = crypt(p_password, u.password_hash)) THEN 'Haslo porawne'
            ELSE 'Haslo bledne'
        END AS message
    FROM 
        users u
    WHERE 
        u.login = p_login;

    -- Dodatkowe komunikaty w zależności od wyniku
    IF FOUND THEN
        IF (SELECT NOT u.is_active FROM users u WHERE u.login = p_login) THEN
            RAISE NOTICE 'Konto użytkownika "%", jest nieaktywne.', p_login;
        ELSIF (SELECT u.password_hash = crypt(p_password, u.password_hash) FROM users u WHERE u.login = p_login) THEN
            RAISE NOTICE 'Podane haslo uzytkownika "%", jest poprawne', p_login;
        ELSE
            RAISE NOTICE 'Podane haslo uzytkownika "%", jest bledne', p_login;
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


--DROP
;DROP FUNCTION public.verify_user_password;

--przyklad uzycia:
select * from verify_user_password ('Test', 'Test1..');