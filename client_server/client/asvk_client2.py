import requests
#будем отправлять запросы серверу и распечатывать текст сообщений
for i in range(1,9):
    print(requests.get(f'http://localhost:7777/test{i}.txt').text)


