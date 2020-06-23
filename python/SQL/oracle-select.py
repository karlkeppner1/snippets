import cx_Oracle
import json
from collections import namedtuple

def lambda_handler(event, context):
  result = []
  dsn_tns = cx_Oracle.makedsn('FQDN', 'PORT', service_name='service_name')
  database = "database"
  table_name = "table_name"
  with cx_Oracle.connect(user='user', password='password', dsn=dsn_tns, encoding="UTF-8") as connection:
    cursor = connection.cursor()
    cursor.execute(f'select * from {database}.{table_name}')
    for row in cursor:
      formatted_row = {}
      raw_row = list(map(str, list(row)))  # ensure all items are treated as strings, remove 'Decimal' for fields in cursor
      for i in range(len(cursor.description)):
        formatted_row[cursor.description[i][0].lower()] = raw_row[i]
      result.append(formatted_row)
  return result
