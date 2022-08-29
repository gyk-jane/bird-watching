"""Connects to an AWS S3 bucket to store the csv file and loads the file to an Aurora MySQL table.

This module contains functions which...
    1. Connects to a pre-existing AWS S3 bucket, created just for this project and stores csv files
    2. ...and loads the csv file from the S3 bucket to an Aurora MySQL table.

"""
import boto3
import os
import inspect
import pymysql
import configparser

def to_bucket(filename, bucket_name):
    """Stores csv file to the specified bucket
    
    Args:
        filename (str): name of the csv file
        bucket_name (str): name of the S3 bucket to connect and store data to

    """
    # Creating the connection
    session = boto3.Session(profile_name='default')
    s3 = session.resource('s3')

    # Storing data
    s3_object = s3.Object(bucket_name, filename).put(Body=open(filename, 'rb'))

    # Delete .csv in local folder
    os.remove(filename)
    
    statement = filename + ' successfully uploaded to ' + bucket_name + '\n'
    print(statement)
    

def connect_to_tables():
    """Connects to Aurora MySQL ebirddata database.
    
    Returns (Cursor): connected cursor to ebirddata
    
    """
    # Get credentials from config.ini
    config = configparser.ConfigParser()
    # DELETEEEE LATER!!!!!!
    config_file_path = r'/Users/janekim/Developer/bird proj/birds/config.ini'
    config.read(config_file_path)

    # Connecting to Aurora MySQL table 'birds'
    host = config.get('mysql', 'host')
    port = config.get('mysql', 'port')
    dbname = config.get('mysql', 'dbname')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    
    db = pymysql.connect(host=host, user=user, port=int(port), passwd=password, db=dbname)
    cursor = db.cursor() 
    
    return cursor   


def to_load(filename, bucket_name, cursor, table_name):
    """Loads csv file to a specified table"""
    # SQL command to load the csv file to the birds table
    load_query = inspect.cleandoc(f"""
                                  LOAD DATA FROM S3 's3://{bucket_name}/{filename}'
                                  INTO TABLE {table_name}
                                  FIELDS TERMINATED BY ';';""")
    cursor.execute(load_query)