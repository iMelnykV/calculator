import math
import json
import os
import datetime
# import requests
from pprint import pprint
from pathlib import Path

"""
Калькулятор:
1) Создать воможность регистрации, авторизации (запись и чтение из json файла).
2) Хранить данные о пользователе в формате json.
3) Для неавторизованого юзера  - калькулятор имеет 4 функции: + - * /
4) Для авторизированого  еще + синус косинус тангес котангенс.
5) Авторизированый юзер имеет возможность просмотреть исторю своих операций за последний день(или всю историю).
6) Историю всех операций предлагаю хранить в формате json. Поля для операции - id(уникальное число) , date - дата
операции , operation - сама операция
	Пример:
[{
	id : 1,
	date: '20-10-1953',
	operation: '2+2=4'
}]

Для авторизации использовать логин и пароль. 
PS: все можно делать из консоли, можете не использовать сторонние библиотеки для построения интерфейса.
Но, если есть желание, можете сделать что-то с красивым интерфейсом :)
"""
print('<<Калькулятор>>')

'''
{
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipitsuscipit recusandae consequuntur expedita et"
  }
'''

filename = os.path.join("calculator_log.json")
file_history = os.path.join("calculator_history.json")
check_account = input('Do you have account? Enter y (Yes) or n (No): ')

def calculation(numbers):
    # создать список операций + - * /
    operation_list = []
    for i in numbers:
        if i == '+' or i == '-' or i == '*' or i == '/':
            operation_list.append(i)

    # создать список из чисел
    numbers_list = []
    for i in numbers:
        if i == '+' or i == '-' or i == '*' or i == '/':
            x = numbers.index(i)
            numbers_list.append(float(numbers[:x]))
            numbers = numbers[x + 1:]
    numbers_list.append(float(numbers))

    # разделить список чисел на float и int
    my_list = []
    for i in numbers_list:
        if i != int(i):
            my_list.append(i)
        elif i == int(i):
            my_list.append(int(i))

    # соединить два списка числа и операции + - * /
    thislist = operation_list.copy()
    x = 0
    for i in my_list:
        thislist.insert(x, i)
        x += 2

    # операция умножения, результат вернуть в список
    while 0 < thislist.count('*'):
        for i in thislist:
            if i == "*":
                x = thislist.index(i)
                f = thislist[x - 1] * thislist[x + 1]
                thislist[x - 1:x + 2] = [f]

    # операция деления, результат вернуть в список
    while 0 < thislist.count('/'):
        for i in thislist:
            if i == "/":
                x = thislist.index(i)
                try:
                    f = thislist[x - 1] / thislist[x + 1]
                    thislist[x - 1:x + 2] = [f]
                except ZeroDivisionError:
                    if thislist[x + 1] == 0:
                        raise

    # операция вычитание, результат вернуть в список
    while 0 < thislist.count('-'):
        for i in thislist:
            if i == "-":
                x = thislist.index(i)
                f = thislist[x - 1] - thislist[x + 1]
                thislist[x - 1:x + 2] = [f]

    # операция сложения, результат вернуть в список
    while 0 < thislist.count('+'):
        for i in thislist:
            if i == "+":
                x = thislist.index(i)
                f = thislist[x - 1] + thislist[x + 1]
                thislist[x - 1:x + 2] = [f]
    return thislist[0]

# calculator sin, cos, tan, cat
def trigonometric(operation, my_number):
    if operation == 'sin':
        return math.sin(my_number)
    elif operation == 'cos':
        return math.cos(my_number)
    elif operation == 'tan':
        return math.tan(my_number)
    elif operation == 'ctg':
        return math.cos(my_number) / math.sin(my_number)

