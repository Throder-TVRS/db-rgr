import sys
from contextlib import closing
import psycopg2
from psycopg2 import IntegrityError

from client import Client
from firm import Firm
from service import Service
from order_t import OrderT
from client_firm import ClientFirm
from order_date_firm import OrderDateFirm

TABLES = [('Клиент', 'Client', 'client'),
          ('Фирма', 'Firm', 'firm'),
          ('Услуга', 'Service', 'service'),
          ('Заказ', 'OrderT', 'order_t'),
          ('Фирмы/клиенты', 'ClientFirm', 'client_firm'),
          ('Фирмы/даты заказов', 'OrderDateFirm', 'order_date_firm')]

OPERATIONS = [('Просмотр', 'select'),
              ('Просмотр всей таблицы', 'show_all'),
              ('Добавление', 'insert'),
              ('Удаление', 'delete'),
              ('Обновление', 'update')]

SPECIAL_QUERIES = [('Полная очистка таблицы', 'table_truncate'),
                   ('По названию фирмы получить список предоставляемых ей услуг', 'service_by_firm'),
                   ('По названию услуги получить список фирм, которые её предоставляют', 'firm_by_service'),
                   ('Получить список клиентов фирмы', 'client_by_firm'),
                   ('Получить список фирм, клиентом которых является человек', 'firm_by_client'),
                   ('По клиенту и дате заказа узнать у какой фирмы он был сделан', 'firm_by_client_and_date'),
                   ('Получить список дат, в которые клиент делал у фирмы заказы', 'date_by_firm_and_client'),
                   ('Сбросить все таблицы', 'drop_tables')]


def is_correct(option, lower_bound, upper_bound):
    """Проверка опции на корректность"""
    return option.isnumeric() and lower_bound <= int(option) <= upper_bound


def print_tables():
    """Печать списка таблиц"""
    print('Список таблиц:')
    for table in TABLES:
        print(f"'{table[0]}'", end=' ')
    print()


def print_options(array, message):
    """Печать опций, перечисленных в списке array"""
    for i in range(len(array)):
        print(f"{i + 1}. {message}{array[i][0]}")
    print(f"{len(array) + 1}. Назад")
    return input('Выберите номер опции: ')


def print_option_without_back(array, message):
    """Печать опций, перечисленных в списке array, без перечисления опции 'Назад'"""
    for i in range(len(array)):
        print(f"{i + 1}. {message}{array[i][0]}")
    return input('Выберите номер опции: ')


def table_selection(conn, cursor):
    """Меню выбора таблицы"""
    while True:
        print()
        print('Доступные таблицы:')
        option = print_options(TABLES, 'Работать с таблицей ')

        if not is_correct(option, 1, len(TABLES) + 1):
            print('Некорректный ввод!')
            print('Повторите попытку.')
        elif option == f'{len(TABLES) + 1}':
            return
        else:
            operation_selection(conn, cursor, int(option) - 1)


def print_select_result(cursor, table):
    """Печать результата селекта"""
    rows = cursor.fetchall()
    cursor.execute(f"select * from {TABLES[table][2]} limit 0")
    for desc in cursor.description:
        print(desc[0], end=' ')
    print()
    for row in rows:
        print(row)


def operation_selection(conn, cursor, table):
    """Меню выбора действия над таблицей"""
    while True:
        print()
        print(f'Вы работаете с таблицей {TABLES[table][0]}')
        print('Доступные операции:')
        option = print_options(OPERATIONS, '')

        if not is_correct(option, 1, len(TABLES) + 1):
            print('Некорректный ввод!')
            print('Повторите попытку.')
        elif option == f'{len(OPERATIONS) + 1}':
            return
        else:
            operation = int(option) - 1
            print(f"Выполняем операцию {OPERATIONS[operation][0]} над таблицей {TABLES[table][0]}")
            try:
                query, params = eval(f'{TABLES[table][1]}.{OPERATIONS[operation][1]}()')
                if query is None:
                    print('Операция запрещена для данной таблицы')
                    continue
                cursor.execute(query, params)
                if operation < 2:
                    print_select_result(cursor, table)
                else:
                    print('Запрос исполнен. Зафиксировать результат?')
                    print('1. Да')
                    print('2. Нет')
                    commit = input('Введите ответ: ')
                    while not is_correct(commit, 1, 2):
                        print('Некорректный ответ. Повторите ввод: ')
                        commit = input()
                    if commit == '1':
                        conn.commit()
                        print('Изменения зафиксированы')
                    else:
                        conn.rollback()
                        print('Изменения не зафиксированы')
            except Exception as e:
                print(e)
                conn.rollback()


def table_truncate():
    """Полная очистка таблицы"""
    print('Доступные таблицы: ')
    table = print_option_without_back(TABLES, 'Очистить ')

    while not is_correct(table, 1, len(TABLES)):
        print('Некорректный ответ. Повторите ввод: ')
        table = input()

    table = int(table) - 1
    return f"truncate {TABLES[table][2]} cascade", []


def service_by_firm():
    """По названию фирмы получить список предоставляемых ей услуг"""
    firm_name = input('Введите название фирмы: ')
    return f"select name from service where firm_name = %s;", [firm_name, 2]


def firm_by_service():
    """По названию услуги получить список фирм, которые её предоставляют"""
    name = input('Введите название услуги: ')
    return f"select firm_name from service where name = %s;", [name, 2]


