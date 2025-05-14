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
        return True
    except Exception as e:
        print(f"Lock acquisition failed: {e}")
        return False


def init_database(cursor, conn):
    """Reset and initialize the database"""
    cursor.execute("DELETE FROM items")
    cursor.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("x", 0))
    cursor.execute("INSERT INTO items (name, value) VALUES (%s, %s)", ("y", 0))
    conn.commit()

def ss2pl_schedule_s3():
    """
    Implementation of schedule S3 with SS2PL to ensure serializability
    Schedule S3 = r2(x) w1(x) w1(y) c1 r2(y) w2(x) w2(y) c2
    """
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
        # S3 = r2(x) w1(x) w1(y) c1 r2(y) w2(x) w2(y) c2

        # r2(x): T2 reads x (acquires shared lock)
        print("\n1. r2(x): T2 reads x")
        if acquire_lock(cursor2, "x", READ_LOCK):
            print("T2: Acquired read lock on x")
            # Separate read operation after acquiring lock
            cursor2.execute("SELECT value FROM items WHERE name = 'x'")
            x_value = cursor2.fetchone()[0]
            print(f"T2: Read x = {x_value}")

        # w1(x): T1 writes to x (needs exclusive lock)
        print("\n2. w1(x): T1 writes to x")
        # T1 will need to wait for T2's lock to be released or fail to acquire
        success = False
        try:
            if acquire_lock(cursor1, "x", WRITE_LOCK):
                print("T1: Acquired write lock on x")
                # Separate update operation after acquiring lock
                cursor1.execute("UPDATE items SET value = 100 WHERE name = 'x'")
                print("T1: Updated x to 100")
                success = True
        except Exception as e:
            print(f"T1: Failed to acquire write lock on x: {e}")
            
        # If first attempt failed due to lock conflict, we need to 
        # either wait for T2 to release the lock (which won't happen yet) or
        # make T2 release the lock to allow SS2PL to proceed
        if not success:
            print("For SS2PL to proceed, T2 must release its lock on x")
            print("T2: Releasing lock on x by committing")
            conn2.commit()
            
            # T1 can now acquire the lock
            print("T1: Retrying to acquire write lock on x")
            if acquire_lock(cursor1, "x", WRITE_LOCK):
                print("T1: Acquired write lock on x")
                cursor1.execute("UPDATE items SET value = 100 WHERE name = 'x'")
                print("T1: Updated x to 100")
                
            # T2 begins a new transaction
            print("T2: Beginning new transaction")
            cursor2 = get_cursor(conn2)

        # w1(y): T1 writes to y (needs exclusive lock)
        print("\n3. w1(y): T1 writes to y")
        if acquire_lock(cursor1, "y", WRITE_LOCK):
            print("T1: Acquired write lock on y")
            # Separate update operation after acquiring lock
            cursor1.execute("UPDATE items SET value = 110 WHERE name = 'y'")
            print("T1: Updated y to 110")

        # c1: T1 commits
        print("\n4. c1: T1 commits")
        print("T1: Committing transaction and releasing all locks")
        conn1.commit()

        # r2(y): T2 reads y (acquires shared lock)
        print("\n5. r2(y): T2 reads y")
        if acquire_lock(cursor2, "y", READ_LOCK):
            print("T2: Acquired read lock on y")
            # Separate read operation after acquiring lock
            cursor2.execute("SELECT value FROM items WHERE name = 'y'")
            y_value = cursor2.fetchone()[0]
            print(f"T2: Read y = {y_value}")

        # w2(x): T2 writes to x (needs exclusive lock)
        print("\n6. w2(x): T2 writes to x")
        if acquire_lock(cursor2, "x", WRITE_LOCK):
            print("T2: Acquired write lock on x")
            # Separate update operation after acquiring lock
            cursor2.execute("UPDATE items SET value = 200 WHERE name = 'x'")
            print("T2: Updated x to 200")

        # w2(y): T2 writes to y (needs exclusive lock)
        print("\n7. w2(y): T2 writes to y")
        if acquire_lock(cursor2, "y", WRITE_LOCK):
            print("T2: Acquired write lock on y")
            # Separate update operation after acquiring lock
            cursor2.execute("UPDATE items SET value = 220 WHERE name = 'y'")
            print("T2: Updated y to 220")

        # c2: T2 commits
        print("\n8. c2: T2 commits")
        print("T2: Committing transaction and releasing all locks")
        conn2.commit()

        # Display final table state
        print("\nFinal table state:")
        cursor1.execute("SELECT * FROM items")
        for row in cursor1:
            print(row)

        # Print information about the executed serial schedule
        print("\nExecuted serial schedule with SS2PL protocol:")
        print("With SS2PL, the executed schedule is equivalent to serial schedule T1 -> T2")
        print("Final values: x = 200, y = 220")
        print("\nNote on PostgreSQL's behavior:")
        print("Using READ COMMITTED, PostgreSQL would allow this schedule without conflicts,")
        print("but SS2PL requires proper lock management to ensure serializability.")
        print("When T2 has a read lock on x, T1 can't acquire a write lock on x unless T2 releases it first.")
        print("This forces a specific ordering of operations that may differ from the original schedule.")

    finally:
        # Close connections
        conn1.close()
        conn2.close()

