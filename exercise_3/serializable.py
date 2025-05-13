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


def schedule_s1():

    
    
    # First connection
    conn1 = get_connection(isolation_level="SERIALIZABLE")
    cursor1 = get_cursor(conn1)

    # Initialize the database using first connection
    cursor1.execute("DELETE FROM items")
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn1.commit()

    # Second connection
    conn2 = get_connection(isolation_level="SERIALIZABLE")
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
    
def schedule_s2():
    # initialize_database using first connection
    conn1 = get_connection(isolation_level="SERIALIZABLE")
    cursor1 = get_cursor(conn1)
    cursor1.execute("DELETE FROM items")
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn1.commit()

    # Second connection
    conn2 = get_connection(isolation_level="SERIALIZABLE")
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

def schedule_s3():
    # initialize_database using first connection
    conn1 = get_connection(isolation_level="SERIALIZABLE")
    cursor1 = get_cursor(conn1)
    cursor1.execute("DELETE FROM items")
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor1.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn1.commit()

    # Second connection
    conn2 = get_connection(isolation_level="SERIALIZABLE")
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
    

if __name__ == "__main__":
    # schedule_s1()

    # print("--------Result of schedule s1:---------")
    # print_table()

    # schedule_s2()

    # print("--------Result of schedule s2:---------")
    # print_table()

    schedule_s3()

    print("--------Result of schedule s3:---------")
    print_table()