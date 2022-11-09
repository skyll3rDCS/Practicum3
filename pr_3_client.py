import socket
d_ip = '238.123.0.5'
d_port = '2345'
Dbg_mode = False
def setting_IP_port():
    ip_found = False
    port_found = False
    global d_port
    global d_ip
    global Dbg_mode
    v_ip = ''
    while not ip_found:
        if not Dbg_mode:
            v_ip = input('Введите ip, или нажмите Enter('+d_ip+'): ')
        else: v_ip = d_ip
        if v_ip == "":
            v_ip = d_ip
        iw_ip = v_ip.split(".")
        if len(iw_ip) != 4:
            print('Неверное значение')
            continue
        for i in iw_ip:
            if not i.isdigit() or 0 > int(i) or int(i) > 255:
                print('Неверное значение')
                continue
        ip_found = True
        print('IP пользователя введен')
    v_port = ''
    while not port_found:
        if not Dbg_mode:
            v_port = input('Введите порт от 1024 до 65535 или Enter(2345):')
        if v_port == "":
            v_port = d_port
        if v_port.isdigit() and 1024 <= int(v_port) <= 65535:
            v_port = int(v_port)
            port_found = True
        else: print('Неверное значение')
    return v_ip, v_port

IP, port = setting_IP_port()
set_sck = socket.socket()
set_sck.setblocking(1)
set_sck.connect((IP, port))
print('Соединение с сервером: '+IP+'-'+str(port))
while True:
    data = set_sck.recv(1024)
    print('Прием данных от сервера '+IP+':'+str(port)+'-'+data.decode())
    if data.decode() == 'end':
        set_sck.close()
        print('Приостановка соединения с сервером: '+IP+':'+str(port))
        break
    k = input()
    set_sck.send(k.encode())
    print('Отправка данных серверу '+IP+':'+str(port)+'-'+k)
    exit_check = k.lower()
