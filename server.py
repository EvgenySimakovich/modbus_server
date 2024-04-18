import socket

import click
from pyModbusTCP.server import ModbusServer
from time import sleep


def get_local_ip() -> str:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    host_info = socket.gethostbyname_ex(hostname)
    (host_name,
     list_of_aliases,
     list_of_IP_addresses) = host_info
    if len(list_of_IP_addresses) > 1:
        remote_ip = list_of_IP_addresses[1]
        return remote_ip
    else:
        return local_ip


def create_servers(count_of_servers) -> list[ModbusServer]:
    # create an instances of Modbus Server
    ip_address = get_local_ip()

    list_of_servers = [ModbusServer(
        host=ip_address,
        port=i,
        no_block=True) for i in range(10503, 10503 + count_of_servers)]

    return list_of_servers


@click.command()
@click.option("--count", default=1, help="Number of Slaves")
def main(count):
    servers = create_servers(count_of_servers=count)
    print(servers)
    try:
        print('Start servers...')
        for server in servers:
            server.start()
            if server.is_run:
                print(f'Server started. Port: {server.port}. Data blank: {server.data_bank}')
        print('Modbus servers are online')

        val = 1
        while True:
            for server in servers:
                server.data_bank.set_input_registers(address=0,
                                                     word_list=[val for _ in range(500)])
                server.data_bank.set_holding_registers(address=0,
                                                       word_list=[val for _ in range(500)])

            print(f'Set value {val} to INPUT and HOLDING registers')
            if val == 100:
                val = 0
            val += 1

            sleep(1)

    except Exception as ex:
        print('Shutdown server...')
        print(ex)
        for server in servers:
            print(f'Server ({server.port}) stopped')
            server.stop()
        print('Modbus server is offline')


if __name__ == '__main__':
    main()
