import glob
import os

import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def create_database(database_name: str):
    # connexion to default database 'postgres'
    conn = psycopg2.connect(host='127.0.01', user='postgres', dbname='postgres', password='CHiheb 10')
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create new database
    drop_query = f"DROP DATABASE IF EXISTS {database_name}"
    cur.execute(drop_query)
    create_query = f"CREATE DATABASE {database_name} with ENCODING 'utf8' TEMPLATE template0 "
    cur.execute(create_query)

    # close connexion to default database
    cur.close()
    conn.close()

    # connexion to new databse
    conn = psycopg2.connect(host='127.0.0.1', user='postgres', dbname=database_name, password='CHiheb 10')
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    return conn, cur


def find_csv_files(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root, '*.csv'))
        for file in files:
            all_files.append(os.path.abspath(file))
    print('{} csv files are found in {}'.format(len(all_files), path))
    return all_files


def file_2_table(files, database_name):
    conn_string = f'postgresql://postgres:CHiheb 10@localhost:5432/{database_name}'
    engine = create_engine(conn_string)
    conn = engine.connect()
    for f in files:
        name = f.split('/')[-1].split('.')[0]
        data = pd.read_csv(f)
        data.to_sql(name, con=conn, if_exists='replace', index=False)
    conn.close()


if __name__ == '__main__':
    conn, cur = create_database('olympics')
    path = '/home/chiheb/PycharmProjects/portfolio/sql_project/data'
    all_files = find_csv_files(path)
    file_2_table(all_files, 'olympics')
