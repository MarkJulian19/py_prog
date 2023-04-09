from socket import *
import re


def is_correct(input_str):  
    pattern_for_input_str = r"[Вв]ход[\d]+:\{\[(?:(?:\['[A-Z]','[A-Z]'\],)*\['[A-Z]','[A-Z]'\]){0,1}\],\{(?:'[A-Z]':[\d]+,)*'[A-Z]':[\d]+\}\}"
    match = re.findall(pattern_for_input_str, input_str)
    if ((len(match) != 1) or (len(match[0]) != len(input_str))):
        return False
    else:
        return True


def parser(input_str):

    tmp_mass = re.findall(r"'[A-Z]','[A-Z]'", input_str)
    mass = list()
    for arr in tmp_mass:
        tmp_arr = arr.replace("'", "").split(',')

        if (tmp_arr not in mass) and ([tmp_arr[1], tmp_arr[0]] not in mass) and (tmp_arr[0] != tmp_arr[1]):
            mass.append(arr.replace("'", "").split(','))
    tmp_dict = re.findall(r"'[A-Z]':[\d]+", input_str)
    dictionary = {}
    for dic in tmp_dict:
        m = dic.replace("'", "").split(':')
        if m[0] in dictionary:
            return None, None
        dictionary[m[0]] = int(m[1])
    for i in sum(mass, []):
        if i not in dictionary:
            return None, None
    return sorted(mass), dict(sorted(dictionary.items()))


def dell_vertex(mass, dictionary, letter):
    d = []
    dictionary.pop(letter)
    for arr in mass:
        if letter not in arr:
            d.append(arr)
    return d


def selecting_groups(mass, dictionary):
    groups = []
    while len(mass) != 0:
        dell_arr = []
        for connection in mass:
            flag = -1
            for i in range(len(groups)):
                if connection[0] in groups[i]:
                    flag = 1
                    groups[i].update(set(connection))
                    dell_arr.append(connection)
                    break
            if flag == -1:
                for i in range(len(groups)):
                    if connection[1] in groups[i]:
                        flag = 1
                        groups[i].update(set(connection))
                        dell_arr.append(connection)
                        break
            if flag == -1:
                groups.append(set(connection))
        for dell_connection in dell_arr:
            mass.remove(dell_connection)
    for vertex in dictionary:
        flag1 = -1
        for group in groups:
            if vertex in group:
                flag1 = 1
                break
        if flag1 == -1:
            groups.append(set(vertex))
    print(groups)
    return groups


def mass_del_vertex(dictionary, groups, letter):
    mass = dictionary[letter]
    for group in groups:
        tmp_mass = 0
        for vertex in group:
            tmp_mass += dictionary[vertex]
        mass += tmp_mass**2
    return mass
########################################################################################################


class Server:
    def __init__(self, ip, port):
        print("SERVER IP: ", ip, "\n", "SERVER PORT: ", port, sep='')
        # Создаем AF_INET(интернет сокет с протоколом IPv4)
        # SOCK_STREAM — говорит о том, что в качестве транспортного протокола будет использоваться TCP
        self.ser = socket(AF_INET, SOCK_STREAM)
        # Свяжем хост(любое устройство, предоставляющее сервисы формата «клиент-сервер» в режиме сервера) с сокетом и портом
        self.ser.bind((ip, port))
        print("The server was created on the host:", ip, "and on port:", port)
        # Запустим режим прослушивания для сокета
        self.ser.listen(1)

    def send_msg(self, user, text):
        user.send(text.encode("utf-8"))

    def start_server(self):
        while True:
            # Принимает подключение клиента, запоминаем дресс и сокет клиента
            user, addr = self.ser.accept()
            print(f"CLIENT CONNECTED:\n\tIP: {addr[0]}\n\tPORT: {addr[1]}")
            # Отправим клиенту, что он присоединился и начнем ждать входные данные
            self.listen_user(user)

    def listen_user(self, user):
        # Отправляем клиенту, что он присоединился
        self.send_msg(user, "YOU ARE CONNECTED!")
        # Начинаем слушать клиента, пока тот не отключится
        is_work = True
        while is_work:
            # Пытаемся принять данные от клиента, иначе отключаем его
            try:
                data = user.recv(2048)
                # Приняли данные и отправили клиенту, что все ОК, мы получили данные
                self.send_msg(user, "information received")
                print("information received")
            except Exception as e:
                print(str(e))
                data = ''
                is_work = False
            if len(data) > 0:
                # Декодируем данные
                msg = data.decode("utf-8")
                # Если получили запрос на рассоединение, то закрываем сеанс с клиентом
                if msg == "DISCONNECT":
                    self.send_msg(user, "YOU ARE DISCONNECTED!")
                    user.close()
                    print("CLIENT DISCONNECTED!")
                    is_work = False
                else:
                    # Если мы получили от клиента данные, то обрабатываем их
                    # Если получилось обработать данные, то отправляем ответ, иначе отправляем ошибку
                    print(msg)
                    # Все комментарии по следующим функциям находятся в программе asvk.py
                    ########################################################################################################
                    if (is_correct(msg)):
                        mass_of_connections, dictionary = parser(msg)
                        if mass_of_connections != None and dictionary != None:
                            arr = []
                            for letter in dictionary:
                                tmp_dictionary = dictionary.copy()
                                tmp_mass = list(mass_of_connections)
                                arr.append(mass_del_vertex(dictionary, selecting_groups(
                                    dell_vertex(tmp_mass, tmp_dictionary, letter), tmp_dictionary), letter))
                            min_value = (min(arr))
                            w = list(dictionary)
                            min_value_vertex = []
                            for i in range(len(arr)):
                                if arr[i] == min_value:
                                    min_value_vertex.append(w[i])
                            self.send_msg(user, str(min_value_vertex))
                            print(min_value_vertex)
                    ########################################################################################################
                        else:
                            self.send_msg(user, "Logical error")
                            print("Logical error")
                    else:
                        self.send_msg(user, 'Syntax error')
                        print('Syntax error')
            else:
                print("CLIENT DISCONNECTED!")
                is_work = False


# Запуск сервера
eth0_ip = "0.0.0.0"
Server(eth0_ip, 7777).start_server()
