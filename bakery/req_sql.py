# Все sql запросы обрабатываются в этом файле
import sqlite3

connection = sqlite3.connect("bakery_data_base.db")
cursor_b =connection.cursor()

# Создание основных таблиц

cursor_b.execute('''CREATE TABLE IF NOT EXISTS `categories` (
	`id_category` integer primary key NOT NULL UNIQUE,
	`name_category` TEXT NOT NULL,
	FOREIGN KEY(`id_category`) REFERENCES `products`(`id_category`)
	);''') 
cursor_b.execute('''CREATE TABLE IF NOT EXISTS `products` (
	`id_product` integer primary key NOT NULL UNIQUE,
	`name_product` TEXT NOT NULL,
	`id_category` INTEGER NOT NULL,
	`price` INTEGER NOT NULL,
	`quantity` INTEGER NOT NULL,
	FOREIGN KEY(`id_product`) REFERENCES `check`(`id_product`)
	);''')
cursor_b.execute('''CREATE TABLE IF NOT EXISTS `checks` (
	`id_check` integer NOT NULL,
	`date` TEXT NOT NULL,
	`id_product` INTEGER NOT NULL,
	`quantity` INTEGER NOT NULL,
    PRIMARY KEY (id_check, id_product)
	);''')

# Заполнение таблицы `categories`
cursor_b.execute('''INSERT OR IGNORE INTO categories(id_category,name_category) VALUES (1,'Хлеб')''')
cursor_b.execute('''INSERT OR IGNORE INTO categories(id_category,name_category) VALUES (2,'Выпечка')''')
cursor_b.execute('''INSERT OR IGNORE INTO categories(id_category,name_category) VALUES (3,'Десерты и пирожные')''')
cursor_b.execute('''INSERT OR IGNORE INTO categories(id_category,name_category) VALUES (4,'Соленая выпечка и закуски')''')
cursor_b.execute('''INSERT OR IGNORE INTO categories(id_category,name_category) VALUES (5,'Напитки')''')

# Заполнение таблицы "products"
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (1,'Багет', 1, 100, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (2,'Пан-де-кампань', 1, 70, 2000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (3,'Пан-де-сель', 1, 90, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (4,'Пан-комплет', 1, 120, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (5,'Фюгасс', 1, 130, 1000)''')

cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (6,'Круассан', 2, 120, 2000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (7,'Пэн-о-шоколад', 2, 110, 1500)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (8,'Шуссон-о-пом', 2, 90, 1205)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (9,'Бриошь', 2, 60, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (10,'Эклер', 2, 80, 1000)''')

cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (11,'Тарт-о-ситрон', 3, 200, 500)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (12,'Тарт-о-пом', 3, 500, 300)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (13,'Миллефёй', 3, 140, 700)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (14,'Макарон', 3, 70, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (15,'Опера', 3, 140, 500)''')

cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (16,'Киш', 4, 200, 500)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (17,'Сэндвичи', 4, 230, 700)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (18,'Фокачча', 4, 250, 550)''')

cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (19,'Американо', 5, 90, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (20,'Эспрессо', 5, 100, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (21,'Капучино', 5, 120, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (22,'Латте', 5, 140, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (23,'Моккачино', 5, 120, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (24,'Флэт уайт', 5, 110, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (25,'Двойной эсперессо', 5, 100, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (26,'Раф', 5, 150, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (27,'Макиато', 5, 120, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (28,'Зеленый чай', 5, 60, 1000)''')
cursor_b.execute('''INSERT OR IGNORE INTO products(id_product, name_product, id_category, price, quantity) VALUES (29,'Черный чай', 5, 60, 1000)''')

with open("check.txt","r",encoding="utf-8") as checks:
	for check in checks:
		temp = check.strip().split(';') 
		cursor_b.execute('''INSERT OR IGNORE INTO checks VALUES (?, ?, ?, ?)''',(int(temp[0]), temp[1], int(temp[2]), int(temp[3])))

connection.commit()

# Функция для запросов из других файлов
def bakery_sql(sting_req):
    result_sql = cursor_b.execute(sting_req).fetchall()
    return result_sql

# Функция для создание чека
def create_check(date,orders,amounts):
	max_id = connection.execute('''SELECT MAX(id_check) FROM checks ''').fetchall()[0][0] + 1
	if isinstance(orders,(tuple,list)):
		for i,order in enumerate(orders):
			res = connection.execute('''INSERT OR IGNORE INTO checks VALUES (?,?,?,?)''',(max_id,date,int(order),int(amounts[i])))
			res = connection.execute(f'''UPDATE products 
										SET  quantity =  quantity - {amounts[i]} 
										WHERE id_product = {order}''')
	else:
		res = connection.execute('''INSERT OR IGNORE INTO checks VALUES (?,?,?,?)''',(max_id,date,int(order),int(amounts)))
	
	connection.commit()
	return "success"

# функция для создания чека в файл
def create_check_in_file(data,orders,amounts):
	create_check(data,orders,amounts)
	max_id = connection.execute('''SELECT MAX(id_check) FROM checks ''').fetchall()[0][0]
	res = connection.execute(f'''SELECT c.date, p.name_product, p.price, c.quantity
						  FROM checks c
						  JOIN products p ON c.id_product = p.id_product
						  WHERE id_check = {int(max_id)}
						  GROUP BY p.name_product''').fetchall()

	with open(f"check{max_id}.txt","w",encoding="utf-8") as out:
		res_price = 0
		for text in res:
			out.write(f"{text[1]}\n") 
			out.write(f"{text[3]} шт. * {text[2]} = {text[3]*text[2]}\n")
			res_price += text[2]*text[3]
		out.write(f"Итоговая стоимость заказа: {res_price}\n")
		out.write("Спасибо за покупку <3")
	return "success"

    