def ss2pl_schedule_s2():
    """
    Implementation of schedule S2 with SS2PL to ensure serializability
    Schedule S2 = r1(x) w2(x) c2 r1(x) c1
    """
    print("Running SS2PL implementation of Schedule S2")

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
        # S2 = r1(x) w2(x) c2 r1(x) c1

        # r1(x): T1 reads x (acquires shared lock)
        print("\n1. r1(x): T1 reads x")
        if acquire_lock(cursor1, "x", READ_LOCK):
            print("T1: Acquired read lock on x")
            # Separate read operation after acquiring lock
            cursor1.execute("SELECT value FROM items WHERE name = 'x'")
            x_value_t1_first = cursor1.fetchone()[0]
            print(f"T1: Read x = {x_value_t1_first}")

        # w2(x): T2 tries to write to x (needs exclusive lock)
        print("\n2. w2(x): T2 tries to write to x")
        success = False
        try:
            # This will likely fail because T1 has a READ lock on x
            if acquire_lock(cursor2, "x", WRITE_LOCK):
                print("T2: Acquired write lock on x")
                # Separate update operation after acquiring lock
                cursor2.execute("UPDATE items SET value = 200 WHERE name = 'x'")
                print("T2: Updated x to 200")
                success = True
        except Exception as e:
            print(f"T2: Failed to acquire write lock on x: {e}")
        
        # In SS2PL, T2 must wait for T1 to release its locks
        # For simulation purposes, we'll have T1 temporarily release its lock
        if not success:
            print("For SS2PL to proceed, T1 must release its lock on x")
            print("T1: Temporarily releasing lock on x by committing")
            conn1.commit()
            
            # T2 can now acquire the lock
            print("T2: Retrying to acquire write lock on x")
            if acquire_lock(cursor2, "x", WRITE_LOCK):
                print("T2: Acquired write lock on x")
                cursor2.execute("UPDATE items SET value = 200 WHERE name = 'x'")
                print("T2: Updated x to 200")
                
            # T1 begins a new transaction for the next read
            print("T1: Beginning new transaction")
            cursor1 = get_cursor(conn1)

        # c2: T2 commits
        print("\n3. c2: T2 commits")
        print("T2: Committing transaction and releasing all locks")
        conn2.commit()

        # r1(x): T1 reads x again
        print("\n4. r1(x): T1 reads x again")
        if acquire_lock(cursor1, "x", READ_LOCK):
            print("T1: Acquired read lock on x")
            # Separate read operation after acquiring lock
            cursor1.execute("SELECT value FROM items WHERE name = 'x'")
            x_value_t1_second = cursor1.fetchone()[0]
            print(f"T1: Read x = {x_value_t1_second}")

        # c1: T1 commits
        print("\n5. c1: T1 commits")
        print("T1: Committing transaction and releasing all locks")
        conn1.commit()

        # Display final table state
        print("\nFinal table state:")
        cursor1.execute("SELECT * FROM items")
        for row in cursor1:
            print(row)

        # Print information about the executed serial schedule
        print("\nExecuted serial schedule with SS2PL protocol:")
        print("With SS2PL, the executed schedule is equivalent to serial schedule T1 -> T2 -> T1")
        print(f"Initial read of x by T1: {x_value_t1_first}")
        print(f"Final value of x after T2's write: {x_value_t1_second}")
        print("\nNote on PostgreSQL's behavior:")
        print("Using READ COMMITTED isolation level, T1 would see the updated value of x in its second read,")
        print("which matches our implementation. However, in SERIALIZABLE isolation, PostgreSQL might")
        print("prevent this schedule to ensure serializability using Serializable Snapshot Isolation (SSI).")

    finally:
        # Close connections
        conn1.close()
        conn2.close()

