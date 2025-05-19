# Обработка всех sql запросов
import sqlite3 as sql

def _sql_append_db(file_name,table,id_e,title):
	if isinstance(id_e,str) and isinstance(title,str):
		with open(file_name,'r',encoding="utf-8") as file:
			for line in file:
				line = line.strip().split(',')
				cursor.execute(f'''INSERT OR IGNORE INTO {table}({id_e},{title}) VALUES ({line[0]},'{line[1]}')''')
		
	elif isinstance(id_e,tuple) and not(isinstance(title,tuple)):
		with open(file_name, 'r', encoding='utf-8') as file:
			for line in file:
				line = line.strip().split(',')
				cursor.execute(f'''INSERT OR IGNORE INTO {table}({id_e[0]},{id_e[1]},{title}) VALUES (?,?,?)''',(line[0],line[1],line[2]))
		
	elif isinstance(title,tuple) and not(isinstance(id_e,tuple)):
		with open(file_name,"r",encoding='utf-8') as file:
			for line in file:
				line = line.strip().split(',')
				cursor.execute(f'''INSERT OR IGNORE INTO {table}({id_e},{title[0]},{title[1]},{title[2]}) VALUES (?,?,?,?)''',
				(line[0],line[1],line[2],line[3]))
				
	elif isinstance(title, tuple) and isinstance(id_e, tuple):
		with open(file_name, "r", encoding='utf-8') as file:
			for line in file:
				line = line.strip().split(',')
				cursor.execute(f'''	INSERT OR IGNORE INTO {table}({id_e[0]},{id_e[1]},{id_e[2]},{id_e[3]},{title[0]},{title[1]},{title[2]}) 
				   VALUES (?,?,?,?,?,?,?)''',
				   (line[0],line[1],line[2],line[3],line[4],line[5],line[6]))
	cursor.connection.commit()
     
# Функция для запросов из базы данных
def sql_request(string):
    return cursor.execute(string).fetchall()[0][0]

connection = sql.connect("vynil.db")
cursor = connection.cursor()

# Создание таблиц 
cursor.execute('''CREATE TABLE IF NOT EXISTS `Genre` (
	`id_genre` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`name_genre` TEXT NOT NULL,
FOREIGN KEY(`id_genre`) REFERENCES `Creators`(`id_genre`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Creators` (
	`id_creator` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`id_genre` INTEGER NOT NULL,
	`name_creator` TEXT NOT NULL,
FOREIGN KEY(`id_creator`) REFERENCES `Albums`(`id_creator`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Albums` (
	`id_album` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`id_creator` INTEGER NOT NULL,
	`name_album` TEXT NOT NULL,
FOREIGN KEY(`id_album`) REFERENCES `Serial_numbers`(`id_album`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Serial_numbers` (
	`id_number` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`id_supplier` INTEGER NOT NULL,
	`id_album` INTEGER NOT NULL,
	`id_branch` INTEGER NOT NULL,
	`state` TEXT NOT NULL,
	`serial_number` TEXT NOT NULL,
	`price` INTEGER NOT NULL,
FOREIGN KEY(`id_number`) REFERENCES `Checks`(`id_number`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Branch_stores` (
	`id_branch` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`address` TEXT NOT NULL,
FOREIGN KEY(`id_branch`) REFERENCES `Serial_numbers`(`id_branch`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Suppliers` (
	`id_supplier` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`name_supplier` TEXT NOT NULL,
FOREIGN KEY(`id_supplier`) REFERENCES `Serial_numbers`(`id_supplier`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Users` (
	`id_user` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`phone_number` TEXT NOT NULL,
	`full_name_user` TEXT NOT NULL,
	`password` TEXT NOT NULL,
FOREIGN KEY(`id_user`) REFERENCES `Checks`(`id_user`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Checks` (
	`id_check` INTEGER key NOT NULL,
	`id_number` INTEGER NOT NULL,
	`id_user` INTEGER NOT NULL,
	`data_order` TEXT NOT NULL,
    PRIMARY KEY(`id_check`,`id_number`)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS `Employees` (
	`id_employee` integer primary key AUTOINCREMENT NOT NULL UNIQUE,
	`id_branch` INTEGER NOT NULL,
	`code_employee` TEXT NOT NULL,
	`password` TEXT NOT NULL,
	FOREIGN KEY(`id_branch`) REFERENCES `Branch_stores`(`id_branch`)
);''')

cursor.connection.commit()

#Добавления значений
_sql_append_db("genre_for_db.txt","Genre","id_genre","name_genre")
_sql_append_db("branch_for_db.txt","Branch_stores","id_branch","address")
_sql_append_db("supplier_for_db.txt","Suppliers","id_supplier","name_supplier")

_sql_append_db("creators_for_db.txt","Creators",("id_creator","id_genre"),"name_creator")
_sql_append_db("albums_for_db.txt","Albums",("id_album","id_creator"),"name_album")

_sql_append_db("employees_for_db.txt","Employees","id_employee",("id_branch","code_employee","password"))
_sql_append_db("checks_for_db.txt","Checks","id_check",("id_number","id_user","data_order"))
_sql_append_db("users_for_db.txt","Users","id_user",("phone_number","full_name_user","password"))

all_id = ("id_number","id_supplier","id_album","id_branch")
all_title =("state","serial_number","price")
_sql_append_db("serial_number_for_db.txt","Serial_numbers",all_id,all_title)

# print(cursor.execute("SELECT * FROM Genre").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Branch_stores").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Suppliers").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Creators").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Albums").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Checks").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Users").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Employees").fetchall(),'\n\n')
# print(cursor.execute("SELECT * FROM Serial_numbers").fetchall(),'\n\n')


