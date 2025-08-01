import os
import json
import websockets
import asyncio
from websockets import serve
import requests
from ytmd_sdk import Events, YTMD, Parser

# Websocket Config
HOST = "localhost"
PORT = 8080
wsClients = set()

# YTMD Config
ytmd = YTMD("tojg", "MusicToWebsocket", "1.0.0")

# THYTM Config
thytm_baseUrl = "http://localhost:26538/api/v1"
thytm_statusUrl = thytm_baseUrl + '/song'

# EddyAPI Config
eddy_baseUrl = "http://localhost:3665"
eddy_statusUrl = eddy_baseUrl + "/now-playing"

# YTDM Logic
def ytdm_logic():
    key = ytmd.authenticate()

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
            ads = "False"
            formattedData = f"{song_name} - {author}|{videoProgress}|{duration}|{ads}"
            print(formattedData)
            await asyncio.sleep(.1)
        if appVer == "2":
           ytdm_status = ytmd.get_state()
           ytdm_statusJson = ytdm_status.json()
           song_name = ytdm_statusJson["video"]["title"]
           author = ytdm_statusJson["video"]["author"]
           videoProgress = int(ytdm_statusJson["player"]["videoProgress"])
           duration = int(ytdm_statusJson["video"]["durationSeconds"])
           ads = bool(ytdm_statusJson["player"]["adPlaying"])
           formattedData = f"{song_name} - {author}|{videoProgress}|{duration}|{ads}"
           print(formattedData)
           await asyncio.sleep(5)
        if appVer == "3":
            eddyStatus = requests.get(eddy_statusUrl)
            eddyStatusJson = eddyStatus.json()
            song_name = eddyStatusJson["item"]["title"]
            authorNames = eddyStatusJson.get("item", {}).get("artists", {})
            authorNameList = [names['name'] for names in authorNames]
            if len(authorNameList) == 1:
                author = authorNameList[0]
                print(author)
            elif len(authorNameList)== 2:
                author = (" & ".join(authorNameList))
                print(author)
            else:
                author = (", ".join(authorNameList[:-1]) + " & " + authorNameList[-1])
                print(author)
            author = author
            videoProgress = int(eddyStatusJson["position"])
            duration = int(eddyStatusJson["duration"])
            ads = "false"
            formattedData = f"{song_name} - {author}|{videoProgress}|{duration}|{ads}"
            print(formattedData)
            await asyncio.sleep(2)
        for clients in wsClients:
            try:
                await clients.send(formattedData)
            except:
                print("ERROR ON SENDING MESSAGE! CLIENT DROPPED BEFORE RECIVING MESSAGE!")
# If ads are programmed to be false, it might be because A: There's no function to detect it or B: It's a subscription service (like Tidal or YTM Premium)


async def websocketMessages(websocket):
    print("Client connected")
    wsClients.add(websocket)
    async for message in websocket:
        await websocket.send(message)
    wsClients.remove(websocket)
    print("Client disconnected")

async def websocketMain():
    print(f"Hello! Hosting at:\nws://{HOST}:{PORT}")
    wsServer = await websockets.serve(websocketMessages, HOST, PORT)
    await asyncio.gather(broadcastMusicStatus())

if __name__ == "__main__":
    if(os.path.exists("key.json")):
        print("Skipping some stuff...")
    # TODO: If we find key.json, we load it into memory and execute the program
    print("Hello World!")
    appVer = input("Please enter a number for the following:\n\n1. th-ch's YoutubeMusic\n2. YTMDesktop\n3. TIDAL via TIDALuna and eddyapi\n\nYour Choice: ")
    if appVer == "1":
        asyncio.run(websocketMain())
    if appVer == "2":
        ytdm_logic()
        print("FOR THE TIME BEING: I haven't done the key implementation, so you must remove the companion and enable authorization again once you exit out of this program!")
        asyncio.run(websocketMain())
    if appVer == "3":
        asyncio.run(websocketMain())    
    else:
        print("This isn't a valid request... Go to github and open an issue!")
        exit


if appVer == "2":
    ytmd.connect()