def client_by_firm():
    """Получить список клиентов фирмы"""
    firm_name = input('Введите название фирмы: ')
    return f"select client_name from client_firm where firm_name = %s;", [firm_name, 4]


def firm_by_client():
    """Получить список фирм, клиентом которых является человек"""
    client_name = input('Введите имя клиента: ')
    return f"select firm_name from client_firm where client_name = %s;", [client_name, 4]


def firm_by_client_and_date():
    """По клиенту и дате заказа узнать у какой фирмы он был сделан"""
    client_name = input('Ввежите имя клиента: ')
    order_date = input('Введите дату заказа: ')

    return f"select firm_name from order_date_firm where client_name = %s and order_date = %s", \
           [client_name, order_date, 5]


def date_by_firm_and_client():
    """Получить список дат, в которые клиент делал у фирмы заказы"""
    client_name = input('Ввежите имя клиента: ')
    firm_name = input('Введите название фирмы: ')

    return f"select order_date from order_date_firm where client_name = %s and firm_name = %s", \
           [client_name, firm_name, 5]


def date_and_client_by_firm():
    """Получить информацию о заказах конкретной фирмы"""
    firm_name = input('Введите название фирмы: ')

    return f"select client_name, order_date from order_date_firm where firm_name = %s", \
           [firm_name, 5]


def create_tables(conn, cursor):
    """Создание стандартных необходимых таблиц, если их нет"""
    cursor.execute("""
create table if not exists firm (
    name varchar(255) primary key,
    address varchar(255),
    owner varchar(255)
);
create table if not exists client (
    name varchar(255) primary key,
    phone_number varchar(255),
    age integer,
    sex varchar(255)
);
create table if not exists service (
    name varchar(255),
    description varchar(255),
    rate float,
    firm_name varchar(255),
    primary key (name, firm_name),
    foreign key (firm_name) references firm (name) on delete cascade on update cascade
);
create table if not exists order_t (
    order_date timestamp,
    cost float,
    details varchar(255),
    client_name varchar(255),
    primary key (order_date, client_name),
    foreign key (client_name) references client (name) on delete cascade on update cascade
);
create table if not exists client_firm (
    firm_name varchar(255),
    client_name varchar(255),
    primary key (firm_name, client_name),
    foreign key (firm_name) references firm (name) on delete cascade on update cascade,
    foreign key (client_name) references client (name) on delete cascade on update cascade
);
create table if not exists order_date_firm (
    firm_name varchar(255),
    order_date timestamp,
    client_name varchar(255),
    primary key (firm_name, order_date, client_name),
    foreign key (firm_name) references firm (name) on delete cascade on update cascade,
    foreign key (order_date, client_name) references order_t (order_date, client_name) on delete cascade on update cascade
);""")
    conn.commit()


def drop_tables(conn, cursor):
    for table in TABLES:
        cursor.execute(f"""drop table if exists {table[2]} cascade;""")
        conn.commit()
    create_tables(conn, cursor)


def special_queries(conn, cursor):
    """Меню выбора особых запросов"""
    while True:
        print()
        print('Доступные запросы:')
        option = print_options(SPECIAL_QUERIES, '')

        if not is_correct(option, 1, len(SPECIAL_QUERIES) + 1):
            print('Некорректный ввод!')
            print('Повторите попытку.')
        elif option == f'{len(SPECIAL_QUERIES) + 1}':
            return
        else:
            option = int(option) - 1
            try:
                if option == 7:
                    drop_tables(conn, cursor)
                    continue
                query, params = eval(f'{SPECIAL_QUERIES[option][1]}()')
                if option > 0:
                    table = params.pop(-1)
                cursor.execute(query, params)
                if option > 0:
                    print_select_result(cursor, table)
                else:
                    print('Запрос исполнен. Зафиксировать результат?')
                    print('1. Да')
                    print('2. Нет')
                    commit = input('Введите ответ: ')
                    while not is_correct(commit, 1, 2):
                        print('Некорректный ответ. Повторите ввод: ')
                        commit = input()
                    if commit == '1':
                        conn.commit()
                        print('Изменения зафиксированы')
                    else:
                        conn.rollback()
                        print('Изменения не зафиксированы')
            except Exception as e:
                print(e)
                conn.rollback()


def main():
    """Главное меню"""
    if len(sys.argv) != 5:
        print('Неправильные аргументы командной строки.')
        print('Использование: python3 main.py <db_name> <user> <password> <host>')
        print('Пример: python3 main.py rgr postgres postgres localhost')
        sys.exit()
    try:
        with closing(psycopg2.connect(dbname=sys.argv[1], user=sys.argv[2], password=sys.argv[3], host=sys.argv[4])) as conn:
            with conn.cursor() as cursor:
                create_tables(conn, cursor)
                while True:
                    print()
                    print('Доступные опции:')
                    print('1. Запросы в конкретную таблицу')
                    print('2. Специальные запросы')
                    print('3. Список таблиц')
                    print('4. Выход')
                    option = input('Выберите номер опции: ')

                    if not is_correct(option, 1, 4):
                        print('Некорректный ввод!')
                        print('Повторите попытку.')

                    elif option == '1':
                        table_selection(conn, cursor)

                    elif option == '2':
                        special_queries(conn, cursor)

                    elif option == '3':
                        print_tables()
                    else:
                        break
    except Exception as e:
        print(e)
        print('Выполнение прервано')


if __name__ == '__main__':
    main()
