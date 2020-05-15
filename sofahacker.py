import os
from subprocess import call

from colorama import init, Fore
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style


# Написано на python 3.8 (64-bit)
# Зависимости:
#   colorama
#   prompt_toolkit


init()


class SIGNALS:
    load = Fore.BLUE + '[#]' + Fore.RESET
    error = Fore.RED + '[x]' + Fore.RESET
    success = Fore.GREEN + '[v]' + Fore.RESET
    warning = Fore.YELLOW + '[!]' + Fore.RESET


HELP = '''
help:

scan
    db
    tbl
    site
    vuln

dump
    table

set
    database
    site
    table
    
show
    database
    site
    table

exit
help
clear
banner
'''

BANNER = f'''
{Fore.BLUE}
 _____        __        _                _             
/  ___|      / _|      | |              | |            
\ `--.  ___ | |_ __ _  | |__   __ _  ___| | _____ _ __ 
 `--. \/ _ \|  _/ _` | | '_ \ / _` |/ __| |/ / _ \ '__|
/\__/ / (_) | || (_| | | | | | (_| | (__|   <  __/ |   
\____/ \___/|_| \__,_| |_| |_|\__,_|\___|_|\_\___|_|   
{Fore.RESET}
        {Fore.RED}!только для образовательных целей!{Fore.RESET}
         {Fore.BLUE}обертка на python3.8 над sqlmap
         список доступных комманд - help{Fore.RESET}
        {Fore.RED}!только для образовательных целей!{Fore.RESET}
'''

SCAN_DATABASE = 'sqlmap -u $SITE -D $DATABASE --tables --threads 10 --random-agent'
SCAN_TABLE = 'sqlmap -u $SITE -D $DATABASE -T #TABLE --columns --threads 10 --random-agent'
SCAN_SITE = 'sqlmap -u $SITE --dbs --threads 10 --random-agent'
SCAN_FOR_VULN = 'sqlmap -u $SITE --threads 10 --random-agent'
DUMP_TABLE = 'sqlmap -u $SITE -D $DATABASE -T $TABLE --dump --threads 10 --random-agent'

USER_LOGIN = os.getlogin()
CURRENT_WORKING_DIRECTORY = os.getcwd()

SITE = ''
DATABASE = ''
TABLE = ''

commands = {
    'scan': {
        'db': None,
        'tbl': None,
        'site': None,
        'vuln': None
    },
    'dump': {
        'table': None
    },
    'set': {
        'database': None,
        'site': None,
        'table': None
    },
    'show': {
        'database': None,
        'site': None,
        'table': None
    },
    'exit': None,
    'help': None,
    'clear': None,
    'bash': None,
    'banner': None
}
completer = NestedCompleter.from_nested_dict(commands)

style = Style.from_dict({
    # User input (default text).
    '': '#ff0066',

    # Prompt.
    'username': '#FF3D14 bold',
    'at': '#5956EA',
    'pound': '#FF3D14',
    'path': '#3330CC bold',
})

message = [
    ('class:username', USER_LOGIN),
    ('class:at', '@'),
    ('class:path', CURRENT_WORKING_DIRECTORY),
    ('class:pound', '$ '),
]


def execute(shell_cmd):
    print(SIGNALS.load, 'выполнение комманды:', shell_cmd)
    call(shell_cmd, shell=True)


print(BANNER)

try:
    while 1:
        command = prompt(message, style=style, completer=completer)

        if command == 'exit':
            print(SIGNALS.load, 'завершение работы...\n' +
                  SIGNALS.success, 'прощай кулхацкер!')
            break
        elif command == 'clear':
            execute('clear')
        elif command.startswith('set'):
            try:
                if command.split(' ')[-2] == 'database':
                    DATABASE = command.split(' ')[-1]
                elif command.split(' ')[-2] == 'site':
                    SITE = command.split(' ')[-1]
                elif command.split(' ')[-2] == 'table':
                    TABLE = command.split(' ')[-1]
                else:
                    print(SIGNALS.warning, 'неверный синтаксис команды')
            except Exception:
                print(SIGNALS.error, 'ошибка')
        elif command.startswith('show'):
            try:
                if command.split(' ')[-1] == 'database':
                    print(SIGNALS.load, DATABASE)
                elif command.split(' ')[-1] == 'site':
                    print(SIGNALS.load, SITE)
                elif command.split(' ')[-1] == 'table':
                    print(SIGNALS.load, TABLE)
                else:
                    print(SIGNALS.warning, 'неверный синтаксис команды')
            except Exception:
                print(SIGNALS.error, 'ошибка')
        elif command.startswith('scan site'):
            try:
                site = command.split(' ')[-1] if SITE == '' else SITE
                execute(SCAN_SITE.replace('$SITE', site))
            except Exception:
                print(SIGNALS.error, 'ошибка')
        elif command.startswith('scan vuln'):
            try:
                site = command.split(' ')[-1] if SITE == '' else SITE
                execute(SCAN_FOR_VULN.replace('$SITE', site))
            except Exception:
                print(SIGNALS.error, 'ошибка')
        elif command.startswith('scan db'):
            try:
                site = command.split(' ')[-2] if SITE == '' else SITE
                db = command.split(' ')[-1] if DATABASE == '' else DATABASE
                execute(SCAN_FOR_VULN.replace('$SITE', site).replace('$DATABASE', db))
            except Exception:
                print(SIGNALS.error, 'ошибка')
        elif command.startswith('scan tbl'):
            try:
                site = command.split(' ')[-3] if SITE == '' else SITE
                db = command.split(' ')[-2] if DATABASE == '' else DATABASE
                table = command.split(' ')[-1] if TABLE == '' else TABLE
                execute(SCAN_FOR_VULN.replace('$SITE', site).replace('$DATABASE', db).replace('$TABLE', table))
            except Exception:
                print(SIGNALS.error, 'ошибка')
        elif command == 'help':
            print(HELP)
        elif command.startswith('bash'):
            cmd = command.split(' ')[1:]
            execute(cmd)
        elif command == 'banner':
            print(BANNER)
except Exception:
    print(SIGNALS.error, 'завершение работы...')
