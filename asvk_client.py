from socket import *

#Считывает файл для дальнейшей отправки и возвращает строку
def open_file(num_file):
    base_of_files = ["test1.txt","test2.txt","test3.txt","test4.txt","test5.txt"]
    print("Input file:")
    input_file = open(base_of_files[num_file-1], "r")
    input_str = ""
    for line in input_file:
        input_str += line.strip().replace(" ", "")
        print(line, end="")
    print("\n")
    input_file.close()
    return input_str

class Client:
    def __init__(self, ip, port):
        # Создаем AF_INET(интернет сокет с протоколом IPv4)
        # SOCK_STREAM — говорит о том, что в качестве транспортного протокола будет использоваться TCP
        self.cli = socket(AF_INET, SOCK_STREAM)
        #Пытаемся присоединиться к серверу
        self.cli.connect((ip, port))
        self.connect_client()
        
    def connect_client(self):
        #Для подсоединения необходимо, чтобы сервер отправил клиенту YOU ARE CONNECTED!
        #Если все ОК, то продолжаем, иначе заканчиваем работу клиента
        try:
            msg = self.cli.recv(2048).decode("utf-8")
            print(msg)
        except Exception as e:
            print("ERROR:", str(e))
            exit()
        if msg == "YOU ARE CONNECTED!":
            self.listen_ser()
        else:
            exit()

    #Отправляет данные на сервер до тех пор пока не получит информацию о доставке информации
    def sender(self, text):
        self.cli.send(text.encode("utf-8"))
        while self.cli.recv(2048).decode("utf-8") != "DATA IS GETED":
            self.cli.send(text.encode("utf-8"))
        print("DATA SENT")

    def listen_ser(self):
        is_work = True
        while is_work:
            #Принимает команду от пользователя
            req = input("You have 5 files from 1 to 5, enter the input file number or 'DISCONNECT': ")
            #Обрабатывает команду, в случае ошибки возвращает ошибку
            if req:
                if req == "DISCONNECT":
                    self.sender(req)
                    print(self.cli.recv(2048).decode("utf-8"))
                    exit()
                else:
                    try:
                        if 1<=int(req)<=5:
                            self.sender(open_file(int(req)))
                            print("Answer is: ", self.cli.recv(2048).decode("utf-8"))
                        else:
                            print('Incorrect data, try again')
                    except Exception as e:
                        print(e)
                        print("Incorrect data, try again")
            else:   
                print("Incorrect data, try again")

#Ввод данных для подключения к серверу и подключение к серверу
# ip = input("Type server IP: ")
ip = "172.17.0.2"
# port = int(input("Type server PORT: "))
port = "7777"
Client(ip, port)
