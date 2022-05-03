import asyncio
import json
import logging
import os
import requests
import websockets
from dotenv import load_dotenv


load_dotenv('.env')
token = os.getenv("my_token")
logger = logging.getLogger(__name__)
data_dict = '{"action":"sub","channel":"alliance:99010987"}'


def send_telegram(text: str):
    url = "https://api.telegram.org/bot"
    channel_id = os.getenv("channel_id")
    url += token
    method = url + "/sendMessage"
    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })
    try:
        if r.status_code != 200:
            raise ValueError
    except ValueError as err:
        logger.error(f"{err}")


async def killmail(data: str):
    uri = "wss://zkillboard.com/websocket/"
    async for websocket in websockets.connect(uri):
        try:
            await websocket.send(data)
            response = await websocket.recv()
            if response:
                response = json.loads(response)
                send_telegram(str(response['url']))
        except websockets.ConnectionClosed:
            continue
        except Exception as err:
            logger.error(f'{err}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a', filename='logs.log')
    while True:
        try:
            asyncio.run(killmail(data=data_dict))
        except Exception as e:
            logger.error(f'{e}')
