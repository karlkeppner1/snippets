import cx_Oracle
import json
from collections import namedtuple

def lambda_handler(event, context):
  dsn_tns = cx_Oracle.makedsn('FQDN', 'PORT', service_name='service_name')
  column_names, where_clause = [], []
  database = "database"
  table_name = "table_name"
  with cx_Oracle.connect(user='user', password='password', dsn=dsn_tns, encoding="UTF-8") as connection:
    connection.autocommit = True
    cursor = connection.cursor()
    # Get column_names from schema for table
    cursor.execute(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{table_name}'")
    for row in cursor:
      formatted_row = {}
      raw_row = list(map(str, list(row)))  # ensure all items are treated as strings, remove 'Decimal' for fields in cursor
      for i in range(len(cursor.description)):
        formatted_row[cursor.description[i][0]] = raw_row[i]
      column_names.append(formatted_row['COLUMN_NAME'])
    statement = f"DELETE FROM {database}.{table_name} WHERE "
    for key, value in event['current_pmt_type'].items():
      where_clause.append(f'"{key.upper()}" = \'{value}\'')
    statement = statement + ' AND '.join(where_clause)
    print(statement)
    # Run statement against database
    cursor.execute(statement)
  return 'success'