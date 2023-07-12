from pyModbusTCP.server import ModbusServer
from time import sleep
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

IP_ADDRESS = os.getenv('IP_ADDRESS')
# create an instance of Modbus Server
servers = [ModbusServer(IP_ADDRESS, i, no_block=True) for i in range(10503, 10524)]


def main():

    try:
        print('Start server...')
        for server in servers:
            print(f'Server ({server.port}) started')
            server.start()

        print('Modbus server is online')

        val = 1
        while True:
            for server in servers:
                server.data_bank.set_input_registers(address=0,
                                                     word_list=[val for i in range(100)])

            if val == 100:
                val = 0
            val += 1

            sleep(1)

    except:
        print('Shutdown server...')
        for server in servers:
            print(f'Server ({server.port}) stopped')
            server.stop()
        print('Modbus server is offline')


if __name__ == '__main__':
    main()

