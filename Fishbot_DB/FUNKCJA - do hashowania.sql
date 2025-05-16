--FUNCKJA do HASHOWANIA

CREATE OR REPLACE FUNCTION create_user_with_password(
    p_login VARCHAR(50),
    p_email VARCHAR(50),
    p_password TEXT,
    p_id_create_user INTEGER,
    
    -- Parametry odpowiadające kolumnom, które mogą być NULL lub mają domyślne wartości
    p_is_active BOOLEAN DEFAULT TRUE,
    p_expiration TIMESTAMP DEFAULT NULL,
    p_forename VARCHAR(50) DEFAULT NULL,
    p_surname VARCHAR(50) DEFAULT NULL,
    p_phone_number VARCHAR(20) DEFAULT NULL,
    p_description TEXT DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_salt TEXT;
    v_hash TEXT;
    v_user_id INTEGER;
    v_current_timestamp TIMESTAMP := CURRENT_TIMESTAMP;
BEGIN
    -- 1. WALIDACJA DANYCH WEJŚCIOWYCH
    -- Sprawdzenie czy login już istnieje
    IF EXISTS (SELECT 1 FROM users WHERE login = p_login) THEN
        RAISE EXCEPTION 'Login "%" już istnieje w systemie', p_login;
    END IF;
    
    -- Sprawdzenie czy email już istnieje
    IF EXISTS (SELECT 1 FROM users WHERE email = p_email) THEN
        RAISE EXCEPTION 'Email "%" już istnieje w systemie', p_email;
    END IF;

    -- 2. GENEROWANIE SKŁADNIKÓW HASŁA
    -- Generowanie soli (16 znaków, algorytm Blowfish)
    v_salt := gen_salt('bf', 12);
    
    -- Generowanie hasha hasła
    v_hash := crypt(p_password, v_salt);
    
    -- 3. TWORZENIE UŻYTKOWNIKA
    -- Pełna lista kolumn z wyraźnym określeniem źródła wartości
    INSERT INTO users (
        -- Kolumny wymagane (NOT NULL)
        login,
        email,
        password_salt,
        password_hash,
        id_create_user,
        
        -- Kolumny opcjonalne z parametrów funkcji
        is_active,
        expiration,
        forename,
        surname,
        phone_number,
        description
        
        -- Kolumny z domyślnymi wartościami w tabeli
        -- (nie podajemy ich w INSERT, aby użyć DEFAULT)
        -- id (SERIAL - autoinkrementacja)
        -- create_date (DEFAULT CURRENT_TIMESTAMP)
        -- last_password_change_date (DEFAULT CURRENT_TIMESTAMP)
    ) VALUES (
        -- Wartości dla kolumn wymaganych
        p_login,
        p_email,
        v_salt,
        v_hash,
        p_id_create_user,
        
        -- Wartości dla kolumn opcjonalnych
        p_is_active,
        p_expiration,
        p_forename,
        p_surname,
        p_phone_number,
        p_description
    ) RETURNING id INTO v_user_id;
    
    -- 4. DODATKOWE OPERACJE
    -- Jeśli ustawiono datę wygaśnięcia, dodaj wpis do historii
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
    END IF;
    
    -- 5. ZWROT ID NOWEGO UŻYTKOWNIKA
    RETURN v_user_id;
    
    -- 6. OBSŁUGA BŁĘDÓW
    EXCEPTION
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Błąd podczas tworzenia użytkownika: %', SQLERRM;
END;
$$ LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public;
-----------------------------------------------------------------