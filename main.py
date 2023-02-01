import argparse
import hashlib
import pyperclip
import utils.add_new_entry
import utils.get_password
import utils.generate_password
from rich.console import Console
from rich import print as printc
from getpass import getpass
from utils.database_configuration import database_config

console = Console()

parser = argparse.ArgumentParser(description='Description')

parser.add_argument('option', help='(a)dd / (e)xtract / (g)enerate')
parser.add_argument("-l", "--login", help="Username")
parser.add_argument("-n", "--name", help="Site name")
parser.add_argument("-u", "--url", help="Site URL")
parser.add_argument("-e", "--email", help="Email")
parser.add_argument("-c", "--copy", action='store_true',
                    help='Copy password to clipboard')
parser.add_argument("--length", help="Length of the password to generate",
                    type=int)

args = parser.parse_args()


def validate_main_password():
    mp = getpass("Please, enter main password: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = database_config()
    cursor = db.cursor()
    query = "SELECT * FROM pm.secrets"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    if hashed_mp != result[0]:
        console.print("[red][!] Wrong, try again! [/red]")
        return None

    return [mp, result[1]]


def main():
    if args.option in ["add", "a"]:
        if args.name is None or args.url is None or args.login is None:
            if args.name is None:
                printc("[red][!][/red] Site Name (-s) required ")
            if args.url is None:
                printc("[red][!][/red] Site URL (-u) required ")
            if args.login is None:
                printc("[red][!][/red] Site Login (-l) required ")
            return

        if args.email is None:
            args.email = ""

        main_password_validation = validate_main_password()
        if main_password_validation is not None:
            utils.add_new_entry.add_new_entry(main_password_validation[0],
                                              main_password_validation[1],
                                              args.name, args.url, args.email,
                                              args.login)

    if args.option in ["extract", "e"]:
        main_password_validation = validate_main_password()

        search = {}
        if args.name is not None:
            search["sitename"] = args.name
        if args.url is not None:
            search["siteurl"] = args.url
        if args.email is not None:
            search["email"] = args.email
        if args.login is not None:
            search["username"] = args.login

        if main_password_validation is not None:
            utils.get_password.retrieve_database_entries(
                main_password_validation[0],
                main_password_validation[1],
                search,
                decrypt_password=args.copy)

    if args.option in ["generate", "g"]:
        if args.length is None:
            printc(
                "[red][+][/red] Please, specify length of password (--length)")
            return
        password = utils.generate_password.generate_password(args.length)
        pyperclip.copy(password)
        printc("[green][+][/green] Password has been generated and "
               "copied to the clipboard!")


main()
