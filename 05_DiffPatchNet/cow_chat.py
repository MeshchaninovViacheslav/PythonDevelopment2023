import asyncio
import shlex
from cowsay import cowsay, list_cows

clients = {}


async def cow_chat(reader, writer):
    # Tasks initialization
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())  # update send task
                command = shlex.split(q.result().decode().strip())  # get command line

                # analyse cases
                if not command:
                    continue
                if command[0] == "login":
                    if len(command) < 2:
                        break
                    if command[1] not in list_cows():
                        writer.write(f"This is not a cow name\n".encode())
                        await writer.drain()
                    elif command[1] in clients:
                        writer.write(f"This name is taken\n".encode())
                        await writer.drain()
                    else:
                        clients[command[1]] = clients.pop(me)
                        me = command[1]
                        writer.write(f"Successful login\n".encode())
                        await writer.drain()

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    # Tasks close
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    # The client_connected_cb callback is called whenever a new client connection is established.
    # It receives a (reader, writer) pair as two arguments, instances of the StreamReader and StreamWriter classes.
    server = await asyncio.start_server(client_connected_cb=cow_chat, host='0.0.0.0', port=1337)
    async with server:
        await server.serve_forever()  # Start accepting connections until the coroutine is cancelled.


asyncio.run(main())
