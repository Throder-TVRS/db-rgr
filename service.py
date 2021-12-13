
class Service:

    @staticmethod
    def select():
        name = input('Введите имя клиента: ')

        return "select * from service where name = %s;", [name, ]

    @staticmethod
    def show_all():
        return 'select * from service;', []

    @staticmethod
    def insert():
        name = input('Введите название услуги: ')
        description = input('Введите описание услуги: ')
        rate = input('Введите тариф услуги: ')
        firm_name = input('Введите название фирмы, которая предоставляет услугу: ')

        return "insert into service (name, description, rate, firm_name) VALUES (%s, %s, %s, %s);", \
               [name, description, rate, firm_name]

    @staticmethod
    def update():
        name = input('Введите название услуги: ')
        firm_name = input('Введите название фирмы, которая предоставляет услугу: ')
        description = input('Введите новое описание услуги: ')
        rate = input('Введите новый тариф услуги: ')


        return "update service set description = %s, rate = %s where name = %s and firm_name = %s;", \
               [description, rate, name, firm_name]

    @staticmethod
    def delete():
        name = input('Введите название услуги: ')
        firm_name = input('Введите название фирмы, которая предоставляет услугу: ')

        return "delete from service where name = %s and firm_name = %s;", [name, firm_name]
