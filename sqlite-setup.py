import sqlite3

connect = sqlite3.connect('python-tody_in_history.db')
cursor = connect.cursor()

cursor.execute("""create table if not exists todays(
    date text,
    bigThings text,
    birth text,
)
""")

connect.commit()
connect.close()
