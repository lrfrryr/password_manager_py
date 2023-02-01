# requirements for connecting with database
import mysql.connector
from rich.console import Console

# for better display on command line
console = Console()


def database_config():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            )
    except Exception:
        console.print_exception(show_locals=True)

    return db