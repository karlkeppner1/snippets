import psycopg2
import json
from decimal import Decimal

def lambda_handler(event, context):
  column_names, where_clause = [], []
  database = "database"
  table_name = "table_name"
  with psycopg2.connect(host='FQND', database=database, user='user', password='password') as connection:
    cursor = connection.cursor()
    # Get column names from schema for table
    cursor.execute(f"SELECT COLUMN_NAME FROM	information_schema.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    for row in cursor:
      formatted_row = {}
      raw_row = list(map(str, list(row)))  # ensure all items are treated as strings, remove 'Decimal' for fields in cursor
      for i in range(len(cursor.description)):
        formatted_row[cursor.description[i][0]] = raw_row[i]
      column_names.append(formatted_row['column_name'])
    # Create Insert Statement
    statement = f"DELETE FROM {database}.{table_name} WHERE "
    for key, value in event['current_pmt_type'].items():
      where_clause.append(f'"{key}" = \'{value}\'')
    statement = statement + ' AND '.join(where_clause)
    print(statement)
    # Run statement against database
    cursor.execute(statement)
  return cursor.statusmessage
