
import errno
import socket
from datetime import datetime
import json

d_port = "2345"
Dbg_mode = False

try:
    with open('data_cl.json', 'r', encoding='utf-8') as f:
        l_users = json.load(f)
except:
    l_users = {}
    with open(f'data_cl.json', 'w', encoding='utf-8') as f:
        json.dump(l_users, f, ensure_ascii=False, indent=4)

def path_con(text):
    print(text)
    ct = datetime.now().time()
    with open('path_con.txt', 'a', encoding='utf-8') as f:
        f.write(f'[%d:%d:%d]: ' % (ct.hour, ct.minute, ct.second)+text+'\n')


def launch_port(port):
    t_sckt = None
    try:
        t_sckt = socket.socket()
        t_sckt.bind(("238.123.0.5", port))
        path_con("Запуск сервера на 238.123.0.5:" + str(port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            path_con("Порт "+str(port)+" уже используется, соед. со след.")
            return None
    return t_sckt

def main_serv():
    port_found = False
    global d_port
    global Dbg_mode
    while not port_found:
        if not Dbg_mode:
            v_port = input('Введите порт от 1024 до 65535 или Enter('+d_port+'): ')
        else: v_port = d_port
        if v_port == '':
            v_port = d_port
        if v_port.isdigit() and 1024 <= int(v_port) <= 65535:
            port = int(v_port)
            new_sckt = None
            while new_sckt is None:
                new_sckt = launch_port(port)
                port += 1
            return new_sckt
        else: print("Ошибка при вводе")

cr_sckt = main_serv()
stb = False
while stb is False:
    cr_sckt.listen(1)
    path_con("Прослушивания порта")
    cnnctn, adrss = cr_sckt.accept()
    path_con("Подключение клиента: " + adrss[0] + ":" + str(adrss[1]))
    user = adrss[0]
    user_status = "Не авторизован!"
    while True:
        msg = ''
        if user_status == "Не авторизован!":
            if l_users.get(user) is None:
                cnnctn.send('Вы не зарег-ны. Регистрация: *Имя* *пароль*'.encode())
                data = cnnctn.recv(1024)
                path_con('Данные от клиента '+adrss[0]+':'+str(adrss[1])+'-'+data.decode())
                if not data:
                    break
                inp = data.decode()
                print(inp)
                l_users[user] = {}
                l_users[user]['name'] = inp.split()[0]
                l_users[user]['password'] = inp.split()[1]
                with open(f'db.json', 'w', encoding='utf-8') as f:
                    json.dump(l_users, f, ensure_ascii=False, indent=4)
                cnnctn.send(('Вы зарегистрировались, ' + l_users[user]['name'] + '. Введите данные на отправку').encode())
                user_status = 'Авторизован'
            else:
                cnnctn.send(('Здравствуйте, ' + l_users[user]['name'] + '. Пароль:').encode())
                data = cnnctn.recv(1024)
                path_con('Прием данных от клиента ' + adrss[0] + ':' + str(adrss[1]) + '-' + data.decode())
                if not data:
                    break
                inp = data.decode()
                if l_users[user]['password'] == inp:
                    cnnctn.send(('Вход, ' + l_users[user]['name'] + '. Введите данные на отправку').encode())
                    user_status = 'Авторизован'
        else:
            data = cnnctn.recv(1024)
            path_con('Прием данных от клиента ' + adrss[0] + ':' + str(adrss[1]) + '-' + data.decode())
            if not data:
                break
            inp = data.decode()
            if inp == 'exit':
                cnnctn.send('exit'.encode())
                break
            if inp == 'stop server':
                cnnctn.send('exit'.encode())
                stb = True
                cr_sckt.close()
                path_con('Остановка сервера 238.123.0.5')
                break
            cnnctn.send((inp*2).encode())
            path_con('Отправка данных клиенту' + adrss[0] + ':' + str(adrss[1]) + '-' + inp)
    path_con('Отключение клиента: ' + adrss[0] + '-' + str(adrss[1]))
