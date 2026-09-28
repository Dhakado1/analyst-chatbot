import mysql.connector
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
    except mysql.connector.Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    conn = None
    try:
        # Connect without database first to create it
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )
        cursor = conn.cursor()
        db_name = os.getenv("MYSQL_DATABASE")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        with open('schema.sql', 'r') as file:
            sql_script = file.read()
            
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
                    
        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def execute_query(sql):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return {"results": results}
    except mysql.connector.Error as e:
        return {"error": str(e)}
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()