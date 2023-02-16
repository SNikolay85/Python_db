import psycopg2

def create_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id_client SERIAL PRIMARY KEY,
            first_name VARCHAR(15),
            last_name VARCHAR(30),
            mail VARCHAR(50) UNIQUE);
        """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                phone_id SERIAL PRIMARY KEY,
                phone_number INTEGER UNIQUE,
                id_client INTEGER REFERENCES client(id_client));
            """)
    conn.commit()

def del_db():
    cur.execute("""
    DROP TABLE client, phone CASCADE
    """)
    conn.commit()

def add_client(first_name, last_name, mail=None, phone=None):
    cur.execute("""
        INSERT INTO client(first_name, last_name, mail)
            VALUES(%s,%s,%s);
        """, (first_name, last_name, mail))
    if mail == None:
        cur.execute("""
            INSERT INTO phone(phone_number, id_client)
                VALUES(%s,(SELECT id_client
                             FROM client
                            WHERE first_name = %s AND last_name = %s AND mail IS NULL));
        """, (phone, first_name, last_name))
    else:
        cur.execute("""
                    INSERT INTO phone(phone_number, id_client)
                        VALUES(%s,(SELECT id_client
                                     FROM client
                                    WHERE first_name = %s AND last_name = %s AND mail = %s));
                """, (phone, first_name, last_name, mail))
    conn.commit()
    display()

def delete_client(id_client):
    cur.execute("""
    DELETE FROM phone
    WHERE id_client = %s;
    """, (id_client,))
    cur.execute("""
    DELETE FROM client
    WHERE id_client = %s;
    """, (id_client,))
    conn.commit()
    display()

def add_phone(id_client, phone):
    cur.execute("""
    INSERT INTO phone(phone_number, id_client)
        VALUES(%s, %s);
    """, (phone, id_client))
    conn.commit()
    display()

def update_phone(id_client, phone_number):
    cur.execute("""
    UPDATE phone SET phone_number = %s
    WHERE id_client = %s;
    """, (phone_number, id_client))
    conn.commit()
    display()

def del_phone(id_client, phone, phone_num):
    cur.execute("""
    UPDATE phone SET phone_number = %s
    WHERE id_client = %s AND phone_number = %s;
    """, (phone_num, id_client, phone))
    conn.commit()
    display()

def delete_phone(id_client, phone):
   cur.execute("""
   DELETE FROM phone
   WHERE phone_number = %s AND id_client = %s;
   """, (phone, id_client))
   conn.commit()
   display()

def change_client(id_client, first_name=None, last_name=None, mail=None):
    cur.execute("""
    UPDATE client SET first_name = %s, last_name = %s, mail = %s
    WHERE id_client = %s;
    """, (first_name, last_name, mail, id_client))
    conn.commit()
    display()

def find_client(first_name=None, last_name=None, mail=None, phone=None):
    cur.execute("""
    SELECT cl.id_client, first_name, last_name, mail, phone_number
    FROM client AS cl
    LEFT JOIN phone AS ph ON ph.id_client = cl.id_client
    WHERE first_name = %s OR last_name = %s OR mail = %s OR phone_number = %s;
    """, (first_name, last_name, mail, phone))
    lst = cur.fetchall()
    lst.insert(0, ('id_client', 'first_name', 'last_name', 'mail', 'phone'))
    lst.insert(1, ('---------------', '---------------', '---------------', '---------------', '---------------'))
    for cl in lst:
        for field in cl:
            text = str(field)
            print(f'| {text.center(15)}', end=' ')
        print()

def display():
    cur.execute("""
        SELECT cl.id_client, first_name, last_name, mail, phone_number
        FROM client AS cl
        LEFT JOIN phone AS ph ON ph.id_client = cl.id_client;
        """)
    lst = cur.fetchall()
    lst.insert(0, ('id_client', 'first_name', 'last_name', 'mail', 'phone'))
    lst.insert(1, ('---------------', '---------------', '---------------', '---------------', '---------------'))
    for cl in lst:
        for field in cl:
            text = str(field)
            print(f'| {text.center(15)}', end=' ')
        print()

def message(x):
    if x == 'y':
        print(f'1 - Создание структуры БД \n'
              f'2 – Удаление структуры БД \n'
              f'3 – Добавить нового клиента \n'
              f'4 – Удалить существующего клиента \n'
              f'5 – Добавить телефон для существующего клиента \n'
              f'6 – Удалить телефон у существующего клиента \n'
              f'7 – Изменить данные о клиенте \n'
              f'8 – Найти клиента по его данным \n'
              f'9 – Просмотр списка клиентов \n'
              f'q - выход')
        comand = input('\nВведи команду: ')
        return comand
    else:
        comand = 'q'
        return comand

def digit():
    while True:
        p_num = input('Введи номер телефона: ')
        if p_num.isdigit():
            phone_num = int(p_num)
            return phone_num
            break
        elif p_num == '':
            return ''
            break
        else:
            print('Введено не число')


