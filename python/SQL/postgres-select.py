import psycopg2
import json
from decimal import Decimal

def lambda_handler(event, context):
  result = []
  database = "database"
  table_name = "table_name"
  with psycopg2.connect(host='FQND', database=database, user='user', password='password') as connection:
    cursor = connection.cursor()
    cursor.execute(f'SELECT * from {database}.{table_name}')
    for row in cursor:
      raw_row = list(map(str, list(row)))  # ensure all items are treated as strings, remove 'Decimal' for fields in cursor
      formatted_row = {}
      for i in range(len(cursor.description)):
        formatted_row[cursor.description[i].name] = raw_row[i]
      result.append(formatted_row)
  return result
