"""
Main module
"""
from app.web.router import start
from app.data import check_db

if __name__ == "__main__":
    check_db()
    start()
