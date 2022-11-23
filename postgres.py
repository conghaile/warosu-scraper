import psycopg2
from config import config

def connect():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def verifyTable():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS Warosu (number varchar(100) primary key, subject varchar(500), text varchar(5000), time varchar(500))')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def create(post, table):
    postnum = post.number
    if post.subject == '':
        sub = 'none'
    else:
        sub = post.subject.replace("'", "''")
    text = '##'.join(post.text).replace("'", "''")
    time = post.time

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        
        cur = conn.cursor()
        query = '''INSERT INTO %s(number, subject, text, time) VALUES('%s', '%s', '%s', '%s')''' % (table,  postnum, sub, text, time)
        cur.execute(query)
        print("Success!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    

