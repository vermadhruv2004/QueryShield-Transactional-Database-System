import pymysql

def get_connection():
    try:
        db = pymysql.connect(
            host="localhost",
            user="queryuser",
            password="query123",
            database="queryshield"
        )
        return db

    except Exception as e:
        print("Database Connection Error:", e)
        return None