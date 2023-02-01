import hashlib
import random
import string
from getpass import getpass
from utils.database_configuration import database_config
from rich.console import Console

console = Console()


def generate_device_secret(leng=10):
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=leng))


def config():
    # create Database

    db = database_config()
    cursor = db.cursor()

    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception:
        console.print("[red][!] There was an error "
                      "while creating the database.")
        console.print_exception(show_locals=True)
    console.print("[green][+][/green] Database was created.")

    # create Tables
    query = "CREATE TABLE pm.secrets (mainkey_hash TEXT NOT NULL, " \
            "device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    console.print("[green][+][/green] 'secrets' table was created")

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, " \
            "siteurl TEXT NOT NULL, email TEXT, username TEXT, " \
            "password TEXT NOT NULL)"
    res = cursor.execute(query)
    console.print("[green][+][/green] 'entries' table was created")

    mp = ""
    while True:
        # Get the user to create main password
        mp = getpass("Enter a new main password: ")
        if mp == getpass("Repeat main password: ") and mp != "":
            break
        console.print("[yellow][-] Please try again.[/yellow]")

    # password1234
    # Hash the main password
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    console.print(
        "[green][+][/green] hash for main password was generated.")

    # Generate device secret
    ds = generate_device_secret()
    console.print("[green][+][/green] device secret was generated.")

    # Insert values into database
    query = "INSERT INTO pm.secrets " \
            "(mainkey_hash, device_secret) values (%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()
    console.print("[green][+] insertion was successful. "
                  "Configuration completed![/green]")

    db.close()


config()
