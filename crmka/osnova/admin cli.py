import sqlite3

conn = sqlite3.connect('crmka/locallibrary/db.sqlite3')
cursor = conn.cursor()

def changes_in_table():
    table_name = input("Table name: ")
    set_field = input("Field to update: ")
    new_value = input("New value: ")
    filter_field = input("Filter field: ")
    filter_value = input("Filter value: ")
    
    # Execute the update query
    query = f"UPDATE catalog_{table_name} SET {set_field} = ? WHERE {filter_field} = ?"
    cursor.execute(query, (new_value, filter_value))

    try:
        conn.commit()
        print("Data updated successfully!")
    except sqlite3.Error as e:
        print(f"Error: {e}")


def delete_records_table():
    table_name = input("Table name: ")
    filter_field = input("Filter field: ")
    filter_value = input("Filter value: ")
    
    query = f"DELETE FROM catalog_{table_name} WHERE {filter_field} = ?"
    cursor.execute(query, (filter_value,))

    try:
        conn.commit()
        print("Record deleted!")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def write_in_table():
    table_name = input("Table name: ")
    try:
        cursor.execute(f"PRAGMA table_info(catalog_{table_name})")
        columns = [row[1] for row in cursor.fetchall() if row[1] != 'id']
        
        if not columns:
            print("No columns found in the table (or only 'id' column exists).")
            return
        
        fields = {column: input(f"Enter {column}: ") for column in columns}
        
        columns_str = ", ".join(fields.keys())
        values_str = ", ".join("?" * len(fields))
        query = f"INSERT INTO catalog_{table_name} ({columns_str}) VALUES ({values_str})"
        
        cursor.execute(query, tuple(fields.values()))
        
        print(f"Record added: {fields}")
        
        conn.commit()
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    


def show_table():
    table_name = input("Table name: ")
    cursor.execute(f"PRAGMA table_info(catalog_{table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    
    print(" | ".join(columns))
    
    cursor.execute(f"SELECT * FROM catalog_{table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(" | ".join(str(value) for value in row))


def menu():
    
    while True:
        action = input("ACTION: ").strip().upper()
        if action == "CHANGES IN":
            changes_in_table()
        elif action == "DELETE IN":
            delete_records_table()
        elif action == "WRITE IN":
            write_in_table()
        elif action == "SHOW TABLE":
            show_table()
        elif action == "HELP":
            print("""
                CHANGES IN - change a table's field
                DELETE IN - delete a record from a table
                WRITE IN - write in a table
                SHOW TABLE - prints a table's contents
            """)
        elif action == "QUIT":
            conn.close()
            break
        else:
            print("No such command\n")


if __name__ == "__main__":
    menu()
