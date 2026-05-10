
CREATE OR REPLACE PROCEDURE insert_contacts(p_names TEXT[], p_phones TEXT[])
AS $$
BEGIN
    FOR i IN 1 .. CARDINALITY(p_names) LOOP
        IF p_names[i] <> '' THEN
            INSERT INTO phonebook (name, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
        END IF;

    END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_contact_by_data(p_val VARCHAR)
AS $$
BEGIN
    DELETE FROM phonebook WHERE name = p_val OR phone = p_val;
END;
$$ LANGUAGE plpgsql;