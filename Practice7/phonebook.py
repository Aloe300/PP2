import csv
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")


def insert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact inserted successfully.")
    except Exception as e:
        print("Error:", e)
        conn.rollback()

    cur.close()
    conn.close()


def insert_from_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) != 2:
                    continue

                name, phone = row

                try:
                    cur.execute(
                        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                        (name.strip(), phone.strip())
                    )
                except Exception:
                    conn.rollback()
                    continue

        conn.commit()
        print("Contacts imported from CSV.")
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print("Error:", e)
        conn.rollback()

    cur.close()
    conn.close()


def update_contact(name, new_phone):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE name = %s",
            (new_phone, name)
        )

        if cur.rowcount == 0:
            print("Contact not found.")
        else:
            print("Contact updated successfully.")

        conn.commit()
    except Exception as e:
        print("Error:", e)
        conn.rollback()

    cur.close()
    conn.close()


def search_contact(keyword):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT * FROM phonebook
            WHERE name ILIKE %s OR phone ILIKE %s
            """,
            (keyword, keyword)
        )

        rows = cur.fetchall()

        if rows:
            print("Search results:")
            for row in rows:
                print(row)
        else:
            print("No matching contacts found.")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def delete_contact(name):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))

        if cur.rowcount == 0:
            print("Contact not found.")
        else:
            print("Contact deleted successfully.")

        conn.commit()
    except Exception as e:
        print("Error:", e)
        conn.rollback()

    cur.close()
    conn.close()


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM phonebook ORDER BY id")
        rows = cur.fetchall()

        if rows:
            print("All contacts:")
            for row in rows:
                print(row)
        else:
            print("Phonebook is empty.")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert contact")
        print("3. Import contacts from CSV")
        print("4. Update contact")
        print("5. Search contact")
        print("6. Delete contact")
        print("7. Show all contacts")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_contact(name, phone)
        elif choice == "3":
            filename = input("Enter CSV filename (default contacts.csv): ").strip()
            if filename == "":
                filename = "contacts.csv"
            insert_from_csv(filename)
        elif choice == "4":
            name = input("Enter name to update: ")
            new_phone = input("Enter new phone: ")
            update_contact(name, new_phone)
        elif choice == "5":
            keyword = input("Enter name or phone to search: ")
            search_contact(keyword)
        elif choice == "6":
            name = input("Enter name to delete: ")
            delete_contact(name)
        elif choice == "7":
            show_all_contacts()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()


#ILIKE — это поиск без учёта регистра
#execute() выполняет SQL-запрос.
#fetchall() возвращает список результатов