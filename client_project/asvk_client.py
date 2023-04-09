from socket import *

# Считывает файл для дальнейшей отправки и возвращает строку


def open_file(num_file):
    base_of_files = ["test1.txt",
                     "test2.txt",
                     "test3.txt",
                     "test4.txt",
                     "test5.txt",
                     "test6.txt",
                     "test7.txt",
                     "test8.txt",
                     "DISCONNECT"]
    if base_of_files[num_file] == "DISCONNECT":
        return "DISCONNECT"
    else:
        input_file = open(base_of_files[num_file], "r")
        input_str = ""
        for line in input_file:
            input_str += line.strip().replace(" ", "")
        input_file.close()
        return input_str


class Client:
    def __init__(self, ip, port):
        # Создаем AF_INET(интернет сокет с протоколом IPv4)
        # SOCK_STREAM — говорит о том, что в качестве транспортного протокола будет использоваться TCP
        self.cli = socket(AF_INET, SOCK_STREAM)
        # Пытаемся присоединиться к серверу
        self.cli.connect((ip, port))
        self.connect_client()

    def connect_client(self):
        # Для подсоединения необходимо, чтобы сервер отправил клиенту YOU ARE CONNECTED!
        # Если все ОК, то продолжаем, иначе заканчиваем работу клиента
        try:
            msg = self.cli.recv(2048).decode("utf-8")
        except Exception as e:
            exit()
        if msg == "YOU ARE CONNECTED!":
            self.listen_ser()
        else:
            exit()

    # Отправляет данные на сервер до тех пор пока не получит информацию о доставке информации
    def sender(self, text):
        self.cli.send(text.encode("utf-8"))
        self.cli.recv(2048).decode("utf-8") != "information received"

    def listen_ser(self):
        is_work = True
        k = 0
        while is_work:
            # Принимает команду от пользователя
            req = open_file(k)
            # Обрабатывает команду, в случае ошибки возвращает ошибку
            if req == "DISCONNECT":
                self.sender(req)
                self.cli.recv(2048).decode("utf-8")
                exit()
            else:
                if 0 <= k <= 8:
                    self.sender(req)
                    k += 1
                    print(self.cli.recv(2048).decode("utf-8"))


# Ввод данных для подключения к серверу и подключение к серверу
ip = "172.17.0.2"
port = 7777
Client(ip, port)
