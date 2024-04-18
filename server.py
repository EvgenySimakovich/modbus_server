import socket

from pyModbusTCP.server import ModbusServer
from time import sleep

from config import QUANT


server_quantity = QUANT


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



# create an instances of Modbus Server
# server_quantity = int(input('Введите кол-во серверов (N). Сервера будут запущены на портах 10503 и далее: '))
ip_address = get_local_ip()
print(ip_address)

servers = [ModbusServer(
            host=ip_address,
            port=i,
            no_block=True) for i in range(10503, 10503 + server_quantity)]


def main():

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
