import sqlite3

connect = sqlite3.connect("data_base_employees.db")
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS `job_title` (
	`id_positions` integer primary key NOT NULL UNIQUE,
	`title` TEXT NOT NULL,
    FOREIGN KEY(`id_positions`) REFERENCES `employees`(`id_position_emp`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `employees` (
	`id_employee` integer primary key NOT NULL UNIQUE,
	`fullname` TEXT NOT NULL,
	`name` TEXT NOT NULL,
	`number_phone` TEXT NOT NULL,
	`id_position_emp` INTEGER NOT NULL,
    FOREIGN KEY(`id_employee`) REFERENCES `order`(`id_employee_or`)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `orders` (
	`id_order` integer primary key NOT NULL UNIQUE,
	`id_client` INTEGER NOT NULL,
	`id_employee_or` INTEGER NOT NULL,
	`sum_order` INTEGER NOT NULL,
	`data_complited` TEXT NOT NULL,
	`mark_about_completed` INTEGER NOT NULL,
    FOREIGN KEY(`id_client`) REFERENCES `clients`(`id_client`)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `clients` (
	`id_client` integer primary key NOT NULL UNIQUE,
	`organization` TEXT NOT NULL,
	`number_phone_client` INTEGER NOT NULL
    );''')

def append_db(file_name,table,id_el,title):
	with open(file_name,"r", encoding="utf-8") as file:
		for str_file in file:
			str_file = str_file.strip()
			temp = str_file.split(',')
			cursor.execute(f'''INSERT OR IGNORE INTO {table} ({id_el}, {title}) VALUES ({temp[0]},'{temp[1]}')''')
	cursor.connection.commit()

def change_str(line):
	line = line.strip().split(',')
	return line
append_db("job_title.txt","job_title","id_positions","title")

# Открываем файл и записываем данные работников в базу данных
with open("employees.txt",'r',encoding="utf-8") as emp:
	for el in emp:
		el_m = change_str(el)
		cursor.execute(f'''INSERT OR REPLACE INTO employees VALUES ({int(el_m[0])},'{el_m[1]}','{el_m[2]}','{el_m[3]}',{int(el_m[4])})''')


# Открываем файл и записываем данные заказов в базу данных 
with open("orders.txt",'r',encoding='utf-8') as orders:
	for el in orders:
		el_m = change_str(el)
		cursor.execute(f'''INSERT OR REPLACE INTO orders VALUES ({int(el_m[0])},{int(el_m[1])},{int(el_m[2])},{int(el_m[3])},'{el_m[4]}',{int(el_m[5])})''')


# Открываем файл и записываем данные заказов в базу данных
with open("clients.txt",'r',encoding='utf-8') as clients:
	for el in clients:
		el_m = change_str(el)
		cursor.execute(f'''INSERT OR REPLACE INTO clients VALUES ({int(el_m[0])},'{el_m[1]}','{el_m[2]}')''')
cursor.connection.commit()
print()

# Пять простых запросов
query_count_emp = '''SELECT COUNT(id_employee) FROM employees'''
res = cursor.execute(query_count_emp).fetchall()
print("Кол-во работников",*res[0])

query_sum_order='''SELECT SUM(sum_order) FROM orders'''
res = cursor.execute(query_sum_order).fetchall()
print("Выручка со всех заказов",*res[0])

query_avg_order = '''SELECT AVG(sum_order) FROM orders'''
res = cursor.execute(query_avg_order).fetchall()
print("Средняя цена заказа",round(*res[0],2))

query_max_order = '''SELECT MAX(sum_order) FROM orders'''
res = cursor.execute(query_max_order).fetchall()
print("Самый дорогой заказ на сумму",*res[0])

query_min_order = '''SELECT MIN(sum_order) FROM orders'''
res = cursor.execute(query_min_order).fetchall()
print("Самый дешевый заказ на сумму",*res[0])
print()

#  Функция для вывода сообщений
def print_el(res,message):
	for i in res:
		print(*i,message)
	return '\n'

# Запросы с агригацией
query_how_many_order = '''SELECT 
						clients.organization,
						COUNT(orders.id_client) AS order_count
						FROM orders
						JOIN clients ON orders.id_client = clients.id_client
						GROUP BY orders.id_client, clients.organization'''
res = cursor.execute(query_how_many_order).fetchall()
print("Кол-во заказов разных компаний:")
print(print_el(res,'заказ(а)'))

query_sum_order_organization = '''SELECT 
						clients.organization,
						SUM(orders.sum_order) AS order_sum
						FROM orders
						JOIN clients ON orders.id_client = clients.id_client
						GROUP BY clients.organization'''
res = cursor.execute(query_sum_order_organization).fetchall()
print("Сколько денег потратила каждая компания:")
print(print_el(res,'руб'))

query_cnt_position = '''SELECT jt.title,
    		COUNT(e.id_employee) AS employee_count
			FROM job_title jt
			JOIN employees e ON jt.id_positions = e.id_position_emp
			GROUP BY jt.title'''
res = cursor.execute(query_cnt_position).fetchall()
print("Кол-во человек на каждой должности:")
print(print_el(res,"человек"))

# три запроса с объединением и условиями
query_emp_have_amount_ord = ''' SELECT e.fullname,
			e.name,
			COUNT(o.id_order) AS cnt_order
			FROM employees e 
			JOIN orders o ON e.id_employee = o.id_employee_or
			GROUP BY e.fullname,e.name
			HAVING COUNT(o.id_order) > 2
			'''
res = cursor.execute(query_emp_have_amount_ord).fetchall()
print("Самые активные работники:")
print(print_el(res,'участия в заказах'))

query_emp_brought_money = ''' SELECT e.fullname,
			e.name,
			SUM(o.sum_order) AS sum_emp
			FROM employees e 
			JOIN orders o ON e.id_employee = o.id_employee_or
			GROUP BY e.fullname,e.name
			HAVING SUM(o.sum_order) > 700000
			ORDER BY sum_emp DESC
			'''
res = cursor.execute(query_emp_brought_money).fetchall()
print("Лучшие работники, принесшие большую выручку в компанию:")
print(print_el(res,'руб'))

query_pos_brought_money = '''SELECT jt.title,
				SUM(o.sum_order) AS sum_pos
				FROM job_title jt
				JOIN employees e ON e.id_position_emp = jt.id_positions
				JOIN orders o ON e.id_employee = o.id_employee_or
				GROUP BY jt.title
				HAVING SUM(o.sum_order) > 3000000
				ORDER BY sum_pos DESC
'''
res = cursor.execute(query_pos_brought_money).fetchall()
print("Самые прибыльные должности для компании:")
print(print_el(res,'руб'))
