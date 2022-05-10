import threading

from Source.Modbus.Modbus import *
from Source.Storage.Database import Database
from Source.Storage.Json import Json


def main():
    # Create the storage
    if DB:
        storage = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    else:
        storage = Json(JSON_PATH, JSON)

    modbus_tcp = Modbus(storage)

    modbus_tcp.bind(socket.gethostbyname(socket.gethostname()), 501)
    modbus_tcp.listen(5)

    print("[LISTENING]\n")

    while True:
        try:
            connection, address = modbus_tcp.accept()
            print(f"[CONNECTED TO {address[0]}]\n")
        except Exception as e:
            print(e)
            print("Socket closed!")
            break

        try:
            threading.Thread(target=modbus_tcp.receive, args=(connection, address)).start()
        except Exception as e:
            print(e)
            print(f"Error to make a connection to {address[0]}")


if __name__ == '__main__':
    main()
