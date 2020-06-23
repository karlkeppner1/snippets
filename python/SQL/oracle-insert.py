import cx_Oracle
import json
from collections import namedtuple

def lambda_handler(event, context):
  dsn_tns = cx_Oracle.makedsn('FQDN', 'PORT', service_name='service_name')
  column_names, columns, variables, values = [], [], [], {}
  database = "database"
  table_name = "table_name"
  with cx_Oracle.connect(user='user', password='password', dsn=dsn_tns, encoding="UTF-8") as connection:
    connection.autocommit = True
    cursor = connection.cursor()
    # Get column names from schema for table
    cursor.execute(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{table_name}'")
    for row in cursor:
      formatted_row = {}
      raw_row = list(map(str, list(row)))  # ensure all items are treated as strings, remove 'Decimal' for fields in cursor
      for i in range(len(cursor.description)):
        formatted_row[cursor.description[i][0]] = raw_row[i]
      column_names.append(formatted_row['COLUMN_NAME'])
    # Create Insert Statement
    for column in column_names:
      if column.lower() in event:  # check if particular column is passed in from GraphQL
        variables.append(f':{column}')  # variables are column names prepepended with a :
        columns.append(column)
        values[column] = f'{event[column.lower()]}'  # create dict of column:value, need to wrap the values in quotes
    statement = f"INSERT INTO {database}.{table_name} ({', '.join(columns)}) VALUES ({', '.join(variables)})"
    # Run statement against database
    cursor.execute(statement, values)
  return 'success'
