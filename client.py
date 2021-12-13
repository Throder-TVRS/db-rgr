
class Client:

    @staticmethod
    def select():
        name = input('Введите имя клиента: ')

        return "select * from client where name = %s;", [name, ]

    @staticmethod
    def show_all():
        return 'select * from client;', []

    @staticmethod
    def insert():
        name = input('Введите имя клиента: ')
        phone_number = input('Введите номер телефона клиента: ')
        age = input('Введите возраст клиента: ')
        sex = input('Введите пол клиента: ')

        return "insert into client (name, phone_number, age, sex) VALUES (%s, %s, %s, %s);", \
               [name, phone_number, age, sex]

    @staticmethod
    def update():
        name = input('Введите имя клиента: ')
        phone_number = input('Введите новый номер телефона клиента: ')
        age = input('Введите новый возраст клиента: ')
        sex = input('Введите новый пол клиента: ')

        return "update client set phone_number = %s, age = %s, sex = %s where name = %s;", \
               [phone_number, age, sex, name]

    @staticmethod
    def delete():
        name = input('Введите имя клиента: ')

        return "delete from client where name = %s;", [name, ]