# если аккаунт уже есть, проверить его в базе
if check_account == "y":
    # десериализация
    login_list = []
    with open(filename, 'r') as file:
        read_data = json.load(file)
        i = 0
        z = 0
        y = 0
        while i <= 20:
            try:
                login = input('Enter your login: ')
                # если поле login пустое
                if login == '':
                    if i < 20:
                        print('<< This field is empty! Please input a login >>', i)
                    elif i == 20:
                        print('<< This field is empty! Try later >>')
                else:
                    # все login поместить в список
                    for elem in read_data:
                        login_list.append(elem.get('login'))
                    # print('Users =', login_list)
                    x = login_list.index(login)
                    if 0 <= x <= len(read_data):
                        print('<< Hi!', login_list[x], '>>')
                        thisdict = read_data[x:x + 1]
                        # проверка password с базой
                        password = input('Enter your password: ')
                        for z in thisdict:
                            cur_login = z.get('login')
                            # print(z.get('login'), end=" => ")      # !!!! скрыть !!!!
                            # print(z.get('password'))               # !!!! скрыть !!!!
                            while y < 5:
                                if password != z.get('password') or password == '':
                                    if y < 4:
                                        print("<< Password is incorrect! Try again", 4 - y, ">>")
                                    elif y == 4:
                                        print('<< Password is incorrect! Try later >>')
                                        break
                                    password = input('Enter your password: ')
                                elif password == z.get('password'):
                                    print('<< You have successfully logged in! >>')

                                    # добавить операцию в историю
                                    def calculator_history(x, print_result, txt):
                                        # если файл пустой
                                        if os.path.getsize(file_history) == 0:
                                            thisdict = {'id': login_list[x], 'date': txt[0], 'operation': print_result}
                                            data = []
                                            data.append(thisdict)

                                            # сериализация
                                            with open(file_history, 'w') as file:
                                                json.dump(data, file)
                                        else:
                                            # десериализация
                                            # если в файле уже есть данные, добавить в историю
                                            with open(file_history, 'r') as file:
                                                read_data = json.load(file)
                                                thisdict = {'id': login_list[x], 'date': txt[0], 'operation': print_result}
                                                read_data.append(thisdict)

                                        # сериализация
                                        with open(file_history, 'w') as file:
                                            json.dump(read_data, file)

                                        show_history = input('Do you want to see all history operation (a) or last day (l)? Enter a or l: ')

                                        id_login = cur_login
                                        if show_history == 'a':
                                            print('All history:')

                                        history_list = []
                                        all_history = []
                                        numbers = []
                                        last_day_list = []

                                        # десериализация
                                        with open(file_history, 'r') as file:
                                            read_data = json.load(file)

                                            # показать историю за весь период
                                            for elem in read_data:
                                                history_list.append(elem.get('id'))
                                            x = history_list.index(id_login)
                                            for i in history_list:
                                                if i == id_login:
                                                    x = history_list.index(id_login)
                                                    history_list[x] = "#"
                                                    dict_history = read_data[x:x + 1]
                                                    for i in dict_history:
                                                        all_history.append(i)
                                                        numbers.append(i.get('date'))
                                                        if show_history == 'a':
                                                            print('id:', i.get('id'))
                                                            print('date:', i.get('date'))
                                                            print('operation:', i.get('operation'))
                                                            print('')
                                            # показать историю за последний день
                                            if show_history == 'l':
                                                print('Last day history:')
                                                for i in numbers:
                                                    if i == numbers[-1]:
                                                        x = numbers.index(i)
                                                        numbers[x] = '#'
                                                        last_day = all_history[x:x + 1]
                                                        for i in last_day:
                                                            last_day_list.append(i)
                                                        print('id:', i.get('id'))
                                                        print('date:', i.get('date'))
                                                        print('operation:', i.get('operation'))
                                                        print('')
                                    # показать только год-месяц-день
                                    cur_time = str(datetime.datetime.now())
                                    txt = cur_time.split()

                                    choose_operation = input('Do you want to use (sin, cos, tan, ctg)? Enter y or n: ')
                                    if choose_operation == 'y':
                                        operation = input('Choose operation sin, cos, tan, ctg: ')
                                        my_number = float(input('Enter your number: '))
                                        res_trig = trigonometric(operation, my_number)
                                        print_result = operation + '(' + str(my_number) + ')' + ' = ' + str(res_trig)
                                        print(print_result)
                                        calculator_history(x, print_result, txt)
                                    elif choose_operation == 'n':
                                        numbers = input('Calculator + - * /: ')
                                        print_numbers = numbers
                                        result = calculation(numbers)
                                        print_result = print_numbers + ' = ' + str(result)
                                        print(print_result)
                                        calculator_history(x, print_result, txt)
                                    break
                                y += 1
                        break
            # если login нет в списке (index() method raises an exception if the value is not found)
            except ValueError:
                if i < 20:
                    print('<< Login not found! Try again >>')
                elif i == 20:
                    print('<< Login not found! Try later >>')
            if i >= 0:
                login_list.clear()
            i += 1
