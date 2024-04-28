import bot_cfrec
import threading
import sqlite3
import os

def start_flask():
	os.system("flask run")


def main():
	con = sqlite3.connect("users.db")
	cursor = con.cursor()
	
	find_table = """
SELECT *
FROM sqlite_master
WHERE type='table' AND NAME='cf_users'
"""
	cursor.execute(find_table)
	if cursor.fetchone() == None:
		create_table = """
CREATE TABLE cf_users (
	handle varchar(255) UNIQUE,
	discord_id varchar(255) UNIQUE,
	pauth_id varchar(255) UNIQUE
)
"""
		cursor.execute(create_table)
		con.commit()
	
	flask_thread = threading.Thread(target=start_flask)
	flask_thread.start()

	bot_cfrec.start_bot()

if __name__ == '__main__':
	main()

