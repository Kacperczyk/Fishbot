-- Tabela users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    expiration TIMESTAMP,
    forename VARCHAR(50),
    surname VARCHAR(50),
    email VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    description TEXT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_create_user INTEGER NOT NULL, --> tutaj potem dodamy INTEGER REFERENCES users(id), ALTER TABLE users ADD CONSTRAINT fk_users_create_user FOREIGN KEY (id_create_user) REFERENCES users(id) 
    last_password_change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password_salt TEXT,
    password_hash TEXT
);

ALTER TABLE users 
ADD CONSTRAINT fk_users_create_user 
FOREIGN KEY (id_create_user) REFERENCES users(id) 


-- Tabela users_expiration_history
CREATE TABLE users_expiration_history (
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL REFERENCES users(id),
    activation_date TIMESTAMP NOT NULL,
    expiration_date TIMESTAMP NOT NULL
);

--------------------------------------------------------------------------------------
select * from users order by id asc;
select * from users_expiration_history;

update users set expiration = null where login = 'adm_kkacperczyk'; 
--Sekwencje
SELECT currval(pg_get_serial_sequence('users', 'id')) AS current_value;
SELECT nextval('users_id_seq') AS next_value; --Uwaga to dodaje +1
ALTER SEQUENCE users_id_seq RESTART WITH 3; --> czyli kolejne bedzie mialo 2

---DO HASHOWANIA HASEL ITP
CREATE EXTENSION IF NOT EXISTS pgcrypto;




































