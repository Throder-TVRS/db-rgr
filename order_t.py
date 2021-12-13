
class OrderT:

    @staticmethod
    def select():
        client_name = input('Введите имя клиента, сделавшего заказ: ')
        order_date = input('Введите дату заказа: ')

        return "select * from order_t where order_date = %s and client_name = %s;", [order_date, client_name]

    @staticmethod
    def show_all():
        return 'select * from order_t;', []

    @staticmethod
    def insert():
        client_name = input('Введите имя клиента, сделавшего заказ: ')
        order_date = input('Введите дату заказа: ')
        cost = input('Введите цену заказа: ')
        details = input('Введите детали заказа: ')

        return "insert into order_t (client_name, order_date, cost, details) VALUES (%s, %s, %s, %s);", \
               [client_name, order_date, cost, details]

    @staticmethod
    def update():
        client_name = input('Введите имя клиента, сделавшего заказ: ')
        order_date = input('Введите дату заказа: ')
        cost = input('Введите новую цену заказа: ')
        details = input('Введите новые детали заказа: ')

        return "update order_t set cost = %s, details = %s where client_name = %s and order_date = %s;", \
               [cost, details, client_name, order_date]

    @staticmethod
    def delete():
        client_name = input('Введите имя клиента, сделавшего заказ: ')
        order_date = input('Введите дату заказа: ')

        return "delete from order_t where client_name = %s and order_date = %s;", [client_name, order_date]
