from database.db import get_connection, get_cursor, get_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = get_engine()


class Items(Base):
    __tablename__ = "items"

    name = Column(String, primary_key=True)
    value = Column(Integer)
    
Base.metadata.create_all(engine)

# Lock types
READ_LOCK = "FOR SHARE" # Shared lock (S) or READ lock (R)
WRITE_LOCK = "FOR UPDATE" # Exclusive lock (X) or WRITE lock (W)

# -- Transactions Operations -- #
# T1 sets x=100 and y=110
# T2 sets x=200 and y=220

INITIAL_VALUES = {
    "x": 0,
    "y": 0
}

def acquire_lock(cursor, item_name, lock_type):
    """
    Acquires a lock on a specific row
    """
    query = f"SELECT * FROM items WHERE name = %s {lock_type} NOWAIT"
    try:
        cursor.execute(query, (item_name,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Lock acquisition failed: {e}")
        return None


def init_database(cursor, conn):
    """Reset and initialize the database"""
    cursor.execute("DELETE FROM items")
    cursor.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn.commit()

def ss2pl_schedule_s3():
    """
    Implementationn of schedule S3 with SS2PL to ensure serializability
    """
    # reset and initialize the database
    
    
    print("Running SS2PL implementation of Schedule S3")

    # Create connections with READ COMMITTED isolation level
    conn1 = get_connection(isolation_level="READ COMMITTED")
    conn2 = get_connection(isolation_level="READ COMMITTED")

    cursor1 = get_cursor(conn1)
    cursor2 = get_cursor(conn2)

    # Initialize database
    init_database(cursor1, conn1)

    print("Database initialized")
    print("Initial table state:")
    cursor1.execute("SELECT * FROM items")
    for row in cursor1:
        print(row)
    
    conn1.commit()
    
    try:
        # T2 reads (acquired shared lock)
        print("T2: Acquiring read lock on x")
        row = acquire_lock(cursor2, "x", READ_LOCK)
        if row:
            print(f"T2: Acquired read lock on x")
            x_value = row[1]
            print(f"T2: Read x = {x_value}")

        # T1 tries to update x (will need exclusive lock)
        print("T1: Attempting to acquire write lock on x")
        try:
            # Will block or fail because T2 has a READ LOCK
            row = acquire_lock(cursor1, "x", WRITE_LOCK)
            if row:
                print(f"T1: Acquired write lock on x")
                cursor1.execute("UPDATE items SET value = 100 WHERE name = 'x'")
                print("T1: Updated x to 100")
        except Exception as e:
            print(f"T1: Failed to acquire write lock: {e}")

        # T1 commits, releasing its locks
        print("T1: Committing transaction and releasing locks")
        conn1.commit()

        # r2(y) T2 acquires read lock on y
        print("T2: Acquiring read lock on y")
        row = acquire_lock(cursor2, "y", READ_LOCK)
        if row:
            print(f"T2: Acquired read lock on y")
            y_value = row[1]
            print(f"T2: Read y = {y_value}")
            
        # w2(x) T2 acquires write lock on x
        print("T2: Acquiring write lock on x")
        row = acquire_lock(cursor2, "x", WRITE_LOCK)
        if row:
            print(f"T2: Acquired write lock on x")
            cursor2.execute("UPDATE items SET value = 220 WHERE name = 'x'")
            print("T2: Updated x to 220")

        # w2(y) T2 acquires write lock on y
        print("T2: Acquiring write lock on y")
        row = acquire_lock(cursor2, "y", WRITE_LOCK)
        if row:
            print(f"T2: Acquired write lock on y")
            cursor2.execute("UPDATE items SET value = 220 WHERE name = 'y'")
            print("T2: Updated y to 220")

        # T2 commits, releasing its locks
        print("T2: Committing transaction and releasing locks")
        conn2.commit()

        # Display final table state
        print("\nFinal table state:")
        cursor1.execute("SELECT * FROM items")
        for row in cursor1:
            print(row)

    finally:
        # Close connections
        conn1.close()
        conn2.close()

if __name__ == "__main__":
    ss2pl_schedule_s3()
            
            
        
                
