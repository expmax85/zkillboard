import json
import os
from config import token, bot_url, bot_command, url_socket

import requests
import websockets

from bot import logger


def send_telegram(text: str):
    url = bot_url
    channel_id = os.getenv("channel_id")
    url += token
    method = url + bot_command
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
    uri = url_socket
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
