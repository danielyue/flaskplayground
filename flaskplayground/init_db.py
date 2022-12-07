import mysql.connector
import dotenv

with open('flaskplayground/secrets.json') as f:
    secrets = json.load(f)

connection = mysql.connector.connect(
    host=secrets["HOST"],
    user=secrets["USER"],
    password=secrets["PASSWORD"],
    database='flask_playground'
)

with open('schema.sql') as f:
    res = connection.cmd_query_iter(f.read())
    outcomes = [x for x in res]

cur = connection.cursor()
insert_stmt = "INSERT INTO posts (title, content) VALUES (%s, %s)"
first_post = ('First Post', 'Content for the first post')
second_post = ('Second Post', 'Content for the second post')
cur.execute(insert_stmt, first_post)
cur.execute(insert_stmt, second_post)
connection.commit()
connection.close()