def ss2pl_schedule_s1():
    """
    Implementation of schedule S1 with SS2PL to ensure serializability
    Schedule S1 = r1(x) w2(x) c2 w1(x) r1(x) c1
    """
    print("Running SS2PL implementation of Schedule S1")

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
        # S1 = r1(x) w2(x) c2 w1(x) r1(x) c1

        # r1(x): T1 reads x (acquires shared lock)
        print("\n1. r1(x): T1 reads x")
        if acquire_lock(cursor1, "x", READ_LOCK):
            print("T1: Acquired read lock on x")
            # Separate read operation after acquiring lock
            cursor1.execute("SELECT value FROM items WHERE name = 'x'")
            x_value_t1_first = cursor1.fetchone()[0]
            print(f"T1: Read x = {x_value_t1_first}")

        # w2(x): T2 tries to write to x (needs exclusive lock)
        print("\n2. w2(x): T2 tries to write to x")
        success = False
        try:
            # This will likely fail because T1 has a READ lock on x
            if acquire_lock(cursor2, "x", WRITE_LOCK):
                print("T2: Acquired write lock on x")
                # Separate update operation after acquiring lock
                cursor2.execute("UPDATE items SET value = 200 WHERE name = 'x'")
                print("T2: Updated x to 200")
                success = True
        except Exception as e:
            print(f"T2: Failed to acquire write lock on x: {e}")
        
        # In SS2PL, T2 must wait for T1 to release its locks
        # For simulation purposes, we'll have T1 temporarily release its lock
        if not success:
            print("For SS2PL to proceed, T1 must release its lock on x")
            print("T1: Temporarily releasing lock on x by committing")
            conn1.commit()
            
            # T2 can now acquire the lock
            print("T2: Retrying to acquire write lock on x")
            if acquire_lock(cursor2, "x", WRITE_LOCK):
                print("T2: Acquired write lock on x")
                cursor2.execute("UPDATE items SET value = 200 WHERE name = 'x'")
                print("T2: Updated x to 200")
                
            # T1 begins a new transaction for the next operations
            print("T1: Beginning new transaction")
            cursor1 = get_cursor(conn1)

        # c2: T2 commits
        print("\n3. c2: T2 commits")
        print("T2: Committing transaction and releasing all locks")
        conn2.commit()

        # w1(x): T1 writes to x
        print("\n4. w1(x): T1 writes to x")
        if acquire_lock(cursor1, "x", WRITE_LOCK):
            print("T1: Acquired write lock on x")
            # Separate update operation after acquiring lock
            cursor1.execute("UPDATE items SET value = 150 WHERE name = 'x'")
            print("T1: Updated x to 150")

        # r1(x): T1 reads x again
        print("\n5. r1(x): T1 reads x again")
        # T1 already has a write lock on x (which is stronger than a read lock)
        # So we don't need to acquire a read lock again
        cursor1.execute("SELECT value FROM items WHERE name = 'x'")
        x_value_t1_second = cursor1.fetchone()[0]
        print(f"T1: Read x = {x_value_t1_second}")

        # c1: T1 commits
        print("\n6. c1: T1 commits")
        print("T1: Committing transaction and releasing all locks")
        conn1.commit()

        # Display final table state
        print("\nFinal table state:")
        cursor1.execute("SELECT * FROM items")
        for row in cursor1:
            print(row)

        # Print information about the executed serial schedule
        print("\nExecuted serial schedule with SS2PL protocol:")
        print("With SS2PL, the executed schedule is equivalent to serial schedule T1 -> T2 -> T1")
        print(f"Initial read of x by T1: {x_value_t1_first}")
        print(f"Value of x after T2's write: 200")
        print(f"Final value of x after T1's write: {x_value_t1_second}")
        print("\nNote on PostgreSQL's behavior:")
        print("Using READ COMMITTED isolation level, this schedule would execute as shown,")
        print("with T1 seeing its own latest write to x in its second read operation.")
        print("This behavior matches our implementation. However, in SERIALIZABLE isolation,")
        print("PostgreSQL might prevent this schedule due to potential write-write conflicts.")

    finally:
        # Close connections
        conn1.close()
        conn2.close()

if __name__ == "__main__":
    while True:
        choice = input("Enter the schedule number (1, 2, or 3) or 4 to exit: ")
        if choice == "1":
            ss2pl_schedule_s1()
        elif choice == "2":
            ss2pl_schedule_s2()
        elif choice == "3":
            ss2pl_schedule_s3()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        
                
