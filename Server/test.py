import ACI
import time
import asyncio
import threading

def test():
    database = ACI.create(ACI.Client, 8765, "127.0.0.1", "main")
    time.sleep(1)
    print(database["TicTac"]["numGames"])

threading.Thread(target=test, daemon=False).start()