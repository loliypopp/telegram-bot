import psycopg2 as sql

base = sql.connect(database='onlineshop', user='gaboom', host='localhost', password='0000')
cursor = base.cursor()




class Users:
    ...