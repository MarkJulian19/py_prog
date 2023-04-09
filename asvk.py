import re
#import time

#start = time.time()
try:
    with open("test8.txt", "r", encoding="utf-8") as input_file:  # Открываем файл на чтение
        input_str = ""
        for line in input_file:
            input_str += line.strip().replace(" ", "")  # Создаем из всего файла одну строку
except Exception as e:
    print(str(e))
    exit()
    
# print(input_str)


def is_correct(input_str):  # Функция определяет является ли файл верным
    # Задаем паттерн строки
    pattern_for_input_str = r"[Вв]ход[\d]+:\{\[(?:(?:\['[A-Z]','[A-Z]'\],)*\['[A-Z]','[A-Z]'\]){0,1}\],\{(?:'[A-Z]':[\d]+,)*'[A-Z]':[\d]+\}\}"
    # Находим все вхождения паттерна строки в файле
    match = re.findall(pattern_for_input_str, input_str)
    # print(match)
    # Проверяем файл на содержание мусора
    if ((len(match) != 1) or (len(match[0]) != len(input_str))):
        return False
    else:
        return True


def parser(input_str):  # функция находит в строке нужные данные и возвращает их
    # считываем список(списков) скток
    tmp_mass = re.findall(r"'[A-Z]','[A-Z]'", input_str)
    mass = list()
    for arr in tmp_mass:        # Проверка на добавление рудиментных связей, лишние просто не добавляются
        tmp_arr = arr.replace("'", "").split(',')
        # не добавляются зеркальные связи, связи вершины самой с собой, связи, которые уже были
        if (tmp_arr not in mass) and ([tmp_arr[1], tmp_arr[0]] not in mass) and (tmp_arr[0] != tmp_arr[1]):
            mass.append(arr.replace("'", "").split(','))

    # считывается список(элементов словаря) строк
    tmp_dict = re.findall(r"'[A-Z]':[\d]+", input_str)
    dictionary = {}
    for dic in tmp_dict:
        m = dic.replace("'", "").split(':')
        if m[0] in dictionary:  # Проверка на добавление уже существующей вершины. Неопределенность!
            # print("Logical error")
            return None, None
        dictionary[m[0]] = int(m[1])

    for i in sum(mass, []):  # проверяет все ли вершины в связях существуют, иначе неопределенность
        if i not in dictionary:
            return None, None

    return sorted(mass), dict(sorted(dictionary.items()))


# удаляет вершину из графа(удаляет все связи с ней и саму вершину из словаря)
def dell_vertex(mass, dictionary, letter):
    d = []
    dictionary.pop(letter)
    for arr in mass:
        if letter not in arr:
            d.append(arr)
    return d


#Идет по группам, и проверяет первую и вторую буквы в группе
#если одна из букв уже есть в группах, то свять полностью добавляется в группу
#если обеих букв в группах нет, то создается новая группа из букв связи
#после каждого прохода удаляются использованные связи
#алгоритм работает пока связи не кончатся
#алгоитм пробегает по вершинам,
#если вершины нет в группах, то она добавляется как отдельная группа
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
    #print(groups)
    return groups


# получает на вход исходный словарь, список групп и удаляемую вершину. возвращает массу удаляемой вершины
def mass_del_vertex(dictionary, groups, letter):
    mass = dictionary[letter]  # добавляем массу удаляемой вершины
    for group in groups:
        tmp_mass = 0
        for vertex in group:
            tmp_mass += dictionary[vertex]  # находим сумму вершин
        mass += tmp_mass**2  # добавляет квадрат суммы вершин группы
    return mass


# основное тело программы
if (is_correct(input_str)):  # если файл имеет синтаксические ошибки, то останавливаемся и выводим ошибку синтаксиса
    mass_of_connections, dictionary = parser(input_str)
    # если файл имеет логические ошибки, то останавливаем и выводим ошибку логики
    if mass_of_connections != None and dictionary != None:
        arr = []  # создаем список масс вершин(вершины в порядке словоря)
        for letter in dictionary:
            # не будем портить исходный словарь, некоторые функции портят исходные данные
            tmp_dictionary = dictionary.copy()
            tmp_mass = list(mass_of_connections)
            # страшная строка, которая по сути выполняет по порядку все нужные нам функции и добавляет массу удаляемой вершины в массив
            arr.append(mass_del_vertex(dictionary, selecting_groups(
                dell_vertex(tmp_mass, tmp_dictionary, letter), tmp_dictionary), letter))
        min_value = (min(arr))  # найдем минимальную массу вершин
        #print(arr)
        w = list(dictionary)  # сделаем словарь исчесляемым
        min_value_vertex = []
        for i in range(len(arr)):
            if arr[i] == min_value:
                min_value_vertex.append(w[i])
        print(str(min_value_vertex))
    else:
        print("Logical error")
else:
    print('Syntax error')


#print(time.time() - start)
