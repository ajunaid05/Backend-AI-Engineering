import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host = os.getenv("POSTGRES_HOST"),
        port = os.getenv("POSTGRES_PORT"),
        database = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD"),
    )

def get_alltasks():
    conn=get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("Select * from tasks Order By id")
            return cursor.fetchall()
    finally:
        conn.close()

def get_task(task_id: int):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("Select * from tasks where id = %s",(task_id,))
            return cursor.fetchone()
    finally:
        conn.close()

def create_task(title: str,done: bool = False):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING *
            """, (title, done)
                           )
            task = cursor.fetchone()
            conn.commit()
            return task
    finally:
        conn.close()   

def update_tasks(task_id: int, title:str,done: bool):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
            UPDATE tasks 
            SET title = %s , done = %s
            WHERE id = %s
            RETURNING * 
               """,
            (title,done,task_id)
               )  
            task = cursor.fetchone()
            conn.commit()

            return task
    finally:
        conn.close()

def del_task(task_id: int):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
            DELETE FROM tasks WHERE id = %s
            """, (task_id,)
            )
        deleted = cursor.rowcount
        conn.commit()

        return deleted
    finally:
        conn.close()

if __name__ == "__main__":
    print("Print All Tasks")
    print(get_alltasks())

    print("Print Task with ID:1")
    print(get_task(1))

    print("Create new task")
    print(create_task("Learn PostgresSQL"))

    # print("\nUPDATING TASK:")
    # print(update_tasks(3, "Updated Task", True))

    # print("\nDELETING TASK:")
    # print(del_task(2))