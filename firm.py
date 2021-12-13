
class Firm:

    @staticmethod
    def select():
        name = input('Введите название фирмы: ')

        return "select * from firm where name = %s;", [name, ]

    @staticmethod
    def show_all():
        return 'select * from firm;', []

    @staticmethod
    def insert():
        name = input('Введите название фирмы: ')
        address = input('Введите адрес фирмы: ')
        owner = input('Введите имя владельца фирмы: ')

        return "insert into firm (name, address, owner) VALUES (%s, %s, %s);", \
               [name, address, owner]

    @staticmethod
    def update():
        name = input('Введите название фирмы: ')
        address = input('Введите новый адрес фирмы: ')
        owner = input('Введите новое имя владельца фирмы: ')

        return "update firm set address = %s, owner = %s where name = %s;", \
               [address, owner, name]

    @staticmethod
    def delete():
        name = input('Введите название фирмы: ')

        return "delete from firm where name = %s;", [name, ]
