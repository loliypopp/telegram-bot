import psycopg2 as sql
import aiogram

base = sql.connect(database='onlineshopp', 
                   user='gaboom', 
                   host='localhost', 
                   password='0000')
cursor = base.cursor()