def client_managment():
    while True:
        comand = message(input('Вывести меню?(y/n)'))
        if comand == '1':
            print()
            create_db()
            print()
        elif comand == '2':
            print()
            del_db()
            print()
        elif comand == '3':
            print()
            while True:
                first_name = input('Введи имя: ')
                last_name = input('Введи фамилию: ')
                m = input('Введи адрес эл. почты: ')
                p_num = digit()
                if first_name != '' and last_name != '':
                    if m == '' and p_num != '':
                        add_client(first_name, last_name, phone=p_num)
                    elif m != '' and p_num == '':
                        add_client(first_name, last_name, mail=m)
                    elif m != '' and p_num != '':
                        add_client(first_name, last_name, mail=m, phone=p_num)
                    elif m == '' and p_num == '':
                        add_client(first_name, last_name)
                    print()
                    question = input('Внести следующего клиента?(y/n)')
                    if question == 'y':
                        True
                    else:
                        break
                else:
                    print('Не введены обязательные поля(ФИО)')
            print()
        elif comand == '4':
            print()
            while True:
                while True:
                    data_4 = []
                    id_client = input('Введи ID клиента: ')
                    cur.execute("""
                    SELECT id_client FROM client;
                    """)
                    for i in cur.fetchall():
                        data_4.append(*i)
                    if int(id_client) not in data_4:
                        print('Введен не существующий ID')
                    else:
                        delete_client(id_client)
                        break
                print()
                question = input('Удалить следующего клиента?(y/n)')
                if question == 'y':
                    True
                else:
                    break
            print()
        elif comand == '5':
            print()
            while True:
                while True:
                    data_5 = []
                    id_client = input('Введи ID клиента: ')
                    cur.execute("""
                    SELECT id_client FROM client;
                    """)
                    for i in cur.fetchall():
                        data_5.append(*i)
                    if int(id_client) not in data_5:
                        print('Введен не существующий ID')
                    else:
                        phone = digit()
                        if phone != '':
                            cur.execute("""
                            SELECT COUNT(phone_number) FROM phone
                            WHERE id_client = %s;
                            """, (id_client,))
                            count = cur.fetchone()
                            if count == (0,):
                                update_phone(id_client, phone)
                            else:
                                add_phone(id_client, phone)
                        else:
                            print('Номер не занесен!')
                        break
                print()
                question = input('Добавить еще один номер?(y/n)')
                if question == 'y':
                    True
                else:
                    break
            print()
        elif comand == '6':
            print()
            while True:
                while True:
                    data_6 = []
                    data_6_1 = []
                    id_client = input('Введи ID клиента: ')
                    cur.execute("""
                    SELECT id_client FROM client;
                    """)
                    for i in cur.fetchall():
                        data_6.append(*i)
                    if int(id_client) not in data_6:
                        print('Введен не существующий ID')
                    else:
                        while True:
                            phone = digit()
                            cur.execute("""
                            SELECT phone_number FROM phone WHERE id_client = %s;
                            """, (id_client,))
                            for i in cur.fetchall():
                                data_6_1.append(*i)
                            if phone not in data_6_1:
                                print('У данного клиента нет такого номера')
                            elif phone != '':
                                cur.execute("""
                                SELECT COUNT(id_client) FROM phone
                                WHERE id_client = %s;
                                """, (id_client,))
                                count = cur.fetchone()
                                if count == (1,):
                                    del_phone(id_client, phone, phone_num=None)
                                else:
                                    delete_phone(id_client, phone)
                            break
                        break
                print()
                question = input('Удалить еще один номер?(y/n)')
                if question == 'y':
                    True
                else:
                    break
            print()
        elif comand == '7':
            print()
            while True:
                data_7 = []
                id_client = input('Введи ID клиента: ')
                cur.execute("""
                SELECT id_client FROM client;
                """)
                for i in cur.fetchall():
                    data_7.append(*i)
                if int(id_client) not in data_7:
                    print('Введен не существующий ID')
                else:
                    print('Введи данные, для изменения: ')
                    f_n = input('Введи имя: ')
                    l_n = input('Введи фамилию: ')
                    m = input('Введи адрес эл. почты: ')
                    if f_n == '':
                        f_n = None
                    if l_n == '':
                        l_n = None
                    if m == '':
                        m = None
                    change_client(id_client, f_n, l_n, m)
                    break
            print()
        elif comand == '8':
            print()
            print('Введи данные, для поиска: ')
            f_n = input('Введи имя(необязательно): ')
            l_n = input('Введи фамилию(необязательно): ')
            m = input('Введи адрес эл. почты(необязательно): ')
            p_number = digit()
            if f_n == '':
                f_n = None
            if l_n == '':
                l_n = None
            if m == '':
                m = None
            if p_number == '':
                p_number = None
            find_client(f_n, l_n, m, p_number)
            print()
        elif comand == '9':
            print()
            display()
            print()
        elif comand == 'q':
            break

with open('D:\Python\pas.txt', encoding='utf-8') as file:
    pas = file.read()

with psycopg2.connect(database='clients', user='postgres', password=pas) as conn:
    with conn.cursor() as cur:
        client_managment()


