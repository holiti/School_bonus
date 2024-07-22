CREATE USER sbonus_admin WITH PASSWORD '4567123abe';
CREATE DATABASE school_bonus WITH OWNER sbonus_admin;
ALTER USER sbonus_admin WITH SUPERUSER;

/*
linux:
    sudo nano /etc/postgresql/15/main/pg_hba.conf;
    host    school_bonus    sbonus_admin     127.0.0.1/32            md5
    sudo systemctl restart postgresql;

windows:
    https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
    chcp 1251
    pyinstaller main.py
*/

CREATE TABLE main(
    pers_id serial primary key,
    pers_name character varying(150) NOT NULL UNIQUE,
    gmail character varying(100) NOT NULL,
    required_hours smallint DEFAULT 0,
    completed_hours smallint DEFAULT 0,
    hour_bonus smallint DEFAULT 0,
    bonus_sum smallint DEFAULT 0
);

CREATE TABLE variable(
    id serial,
    vname character varying(20),
    var integer,
    var_t text
);

INSERT INTO variable(vname, var,var_t) VALUES ('max_fond',0,NULL),('sum_bonus',0,NULL),('save_path',NULL,NULL);



CREATE OR REPLACE FUNCTION process_hedit() RETURNS TRIGGER AS $$
    DECLARE
        new_val smallint := ((NEW.completed_hours - NEW.required_hours) * 5);
    BEGIN
        UPDATE main SET hour_bonus = new_val, bonus_sum = bonus_sum + new_val - OLD.hour_bonus WHERE pers_id = NEW.pers_id;

        RETURN NEW;
    END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER hbonus_edit
AFTER UPDATE OF completed_hours ON main
    FOR EACH ROW EXECUTE PROCEDURE process_hedit();



CREATE OR REPLACE FUNCTION process_sedit() RETURNS TRIGGER AS $$
    BEGIN
        UPDATE variable SET var = var - OLD.bonus_sum WHERE id = 2;
        IF NEW.bonus_sum IS NOT NULL THEN 
            UPDATE variable SET var = var + NEW.bonus_sum WHERE id = 2;
        END IF;
        RETURN NEW;
    END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER edit_persons
AFTER UPDATE OF bonus_sum OR DELETE ON main
    FOR EACH ROW EXECUTE PROCEDURE process_sedit();
