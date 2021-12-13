
class ClientFirm:

    @staticmethod
    def select():
        firm_name = input('Введите название фирмы: ')
        client_name = input('Введите клиента этой фирмы: ')

        return "select * from client_firm where firm_name = %s and client_name = %s;", [firm_name, client_name]

    @staticmethod
    def show_all():
        return 'select * from client_firm;', []

    @staticmethod
    def insert():
        firm_name = input('Введите название фирмы: ')
        client_name = input('Введите клиента этой фирмы: ')

        return "insert into client_firm (firm_name, client_name) VALUES (%s, %s);", \
               [firm_name, client_name]

    @staticmethod
    def update():
        return None

    @staticmethod
    def delete():
        firm_name = input('Введите название фирмы: ')
        client_name = input('Введите клиента этой фирмы: ')

        return "delete from client_firm where firm_name = %s and client_name = %s;", [firm_name, client_name]
