import os
from pyairtable import Table, Api
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
api = Api(API_KEY)
base = api.base(BASE_ID)
table_clientes = base.table("CLIENTES")

print(table_clientes.schema())
