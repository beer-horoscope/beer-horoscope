import mysql.connector
import os

from src.training.beer_recs import generate_beer_recs, generate_beer_names, generate_beer_names_tag

HOST=None
PORT=None
DATABASE=None
USER=None
PASSWD=None

def get_beer_recs(beer_names, n):
    return generate_beer_recs(beer_names, n)


def get_beer_names():
    return generate_beer_names()


def get_beer_names_tag(tag):
    return generate_beer_names_tag(tag)


def post_beer_ratings(beer_name, review_overall):
    result = True
    cursor = None
    connection = None

    try:
        populate_env_variables()
        params = (beer_name, review_overall)
        connection = mysql.connector.connect(host=HOST,
                                             port=PORT,
                                             database=DATABASE,
                                             user=USER,
                                             password=PASSWD)
        cursor = connection.cursor()
        cursor.callproc('post_beer_rating', params)
        connection.commit()
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
        result = False
    finally:
        cursor.close()
        connection.close()

    return result

def populate_env_variables():
    global HOST
    global PORT
    global DATABASE
    global USER
    global PASSWD

    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DATABASE = os.getenv('DATABASE')
    USER = os.getenv('USER')
    PASSWD = os.getenv('PASSWORD')
