
from app import app, api
import concurrent.futures
import threading
from flask_script import Manager, Server

from app.forex import forexInitializeMethod


if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(forexInitializeMethod())
        executor.submit(app.run())