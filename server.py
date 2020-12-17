import asyncio
import messenger

board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ['P'] * 8,
        [' '] * 8,
        [' '] * 8,
        [' '] * 8,
        [' '] * 8,
        ['p'] * 8,
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]

async def connect_cb(msger):
    request = await msger.read_msg()
    print(f'received: {request}')
    cmd = request['cmd']

    if cmd == 'show':
        await msger.write_msg(board)
    elif cmd == 'move':
        start = request['start']
        end = request['end']

    print("Close the connection")
    await msger.close()

async def main():
    await messenger.listen(connect_cb, '127.0.0.1', 8888)

asyncio.run(main())
