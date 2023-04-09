print(5)
print("Result: ")
print("Result: ", 5)
print("Result: ", 5, 7, ".")
print("Result: ", 5, 7, ".", sep="|")
print("Result: ", 5, 7, ".", sep="|", end=" ")#по умолчанию sep=" ", end="\n" 
print("Result: ")
print("Result: \"5\"")
print("Result: \"5\"\t5")
print("Result: \"5\"\t5\ \\")
print(5+2)
print(5*2)
print(5/2)
print(5//2)
print(5**2)
print("Result: ", min(1,4,5,7,-10,0))
print("Result: ", max(1,4,5,7,-10,0))
print("Result: ", abs(-11))
print("Result: ", pow(2,7))#возведение в степень
print("Result: ", round(5/3))#округление числа

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

number = 14#int
print("Result: ", number)
# del(number) #удаляет переменную
# print("Result: ", number)#ошибка
digit = -5.635567#float
print("Result: ", digit)
word = "Hello"#str
print("Result: ", word)
print(word, number)
print(word, digit)
print(digit, number)
boolean = True#or False
print(boolean)
#print(word + boolean)#ошибка
print(word + str(boolean))#превращает иные типы данных в строчный str
print(number + digit)#можно, но вообще говоря не очень правильно с точки зрения практичности
print(word + str(number))
print(word + str(digit))
word2 = "None"
print(word + word2)
print(word + " " + word2)
str_num = "5"
print(number + int(str_num))#способен из строки сделать десятичную цифру
#print(int("abc"))#ошибка, изначально int переводит из системы с основанием 10, но в системе с основанием 10 нет цифр 'a','b','c'
print(int("a", base=16))
print(int("abc", base=16))
print(int("127", base=8))
print(bool(5))
print(bool(0))
print(bool(-1))
#input("Введите число: ")#вводится строка, но не сохраняется

#number1 = input()
#print(number + number1)#ошибка, введенное число на самом деле является строкой, которую нельзя складовать с числами

#print(number + int(number1)) либо 

#number1 = int(input())
#print(number + number1)


print(word2*3)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
