from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from rich.console import Console
import utils.encrypt
from utils.database_configuration import database_config

console = Console()


def encode_main_key(mp, ds):
    passw = mp.encode()
    salt = ds.encode()
    key = PBKDF2(passw, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def add_new_entry(mp, ds, sitename, siteurl, email, username):
    password = getpass("Enter Password:")
    mk = encode_main_key(mp, ds)

    encrypted_password = utils.encrypt.encrypt(key=mk,
                                               source=password,
                                               key_type="bytes")

    # add the encrypted password to the database
    db = database_config()
    cursor = db.cursor()

    query = "INSERT INTO pm.entries " \
            "(sitename, siteurl, email, username, password) " \
            "values (%s, %s, %s, %s, %s)"
    val = (sitename, siteurl, email, username, encrypted_password)
    cursor.execute(query, val)
    db.commit()

    console.print("[green][+] insertion was successful.")
