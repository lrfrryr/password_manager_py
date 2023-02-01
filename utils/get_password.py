from utils.add_new_entry import encode_main_key
from utils.database_configuration import database_config
import utils.encrypt
import pyperclip
from rich.console import Console
from rich.table import Table

console = Console()


def retrieve_database_entries(mp, ds, search, decrypt_password=False):
    db = database_config()
    cursor = db.cursor()

    # first case: user does not specify any search term
    if len(search) == 0:
        query = "SELECT * FROM pm.entries"
    # search in the database and retrieve all entries that match
    else:
        query = "SELECT * FROM pm.entries WHERE "
        for i in search:
            query += f"{i} = '{search[i]}' AND "
        query = query[:-5]

    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        console.print("[yellow][-][/yellow] No results for the search")
        return

    if (decrypt_password and len(results) > 1) or (not decrypt_password):
        if decrypt_password:
            console.print("[yellow][-][/yellow] Multiple results were found."
                          " Please, try again.")
        table = Table(title="Results")
        table.add_column("Site Name")
        table.add_column("URL", )
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")

        for i in results:
            table.add_row(i[0], i[1], i[2], i[3], "{hidden password}")
        console.print(table)
        return

    if decrypt_password and len(results) == 1:
        mk = encode_main_key(mp, ds)
        decrypted_password = utils.encrypt.decrypt(key=mk,
                                                   source=results[0][4],
                                                   key_type="bytes")
        console.print("[green][+][/green] Copied!")
        decrypted_password_decode = decrypted_password.decode()
        pyperclip.copy(decrypted_password_decode)

    db.close()
