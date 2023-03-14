import asyncio
import shlex
from cowsay import cowsay, list_cows

clients = {}


async def awriter(writer, message):
    writer.write(message.encode())
    await writer.drain()


async def cow_chat(reader, writer):
    # Tasks initialization
    me = "{}:{}".format(*writer.get_extra_info('peername'))
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
                        await awriter(writer, f"This is not a cow name\n")
                    elif command[1] in clients:
                        await awriter(writer, f"This name is taken\n")
                    else:
                        clients[command[1]] = clients.pop(me)
                        me = command[1]
                        await awriter(writer, f"Successful login\n")
                if command[0] == "who":
                    await awriter(writer, f"Online users: {[cow for cow in clients if cow in list_cows()]}\n")
                if command[0] == "cows":
                    await awriter(writer, f"Available cows: {[cow for cow in list_cows() if cow not in clients]}\n")
                if command[0] == "quit":
                    break
                if command[0] == "say":
                    if me in list_cows():
                        if len(command) < 3:
                            break
                        if command[1] in clients and command[1] in list_cows():
                            await clients[command[1]].put(cowsay(command[2], cow=me))
                    else:
                        await awriter(writer, f"First login\n")
                if command[0] == "yield":
                    if me in list_cows():
                        if len(command) < 2:
                            break
                        for name in clients:
                            if name in list_cows() and name != me:
                                await clients[name].put(cowsay(command[1], cow=me))
                    else:
                        await awriter(writer, f"First login\n")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    # Tasks close
    send.cancel()
    receive.cancel()
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(client_connected_cb=cow_chat, host='0.0.0.0', port=1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
