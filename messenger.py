import json
import asyncio

class Messenger:
    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer

    async def read_msg(self):
        length_bytes = await self._reader.readexactly(4)
        msg_length = int.from_bytes(length_bytes, 'big', signed=False)

        msg_bytes = await self._reader.readexactly(msg_length)
        msg_str = msg_bytes.decode()
        return json.loads(msg_str)

    async def write_msg(self, msg):
        msg_str = json.dumps(msg)
        msg_bytes = msg_str.encode()
        length_bytes = len(msg_bytes).to_bytes(4, 'big')
        self._writer.write(length_bytes)
        self._writer.write(msg_bytes)
        await self._writer.drain()

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()

msg_cb = None
async def connect_cb(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Peer connected from {addr}")
    await msg_cb(Messenger(reader, writer))

async def listen(cb, host, port):
    global msg_cb
    msg_cb = cb 
    server = await asyncio.start_server(connect_cb, host, port)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

async def connect(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    return Messenger(reader, writer)
