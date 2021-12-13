
class OrderDateFirm:

    @staticmethod
    def select():
        firm_name = input('Введите название фирмы: ')
        client_name = input('Введите клиента этой фирмы: ')
        order_date = input('Введите дату заказа клиента у фирмы: ')

        return "select * from order_date_firm where firm_name = %s and client_name = %s and order_date;", \
               [firm_name, client_name, order_date]

    @staticmethod
    def show_all():
        return 'select * from order_date_firm;', []

    @staticmethod
    def insert():
        firm_name = input('Введите название фирмы: ')
        client_name = input('Введите клиента этой фирмы: ')
        order_date = input('Введите дату заказа клиента у фирмы: ')

        return "insert into order_date_firm (firm_name, client_name, order_date) VALUES (%s, %s, %s);", \
               [firm_name, client_name, order_date]

    @staticmethod
    def update():
        return None

    @staticmethod
    def delete():
        firm_name = input('Введите название фирмы: ')
        client_name = input('Введите клиента этой фирмы: ')
        order_date = input('Введите дату заказа клиента у фирмы: ')

        return "delete from order_date_firm where firm_name = %s and client_name = %s and order_date = %s;", \
               [firm_name, client_name, order_date]
