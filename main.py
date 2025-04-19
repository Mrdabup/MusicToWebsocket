import os
import json
import websockets
import asyncio
from websockets import serve
import requests

#import re: We don't need this right now

# Variable init 
appVer = 0
key = 'null'

# Websocket Config
HOST = "localhost"
PORT = 8081
wsClients = set()

# YTDM CONFIG
appId = "tojg"
code = '0000'
ytdm_baseUrl = "http://localhost:9863"
ytdm_apiBase = ytdm_baseUrl + "/api/v1"

ytdmJsonConfig = {
    "appId":  appId,
    "appName": "ytmToWeb",
    "appVersion": "0.0.1"
}


# THYTM CONFIG
thytm_baseUrl = "http://localhost:26538/api/v1"
thytm_statusUrl = thytm_baseUrl + '/song'

# JSON config for the app
importantJson = {
    "appVer": appVer,
    "key": key
}

# YTDM Logic

def ytdm_getAuth():
    print("Getting Auth...")


# th-ch's YTM Logic

def thYtm_getStatus():
    print("ass")

# Websocket Logic
async def broadcastMusicStatus():
    while True:
        thch_status = requests.get(thytm_statusUrl)
        print(thch_status.json())
        for clients in wsClients:
            try:
                await clients.send(thch_status.json())
            except:
                print("ERROR ON SENDING MESSAGES!")
        await asyncio.sleep(3)


async def websocketMessages(websocket):
    print("Client connected")
    async for message in websocket:
        await websocket.send(message)
    print("Client disconnected")

async def websocketMain():
    print(f"Hello! Hosting at:\nws://{HOST}:{PORT}")
    wsServer = await websockets.serve(websocketMessages, HOST, PORT)
    await asyncio.gather(broadcastMusicStatus())
#    async with serve(broadcastMusicStatus, host, port) as server:
#        await server.serve_forever()

if __name__ == "__main__":
    if(os.path.exists("key.json")):
        print("Skipping some stuff...")
    # If we find key.json, we load it into memory and execute the program
    print("Hello World!")
    appVer = input("Please enter a number for the following:\n1. th-ch's YoutubeMusic\n2. YTMDesktop\n")
    if appVer == "1":
        print("ughh")
        #thytm_status()
        asyncio.run(websocketMain())
    elif appVer == "2":
        print("yay")
    else:
        print("Who the fuck asked? Go to github and open an issue!") # Just thought this was funny - Jckl
        exit