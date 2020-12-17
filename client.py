import asyncio
import messenger
import argparse

async def main(cmd):
    print('sending...')
    msger = await messenger.connect('127.0.0.1', 8888)
    await msger.write_msg({"cmd": cmd})
    
    resp = await msger.read_msg()
    for line in resp:
        print(line)

parser = argparse.ArgumentParser(description='Play chess.')
parser.add_argument('command', metavar='cmd', type=str, nargs=1,
                    help='chess command')

args = parser.parse_args()
cmd = args.command[0]

asyncio.run(main(cmd))
