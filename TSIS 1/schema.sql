

CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday DATE,
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id),
    ADD COLUMN IF NOT EXISTS date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'unique_contact_phone'
    ) THEN
        ALTER TABLE phones
        ADD CONSTRAINT unique_contact_phone UNIQUE (contact_id, phone);
    END IF;
END;
$$;

-- Migrate old Practice 7-8 data from phonebook(name, phone), if the table exists.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'phonebook'
    ) THEN
        INSERT INTO contacts (name, group_id)
        SELECT DISTINCT pb.name, g.id
        FROM phonebook pb
        CROSS JOIN groups g
        WHERE g.name = 'Other'
          AND pb.name IS NOT NULL
        ON CONFLICT (name) DO NOTHING;

        INSERT INTO phones (contact_id, phone, type)
        SELECT c.id, pb.phone, 'mobile'
        FROM phonebook pb
        JOIN contacts c ON c.name = pb.name
        WHERE pb.phone IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM phones ph
              WHERE ph.contact_id = c.id AND ph.phone = pb.phone
          );
    END IF;
END;
$$;
