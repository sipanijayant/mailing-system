import psycopg2

conn = psycopg2.connect("dbname=Gmail user=sample password=sample")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS users,mails,folders")
cur.execute("""CREATE TABLE users (
            username varchar(30) PRIMARY KEY NOT NULL,
            first_name varchar(30),
            last_name varchar(30),
            password varchar(30) NOT NULL
            );""")
cur.execute("""CREATE TABLE mails (
            id serial primary key,
            fromId varchar(30) NOT NULL,
            toId varchar(30) NOT NULL,
            subject varchar(200),
            body varchar(2000)
            );""")
cur.execute("""CREATE TABLE folders (
            id serial primary key,
            name varchar(100),
            owner varchar(30),
            emails varchar(200)
            );""")
conn.commit()
cur.close()
conn.close()