elif check_account == "n":
    print("!!! << Without account you can use calculator with 4 operation: + - * / >> !!!")
    print("!!! << With account you can use more operation: sin, cos, tan, ctg >> !!!")
    create_account = input('Do you want to create account? Enter y (Yes) or n (No): ')
    # добавить нового пользователя
    if create_account == "y":
        # регистрация 1-го пользователя, если файл пустой
        if os.path.getsize(filename) == 0:
            login = input('Create your login: ')
            password = input('Create your password min 8 символов; min 2 заглавных буквы; min 1 спец. символ - ! ? : ; % *: ')
            thisdict = {'login': login, 'password': password}
            data = []
            data.append(thisdict)

            # сериализация
            with open(filename, 'w') as file:
                json.dump(data, file)
        else:
            # регистрация нового пользователя и проверка на уникальность логина
            login = input('Create your login: ')
            # десериализация
            x = 0
            with open(filename, 'r') as file:
                read_data = json.load(file)
                while x <= 1000000:
                    for elem in read_data:
                        if login == elem.get('login'):
                            print('<< This login is already taken! Try again >>')
                            login = input('Create your login: ')
                        elif login == '':
                            print('<< This field is empty! Please input a login >>')
                            login = input('Create your login: ')
                        x += 1

            # проверка пароля на валидность
            def validate_password(password1):
                thislist = []
                if len(password1) < 8:
                    return {
                        'status': False,
                        'massage': 'This password is too short. It must contain at least 8 characters.'
                    }
                elif password1.find('-') == -1 and password1.find('!') == -1 and password1.find('?') == -1 and password1.find(':') == -1 \
                        and password1.find(';') == -1 and password1.find('%') == -1 and password1.find('*') == -1:
                    return {
                        'status': False,
                        'massage': 'Must be min 1 special symbols - ! ? : ; % *'
                    }
                elif thislist == []:
                    for i in password1:
                        if i != i.lower():
                            thislist.append(i)
                    if len(thislist) < 2:
                        return {
                            'status': False,
                            'massage': 'Must be min 2 capital letters'
                        }
                    else:
                        return {
                            'status': True,
                            'massage': 'OK! You have successfully registered!'
                        }

            password = input('Create your password (length min 8; min 2 capital letters; min 1 symbols - ! ? : ; % *): ')

            result1 = validate_password(password)

            n = 0
            while n < 1000001:
                if result1['status']:
                    print(result1['massage'])
                    thisdict = {'login': login, 'password': password}
                    read_data.append(thisdict)

                    # сериализация
                    with open(filename, 'w') as file:
                        json.dump(read_data, file)
                    break
                else:
                    print(result1['massage'])
                    if n == 1000000:
                        break
                    else:
                        password = input(
                            'Create your password (length min 8; min 2 capital letters; min 1 symbols - ! ? : ; % *): ')
                        result1 = validate_password(password)
                n += 1

                # Pad12Q!              length min 8
                # Password125!         min 2 capital
                # PassWord125          min 1 symbols
                # LeTo%712

    elif check_account == "n":
        numbers = input('Calculator + - * /: ')
        print_numbers = numbers
        # 20.52+8/4+3*10-23.2+10/2+7*2-10*3+4-2
        # 2 + 3 * 2 + 10 - 4

        result = calculation(numbers)
        print(print_numbers, '=', result)
