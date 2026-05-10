import csv
from connect import connect_db

def insert_or_update_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("CALL insert_contact(%s, %s)", (name, phone))
        conn.commit()
        print("Contact successfully added or updated.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def insert_many_from_list():
    names = []
    phones = []
    
    count = int(input("How many? "))
    for _ in range(count):
        names.append(input("Name: "))
        phones.append(input("Phone: "))

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("CALL insert_contacts(%s, %s)", (names, phones))
        conn.commit()
        print("Processing completed.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def search_by_pattern():
    pattern = input("Enter part of name or phone to search: ")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts_pattern(%s)", (pattern,))
    
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    else:
        print("No records found.")
    
    cur.close()
    conn.close()

def get_with_pagination():
    try:
        limit = int(input("Enter limit: "))
        offset = int(input("Enter offset: "))
    except ValueError:
        print("Error ")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paged(%s, %s)", (limit, offset))
    
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    cur.close()
    conn.close()

def delete_by_name_or_phone():
    target = input("Enter name or phone to delete: ")

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact_by_data(%s)", (target,))
        conn.commit()
        print("Record deleted if it existed.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def main():
    while True:
        print("1 Add/Update Contact")
        print("2 Insert Many from User Input")
        print("3 Search by Pattern")
        print("4 Get with Pagination")
        print("5 Delete Contact")
        print("0 Exit")

        choice = input("Select an option: ")

        if choice == "1":
            insert_or_update_contact()
        elif choice == "2":
            insert_many_from_list()
        elif choice == "3":
            search_by_pattern()
        elif choice == "4":
            get_with_pagination()
        elif choice == "5":
            delete_by_name_or_phone()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()