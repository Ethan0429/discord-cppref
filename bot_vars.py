import os, sys
from dotenv import load_dotenv

if os.path.exists('.env'):
    pass
else:
    with open('.env', 'w') as f:
        f.writelines([
            '# .env\n',
            'DISCORD_TOKEN=\n',
        ])
    print('.env file generated! Exiting bot script.\nFill the appropriate fields in the .env file before running the script again!')
    sys.exit()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
cppref = 'cppreference.com'
man   = 'man7.org/linux/man-pages'
man_alias = 'man7.org'

