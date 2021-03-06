import ACI
import asyncio

connections = {}
LAST = None

usages = {"help": "help",
          "conn": "conn [ip] [port] [name]",
          "lsconn": "lsconn",
          "get": "get [key] [database] [server]",
          "set": "set [key] [database] [value] [server]",
          "exit": "exit",
          "ls": "ls [database] [server]",
          "write": "write [database] [server]",
          "read": "read [database] [server]",
          "test": "test",
          "cdb": "cdb [name]",
          "auth":"auth [id] [token]"}
info = {"help": "Displays help information",
        "conn": "Connects to a new server defaults to [main] 127.0.0.1:8765",
        "lsconn": "Lists all of the currently open connections",
        "get": "Gets a value from the server server name defaults to main",
        "set": "Sets a value on the server server name defaults to main",
        "exit": "Exists the terminal",
        "ls": "Lists all of the values in a database on a server server defaults to main",
        "write": "Writes a database to disk",
        "read": "Reads a database from disk",
        "test": "Runs test code",
        "cdb": "Creates a new Database object. Typically needs to be followed by wctd and wtd",
        "auth":"Authenticates to the ACI Server using the a_auth flow."}


async def _test():
    connections["main"]["db1"]["val"] += "1"


async def _help():
    print("Help")
    print("  Commands:")
    for cmd in usages:
        print("    %s:%s%s%s%s" % (cmd, " " * max(0, 7 - len(cmd)), usages[cmd], " " * max(40 - len(usages[cmd]), 0),
                                   info[cmd]))


async def _connect(ip="127.0.0.1", port=8765, name="main"):
    global connections

    connections[name] = await ACI.async_create(ACI.Client, int(port), ip, name)
    return None


async def _list_connections():
    print("Connections: ")

    if len(connections.values()) == 0:
        print("\tNone")
    else:
        for name in connections:
            print("\t[%s] %s:%i" % (name, connections[name].ip, connections[name].port))


async def _get(key, database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    print("%s:%s[%s] = %s" % (server, database, key, await connections[server][database][key]))


async def _set(key, database, value, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)


    async with connections[server][database] as interface:
        interface[key] = value
    #print("%s:%s[%s] = %s" % (server, database, key, value))


async def _list(database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    result = await connections[server][database].list_databases()
    if len(result) == 0:
        print("\tNone")
    else:
        for data in result:
            print("\t%s" % data)


async def _write(database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    await connections[server][database].write_to_disk()


async def _read(database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    await connections[server][database].read_from_disk()

async def _create_database(db_key, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    await connections[server].create_database(db_key)

async def _authenticate(id, token, server="main"):
    print(await connections[server].authenticate(id, token))


instructions = {"help": _help, "conn": _connect, "lsconn": _list_connections, "get": _get, "set": _set, "ls": _list,
                "write": _write, "read": _read, "test": _test, "cdb": _create_database, "auth":_authenticate}


async def main():
    print("ACI User Terminal\n\n")
    while await instruction() is None:
        pass

    print("Exiting Terminal")
    ACI.stop()


async def exec_instruction(inst, raw_args):
    global instructions

    if inst not in instructions:
        print("Unknown Instruction '%s'" % inst)
        return None

    kwargs = {}
    args = []
    current_arg = ""

    for val in raw_args:
        if val.startswith("-"):
            current_arg = val[1:]
            kwargs[current_arg] = []
        else:
            if current_arg == "":
                args.append(val)
            else:
                kwargs[current_arg].append(val)

    for key in kwargs:
        if len(kwargs[key]) == 1:
            kwargs[key] = kwargs[key][0]
        elif len(kwargs[key]) == 0:
            kwargs[key] = True

    try:
        return await instructions[inst](*args, **kwargs)
    except TypeError as e:
        if e.args[0].startswith(instructions[inst].__name__):
            print("Incorrect Argument Usage")
            print("Correct Usage:", usages[inst])
        else:
            raise e


async def instruction():
    global LAST

    inst = input("$> ")

    if inst == "":
        return
    elif inst == "exit":
        return False

    command, *args = inst.split(" ")

    LAST = await exec_instruction(command, args)


ACI.run(main())
