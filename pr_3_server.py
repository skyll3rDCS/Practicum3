import os
import socket
import random
import sys
stt = sys.stdout
list_ports = []
Flog = open('logserv.txt', 'w')
sys.stdout = Flog
Fport = open('ports.txt','w')
def Main_Server():
    while True:
        while os.stat('ports.txt').st_size == 0:
            True
        host = ''
        with open('ports.txt', 'r') as pfile:
            lines = pfile.readlines()
            port = int(lines[-1])
        if port not in list_ports:
            list_ports.append(port)
        else:
            while True:
                port = random.randint(1024, 65535)
                if port not in list_ports:
                    list_ports.append(port)
                    pfile = open('ports.txt', 'a+')
                    pfile.write("\n" + str(port))
                    pfile.close()
                    break
        with open('ports.txt', 'r') as pfile:
            lines = pfile.readlines()
            port = int(lines[-1])
        with socket.socket() as sock:
            sock.bind((host, port))
            print('Прослушивание порта: ', port)
            sock.listen()
            conn, addr = sock.accept()
            print('Соединение с клиентом: ', host)
            with conn:
                msg = ''
                while True:
                    data = conn.recv(1024)
                    print('Получение данных', data)
                    if not data:
                        break
                    msg = data.decode()
                    print('Данные отправлены клиенту')
                    conn.send(data)
        print("Отключение клиента")
        choose = input('Нажмите Enter, чтобы продолжить или введите end')
        if choose == 'end':
            break
        else:
            continue
print('Сервер запущен')
Main_Server()
print('Работа сервера приостановлена')
Fport.close()
sys.stdout = stt
Flog.close()
