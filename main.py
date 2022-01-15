# -*- coding: utf-8 -*-
# Author: Vladimir Pichugin <vladimir@pichug.in>
import configparser
import asyncio
import threading
import telnetlib3

config = configparser.ConfigParser()
config.read('settings.ini')


@asyncio.coroutine
def shell(reader, writer):
    while True:
        outp = yield from reader.read(1024)
        if not outp:
            break  # End of File
        elif 'Dlink-Router login:' in outp:
            writer.write(config.get('Router', 'Login') + '\r')
        elif 'Password:' in outp:
            writer.write(config.get('Router', 'Password') + '\n')
            print('Logged in.')
        elif 'Enter \'help\' for a list of built-in commands.' in outp:
            writer.write('reboot' + '\n')
            print('Reboot.')
            break

        print(outp, flush=True)


def run_threaded(name, func):
    job_thread = threading.Thread(target=func)
    job_thread.setName(f'{name}Thread')
    job_thread.start()


def reboot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    coro = telnetlib3.open_connection(
        host=str(config.get('Router', 'Host')),
        port=int(config.get('Router', 'Port')),
        shell=shell
    )

    reader, writer = loop.run_until_complete(coro)
    loop.run_until_complete(writer.protocol.waiter_closed)
