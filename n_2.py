import numpy as np

def f(x):
    return 1/(1+np.exp(-x))

def df(x):
    return x*(1-x)

W1 = np.array([[0.8, 0.3], [0.9, 0.3], [0.1, 0.2], [0.05, 0.6]])
W2 = np.array([0.99, 0.3, 0.7, 0.0])

def go_forward(inp):
    sum = np.dot(W1, inp)
    out = np.array([f(x) for x in sum])

    sum = np.dot(W2, out)
    y = f(sum)
    return (y, out)

def train(epoch):
    global W2, W1
    lmd = 0.1          # шаг обучения
    N = 100000       # число итераций при обучении
    count = len(epoch)
    for k in range(N):
        # print(k)
        x = epoch[np.random.randint(0, count)]  # случайных выбор входного сигнала из обучающей выборки
        y, out = go_forward(x[0:2])             # прямой проход по НС и вычисление выходных значений нейронов
        e = y - x[-1]                           # ошибка
        delta = e*df(y)                         # локальный градиент
        W2[0] = W2[0] - lmd * delta * out[0]    # корректировка веса первой связи
        W2[1] = W2[1] - lmd * delta * out[1]    # корректировка веса второй связи
        W2[2] = W2[2] - lmd * delta * out[2]
        W2[3] = W2[3] - lmd * delta * out[3]
        # W2[4] = W2[4] - lmd * delta * out[4]
        # W2[5] = W2[5] - lmd * delta * out[5]
        delta2 = W2*delta*df(out)               # вектор из 2-х величин локальных градиентов
        # print(delta2)
        # корректировка связей первого слоя
        W1[0, :] = W1[0, :] - np.array(x[0:2]) * delta2[0] * lmd
        W1[1, :] = W1[1, :] - np.array(x[0:2]) * delta2[1] * lmd
        W1[2, :] = W1[2, :] - np.array(x[0:2]) * delta2[2] * lmd
        W1[3, :] = W1[3, :] - np.array(x[0:2]) * delta2[3] * lmd
        # W1[4, :] = W1[4, :] - np.array(x[0:2]) * delta2[4] * lmd
        # W1[5, :] = W1[5, :] - np.array(x[0:2]) * delta2[5] * lmd
# обучающая выборка (она же полная выборка)
epoch = [(0, 0, 0),
         (0, 1, 0),
         (1, 0, 0),
         (1, 1, 1)]

train(epoch)        # запуск обучения сети

# проверка полученных результатов
for x in epoch:
    y, out = go_forward(x[0:2])
    print("Выходное значение НС: ", end="")
    if y > 0.1:
        print (1, y, x[-1])
    else:
        print (0, y, x[-1])
print(W1, W2)