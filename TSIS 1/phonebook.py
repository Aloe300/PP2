import csv
import json
import os
from connect import connect_db


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection():
    conn = connect_db()
    if conn is None:
        raise Exception("Database connection failed. Check database.ini and PostgreSQL password.")
    return conn


def run_sql_file(filename):
    path = os.path.join(BASE_DIR, filename)
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(path, "r", encoding="utf-8") as file:
            sql = file.read()
        cur.execute(sql)
        conn.commit()
        print(f"{filename} executed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error while executing {filename}: {e}")
    finally:
        cur.close()
        conn.close()


def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")


def print_contacts(rows):
    if not rows:
        print("No records found.")
        return

    for row in rows:
        print(
            f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | "
            f"Birthday: {row[3]} | Group: {row[4]} | Phones: {row[5]}"
        )


def ask_birthday():
    birthday = input("Birthday (YYYY-MM-DD, empty if none): ").strip()
    return birthday if birthday else None


def ask_phone_type():
    phone_type = input("Phone type (home/work/mobile): ").strip().lower()
    if phone_type not in ("home", "work", "mobile"):
        print("Invalid type. Mobile will be used by default.")
        return "mobile"
    return phone_type


def get_or_create_group(cur, group_name):
    if not group_name:
        group_name = "Other"

    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact_extended():
    name = input("Name: ").strip()
    email = input("Email: ").strip() or None
    birthday = ask_birthday()
    group_name = input("Group (Family/Work/Friend/Other): ").strip() or "Other"
    phone = input("Phone: ").strip()
    phone_type = ask_phone_type()

    if not name:
        print("Name cannot be empty.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        group_id = get_or_create_group(cur, group_name)

        cur.execute(
            """
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id
            """,
            (name, email, birthday, group_id)
        )
        contact_id = cur.fetchone()[0]

        if phone:
            cur.execute(
                """
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (contact_id, phone) DO UPDATE
                SET type = EXCLUDED.type
                """,
                (contact_id, phone, phone_type)
            )

        conn.commit()
        print("Contact saved successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def add_phone_console():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = ask_phone_type()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def move_to_group_console():
    name = input("Contact name: ").strip()
    group_name = input("New group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print("Contact moved successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def advanced_search():
    query = input("Search by name, email, or phone: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        print_contacts(cur.fetchall())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def filter_by_group():
    group_name = input("Group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM search_contacts('')
            WHERE group_name ILIKE %s
            ORDER BY contact_name
            """,
            (group_name,)
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def search_by_email():
    email_part = input("Enter part of email: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT *
            FROM search_contacts('')
            WHERE email ILIKE %s
            ORDER BY contact_name
            """,
            (f"%{email_part}%",)
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def sort_contacts():
    print("Sort by: 1 name | 2 birthday | 3 date added")
    choice = input("Choose: ").strip()

    allowed = {
        "1": "c.name",
        "2": "c.birthday NULLS LAST",
        "3": "c.date_added"
    }
    order_by = allowed.get(choice)
    if order_by is None:
        print("Invalid choice.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            SELECT
                c.id,
                c.name,
                c.email,
                c.birthday,
                g.name AS group_name,
                COALESCE(STRING_AGG(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.id), '') AS phones
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            LEFT JOIN phones ph ON ph.contact_id = c.id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.date_added
            ORDER BY {order_by}
            """
        )
        print_contacts(cur.fetchall())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def pagination_loop():
    try:
        limit = int(input("Page size: "))
    except ValueError:
        print("Page size must be a number.")
        return

    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT *
                FROM search_contacts('')
                ORDER BY contact_name
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )
            rows = cur.fetchall()
            print("\n--- PAGE ---")
            print_contacts(rows)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cur.close()
            conn.close()

        command = input("next / prev / quit: ").strip().lower()
        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Unknown command.")


def export_to_json():
    filename = input("JSON filename to export (default contacts.json): ").strip() or "contacts.json"
    path = os.path.join(BASE_DIR, filename)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.name
            """
        )
        contacts = []
        for contact_id, name, email, birthday, group_name in cur.fetchall():
            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
                (contact_id,)
            )
            phones = [
                {"phone": phone, "type": phone_type}
                for phone, phone_type in cur.fetchall()
            ]
            contacts.append({
                "name": name,
                "email": email,
                "birthday": birthday.isoformat() if birthday else None,
                "group": group_name,
                "phones": phones
            })

        with open(path, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)

        print(f"Exported to {path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def save_contact_from_data(cur, data, overwrite=False):
    name = data.get("name")
    email = data.get("email")
    birthday = data.get("birthday") or None
    group_name = data.get("group") or "Other"
    phones = data.get("phones", [])

    if not name:
        return

    group_id = get_or_create_group(cur, group_name)

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    existing = cur.fetchone()

    if existing and not overwrite:
        return

    if existing and overwrite:
        contact_id = existing[0]
        cur.execute(
            """
            UPDATE contacts
            SET email = %s, birthday = %s, group_id = %s
            WHERE id = %s
            """,
            (email, birthday, group_id, contact_id)
        )
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
    else:
        cur.execute(
            """
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (name, email, birthday, group_id)
        )
        contact_id = cur.fetchone()[0]

    for item in phones:
        phone = item.get("phone")
        phone_type = item.get("type", "mobile")
        if phone_type not in ("home", "work", "mobile"):
            phone_type = "mobile"
        if phone:
            cur.execute(
                """
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (contact_id, phone) DO UPDATE
                SET type = EXCLUDED.type
                """,
                (contact_id, phone, phone_type)
            )


def import_from_json():
    filename = input("JSON filename to import: ").strip()
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        print("File not found.")
        return

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()
    try:
        for item in data:
            name = item.get("name")
            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            exists = cur.fetchone() is not None

            overwrite = False
            if exists:
                answer = input(f"Duplicate contact '{name}'. skip or overwrite? ").strip().lower()
                if answer == "skip":
                    continue
                elif answer == "overwrite":
                    overwrite = True
                else:
                    print("Unknown answer. Skipped.")
                    continue

            save_contact_from_data(cur, item, overwrite=overwrite)

        conn.commit()
        print("JSON import completed.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def import_from_csv_extended():
    filename = input("CSV filename (default contacts.csv): ").strip() or "contacts.csv"
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        print("File not found.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data = {
                    "name": row.get("name"),
                    "email": row.get("email"),
                    "birthday": row.get("birthday") or None,
                    "group": row.get("group") or "Other",
                    "phones": [
                        {
                            "phone": row.get("phone"),
                            "type": row.get("type") or "mobile"
                        }
                    ]
                }
                save_contact_from_data(cur, data, overwrite=True)

        conn.commit()
        print("CSV import completed.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def main():
    while True:
        print("\n===== EXTENDED PHONEBOOK =====")
        print("1 Setup database schema and procedures")
        print("2 Add/Update extended contact")
        print("3 Add phone to existing contact")
        print("4 Move contact to group")
        print("5 Advanced search by name/email/phone")
        print("6 Filter by group")
        print("7 Search by email")
        print("8 Sort contacts")
        print("9 Paginated navigation")
        print("10 Export to JSON")
        print("11 Import from JSON")
        print("12 Import from CSV extended")
        print("0 Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            setup_database()
        elif choice == "2":
            add_contact_extended()
        elif choice == "3":
            add_phone_console()
        elif choice == "4":
            move_to_group_console()
        elif choice == "5":
            advanced_search()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            sort_contacts()
        elif choice == "9":
            pagination_loop()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "12":
            import_from_csv_extended()
        elif choice == "0":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
