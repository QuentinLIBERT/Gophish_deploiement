import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.odoo'))# charge les variables depuis le fichier .env

ODOO_EMAIL = os.getenv('ODOO_EMAIL')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD')
ODOO_DB = os.getenv('ODOO_DB_NAME')
ODOO_PORT = int(os.getenv('ODOO_PORT'))
ODOO_HOST = os.getenv('ODOO_HOST')
