import os
import sys
import psycopg2
import time

def main():
  uri = "host='{}' dbname='{}' user='{}' password='{}'".format(
    os.getenv('POSTGRES_HOST'),
    os.getenv('POSTGRES_DB'),
    os.getenv('POSTGRES_USER'),
    os.getenv('POSTGRES_PASSWORD'),
  )
  conn = connect(uri)
  if conn is None:
    sys.exit(1)

def connect(uri: str, retries: int = 15):
  conn = None
  while conn is None:
    print('trying to connect: {}...'.format(uri))
    try:
      conn = psycopg2.connect(uri)
    except psycopg2.OperationalError:
      if retries == 0:
        return None
      time.sleep(1)
      retries = retries - 1
  return conn

if __name__ == "__main__":
    main()