from http.server import BaseHTTPRequestHandler, HTTPServer
import re


def open_file(file_name):
    input_file = open(file_name, "r")
    input_str = ""
    for line in input_file:
        input_str += line.strip().replace(" ", "")
    input_file.close()
    return input_str

# функции алгоритма
################################################################################################
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
    # print(groups)
    return groups


def mass_del_vertex(dictionary, groups, letter):
    mass = dictionary[letter]
    for group in groups:
        tmp_mass = 0
        for vertex in group:
            tmp_mass += dictionary[vertex]
        mass += tmp_mass**2
    return mass
################################################################################################


# собственный обработчик запросов
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text')
        self.end_headers()
################################################################################################
        input_str = open_file(self.path[1:])
        mass_of_connections, dictionary = parser(input_str)
        if mass_of_connections != None and dictionary != None:
            arr = []
            for letter in dictionary:
                tmp_dictionary = dictionary.copy()
                tmp_mass = list(mass_of_connections)
                arr.append(mass_del_vertex(dictionary, selecting_groups(
                    dell_vertex(tmp_mass, tmp_dictionary, letter), tmp_dictionary), letter))
        min_value = (min(arr))
        # print(arr)
        w = list(dictionary)
        min_value_vertex = []
        for i in range(len(arr)):
            if arr[i] == min_value:
                min_value_vertex.append(w[i])
        # print(str(min_value_vertex))
################################################################################################
        self.wfile.write(str(min_value_vertex).encode("utf-8"))


def run():
    server_address = ('', 7777)
    try:
        # запускает сервер
        http = HTTPServer(server_address, Handler)
        print('Starting server...')
        http.serve_forever()
    except Exception:
        http.shutdown()


run()
