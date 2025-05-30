from database.db import get_connection, get_cursor, get_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = get_engine()

class Items(Base):
    __tablename__ = "items"

    name = Column(String, primary_key=True)
    value = Column(Integer)

Base.metadata.create_all(engine) # Create the table

# -- Transactions Operations -- #
# T1 sets x=100 and y=110
# T2 sets x=200 and y=220

INITIAL_VALUES = {
    "x": 0,
    "y": 0
}


def print_table():
    with get_connection() as conn:
        with get_cursor(conn) as cursor:
            cursor.execute("SELECT * FROM items")
            for row in cursor:
                print(row)


def schedule_s1(isolation_level):
    
    # First connection
    conn1 = get_connection(isolation_level=isolation_level)
    cursor1 = get_cursor(conn1)

    # Initialize the database using first connection
    cursor1.execute("DELETE FROM items")
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn1.commit()

    # Second connection
    conn2 = get_connection(isolation_level=isolation_level)
    cursor2 = get_cursor(conn2)

    # r1(x)
    cursor1.execute("SELECT * FROM items WHERE name = 'x'")
    x_value = cursor1.fetchone()[1]

    # w2(x)
    cursor2.execute("UPDATE items SET value = 200 WHERE name = 'x'")
    
    # c2
    conn2.commit()

    # w1(x)
    cursor1.execute("UPDATE items SET value = 100 WHERE name = 'x'")

    # r1(x)
    cursor1.execute("SELECT * FROM items WHERE name = 'x'")
    x_value = cursor1.fetchone()[1]

    # c1
    conn1.commit()

    # print the table
    print("--------Result of schedule s1:---------")
    cursor1.execute("SELECT * FROM items")
    for row in cursor1:
        print(row)
    
def schedule_s2(isolation_level):
    # initialize_database using first connection
    conn1 = get_connection(isolation_level=isolation_level)
    cursor1 = get_cursor(conn1)
    cursor1.execute("DELETE FROM items")
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn1.commit()

    # Second connection
    conn2 = get_connection(isolation_level=isolation_level)
    cursor2 = get_cursor(conn2)

    # r1(x)
    cursor1.execute("SELECT * FROM items WHERE name = 'x'")
    x_value = cursor1.fetchone()[1]

    # w2(x)
    cursor2.execute("UPDATE items SET value = 200 WHERE name = 'x'")
    
    # c2
    conn2.commit()

    # r1(x)
    cursor1.execute("SELECT * FROM items WHERE name = 'x'")
    x_value = cursor1.fetchone()[1]

    # c1
    conn1.commit()
    
    # Print the table
    print("--------Result of schedule s2:---------")
    cursor1.execute("SELECT * FROM items")
    for row in cursor1:
        print(row)

def schedule_s3(isolation_level):
    # initialize_database using first connection
    conn1 = get_connection(isolation_level=isolation_level)
    cursor1 = get_cursor(conn1)
    cursor1.execute("DELETE FROM items")
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn1.commit()

    # Second connection
    conn2 = get_connection(isolation_level=isolation_level)
    cursor2 = get_cursor(conn2)

    # r2(x)
    cursor2.execute("SELECT * FROM items WHERE name = 'x'")
    x_value = cursor2.fetchone()[1]

    # w1 (x)
    cursor1.execute("UPDATE items SET value = 100 WHERE name = 'x'")

    # w1(y)
    cursor1.execute("UPDATE items SET value = 110 WHERE name = 'y'")

    # c1
    conn1.commit()
    
    # r2(y)
    cursor2.execute("SELECT * FROM items WHERE name = 'y'")
    y_value = cursor2.fetchone()[1]

    # w2(x)
    cursor2.execute("UPDATE items SET value = 220 WHERE name = 'x'")

    # w2(y)
    cursor2.execute("UPDATE items SET value = 220 WHERE name = 'y'")

    # c2
    conn2.commit()

    # Print the table
    print("--------Result of schedule s3:---------")
    cursor1.execute("SELECT * FROM items")
    for row in cursor1:
        print(row)
    

if __name__ == "__main__":

    while True:
        isolation_level_choice = input("Enter your choice of isolation level:\n1. READ COMMITTED\n2. REPEATABLE READ\n3. SERIALIZABLE\n 4. Exit\n")
        if isolation_level_choice == "1":
            isolation_level = "READ COMMITTED"
        elif isolation_level_choice == "2":
            isolation_level = "REPEATABLE READ"
        elif isolation_level_choice == "3":
            isolation_level = "SERIALIZABLE"
        elif isolation_level_choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        schedule_choice = input("Enter the schedule number (1, 2, or 3) or 4 to go back to the main menu: ")
        if schedule_choice == "1":
            schedule_s1(isolation_level)
        elif schedule_choice == "2":
            schedule_s2(isolation_level)
        elif schedule_choice == "3":
            schedule_s3(isolation_level)
        elif schedule_choice == "4":
            continue
        else:
            print("Invalid choice. Please try again.")
            continue