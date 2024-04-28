import time
import Recommend
import bot_cfrec
import myapp
import threading
import asyncio

def main():
	server_thread = threading.Thread(target=myapp.start_server)
	server_thread.start()
	bot_cfrec.start_bot()

if __name__ == '__main__':
    main()
