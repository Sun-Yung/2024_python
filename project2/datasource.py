import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

def get_cities()->list[dict]:
    with psycopg2.connect(database=os.environ['Postgres_DB'],
                      user=os.environ['Postgres_user'],
                      host=os.environ['Postgres_HOST'],
                      password=os.environ['Postgres_password']) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM battery')
            data:list[tuple] = cursor.fetchall()
    
#list comprehension

    convert_data:list[dict] = [{
                            'city':item[1],
                            'dist':item[2],
                            'sitename':item[3],
                            'addresss':item[4],
                            'lat':item[5],
                            'lon':item[6]
                            } for item in data]
    return convert_data