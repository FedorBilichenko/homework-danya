import psycopg2
import datetime
import pprint

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "technics")

    cursor = connection.cursor()
    while True:
        print("""
                Выберите действие:
                1. Посмотреть все партии
                2. Посмотреть все изделия
                3. Посмотреть всех сотрудников и каким изделием он владеет
                4. Найти по наименованию партии сотрудников по отделу, у которых срок эксплуатации изделия превышает введенный (срок подходит к концу)
                5. Найти сотрудников по отделу
                6. Вывести сотрудников по убыванию возраста
                99. Выход
            """)
        inputNumber = input()

        if inputNumber not in ["1", "2", "3", "4", "5", "6", "99"]:
            continue

        if inputNumber == "1":
            cursor.execute("SELECT * FROM consigments;")
            records = cursor.fetchall()
            records_dic = []
            for consigment in records:
                records_dic.append(
                    {
                        'Id партии': consigment[0],
                        'Название партии': consigment[1],
                        'Поставщик партии': consigment[2],
                        'Кол-во изделии': consigment[3],
                        'Время поступления': consigment[4].strftime('%m.%d.%Y'),
                    }
                )

            pprint.pprint(records_dic)

        if inputNumber == "2":
            cursor.execute("""
            SELECT
            products.id as product_id,
            products.name as product_name,
            products.life_time as product_life_time,
            products.warranty_period as product_warranty_period,
            consigments.name as consigment_name,
            consigments.employer as consigment_employer
            FROM products
            JOIN consigments
            ON products.consigment_id = consigments.id;
            """)
            records = cursor.fetchall()
            records_dic = []
            for product in records:
                records_dic.append(
                    {
                        'Id изделия': product[0],
                        'Название изделия': product[1],
                        'Срок эксплуатации до': product[2].strftime('%m.%d.%Y'),
                        'Гарантия до': product[3].strftime('%m.%d.%Y'),
                        'Название партии': product[4],
                        'Название поставщика партии': product[5],
                    }
                )

            pprint.pprint(records_dic)

        if inputNumber == "3":
            cursor.execute("""
            SELECT
            employees.fio as employee_name,
            employees.age as employee_age,
            employees.department as employee_department,
            products.name as product_name
            FROM employees
            JOIN products
            ON employees.product_id = products.id;
            """)
            records = cursor.fetchall()
            records_dic = []
            for employee in records:
                records_dic.append(
                    {
                        'Имя сотрудника': employee[0],
                        'Кол-во лет': employee[1],
                        'Отдел сотрудника': employee[2],
                        'Название продукта': employee[3],
                    }
                )

            pprint.pprint(records_dic)

        if inputNumber == "4":
            print("Введите отдел сотрудника: ")
            department = input()
            print("Введите наименование партии: ")
            consigment_name = input()
            print("Введите минимальный дату эксплуатации изделия в формате год-месяц-день, например, 2020-10-25: ")
            time = input()

            cursor.execute("""
            SELECT
            employees.fio as employee_name,
            employees.department as employee_department,
            products.name as product_name, 
            products.life_time as product_life_time,
            products.warranty_period as product_warranty_period,
            consigments.name as consigment_name,
            consigments.employer as consigment_employer,
            consigments.time as consigment_time
            FROM employees 
            JOIN products 
            ON employees.product_id = products.id 
            JOIN consigments 
            ON products.consigment_id = consigments.id
            WHERE employees.department = %s AND products.life_time::date > %s AND consigments.name = %s;
            """, (department, time, consigment_name))
            records = cursor.fetchall()
            records_dic = []
            for employee in records:
                records_dic.append(
                    {
                        'Имя сотрудника': employee[0],
                        'Отдел сотрудника': employee[1],
                        'Название изделия': employee[2],
                        'Срок эксплуатации изделия': employee[3].strftime('%m.%d.%Y'),
                        'Гарантийный срок изделия': employee[4].strftime('%m.%d.%Y'),
                        'Название партии': employee[5],
                        'Поставщик партии': employee[6],
                        'Дата поступления партии': employee[7].strftime('%m.%d.%Y'),
                    }
                )

            pprint.pprint(records_dic)

        if inputNumber == "5":
            print("Введите отдел")
            department = input()
            cursor.execute("""SELECT
             employees.fio as employee_name,
             employees.age as employee_age,
             employees.department as employee_department
             FROM employees WHERE department = %s;""", (department,))
            records = cursor.fetchall()
            records_dic = []
            for employee in records:
                records_dic.append(
                    {
                        'Имя сотрудника': employee[0],
                        'Кол-во лет': employee[1],
                        'Отдел сотрудника': employee[2]
                    }
                )

            pprint.pprint(records_dic)

        if inputNumber == "6":
            cursor.execute("""
            SELECT
            employees.fio as employee_name,
            employees.age as employee_age,
            employees.department as employee_department
            FROM employees ORDER BY age DESC;""")
            records = cursor.fetchall()
            records_dic = []
            for employee in records:
                records_dic.append(
                    {
                        'Имя сотрудника': employee[0],
                        'Кол-во лет': employee[1],
                        'Отдел сотрудника': employee[2]
                    }
                )

            pprint.pprint(records_dic)

        if inputNumber == "99":
            break

except (Exception, psycopg2.Error) as error:
    print ("Ошибка коннекта к Postgres", error)
finally:
        if(connection):
            cursor.close()
            connection.close()
            print("Соединение закрыто")