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
PORT = 8080
wsClients = set()

# YTDM CONFIG
appId = "tojg"
ytdm_baseUrl = "http://localhost:9863"
ytdm_apiBase = ytdm_baseUrl + "/api/v1"
ytdm_authRequest = ytdm_baseUrl + "/auth/request"

# THYTM CONFIG
thytm_baseUrl = "http://localhost:26538/api/v1"
thytm_statusUrl = thytm_baseUrl + '/song'

# JSON config for the py app
importantJson = {
    "appVer": appVer,
    "key": key
}

# YTDM Logic

def ytdm_getAuth():
    print("Getting Auth...")

# Websocket Logic
async def broadcastMusicStatus():
    while True:
        global appVer
        if appVer == "1":
            thch_status = requests.get(thytm_statusUrl)
            thchStatusJson = thch_status.json()
            song_name = thchStatusJson['alternativeTitle']
            author = thchStatusJson['artist']
            videoProgress = int(thchStatusJson['elapsedSeconds'])
            duration = int(thchStatusJson['songDuration'])
            ads = "False" # Keep this false! This bool is only used in YTMD but is here for sake of not breaking 
            formattedData = f"{song_name} - {author}|{videoProgress}|{duration}|{ads}"
            print(formattedData)
        else:
            formattedData = f"Sorry mate! We are working on one thing..."
        for clients in wsClients:
            try:
                await clients.send(formattedData)
            except:
                print("ERROR ON SENDING MESSAGE! CLIENT DROPPED BEFORE RECIVING MESSAGE!")
        await asyncio.sleep(5) # YTDM only allows clients to look at its API every 5 seconds, so it limits thch.


async def websocketMessages(websocket):
    print("Client connected")
    wsClients.add(websocket)
    # Stupid me forgot to add the client to the set
    async for message in websocket:
        await websocket.send(message)
    wsClients.remove(websocket)
    # Also stupid me forgot to remove the client
    print("Client disconnected")

async def websocketMain():
    print(f"Hello! Hosting at:\nws://{HOST}:{PORT}")
    wsServer = await websockets.serve(websocketMessages, HOST, PORT)
    await asyncio.gather(broadcastMusicStatus())

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
        asyncio.run(websocketMain())
    else:
        print("Who the fuck asked? Go to github and open an issue!") # Just thought this was funny - Jckl
        exit