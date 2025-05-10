import sqlite3


connection = sqlite3.connect("my_database.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS `student` (
	`id_student` integer primary key NOT NULL UNIQUE,
	`id_level` INTEGER NOT NULL,
	`id_way` INTEGER NOT NULL,
	`id_type_education` INTEGER NOT NULL,
	`fullname` TEXT NOT NULL,
	`name` TEXT NOT NULL,
	`secondname` TEXT NOT NULL,
	`average_score` REAL NOT NULL,
    FOREIGN KEY(`id_level`) REFERENCES `level_education`(`id_level`),
    FOREIGN KEY(`id_way`) REFERENCES `way`(`id_way`),
    FOREIGN KEY(`id_type_education`) REFERENCES `type_education`(`id_type`)
    );
    
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS `level_education` (
	`id_level` integer primary key NOT NULL UNIQUE,
	`title_ed` TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS `way` (
	`id_way` integer primary key NOT NULL UNIQUE,
	`title_way` TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS `type_education` (
	`id_type` integer primary key NOT NULL UNIQUE,
	`title_type` TEXT NOT NULL
    );
''')
cursor.connection.commit()
# Функция читает файл и заполоняет базу данных
def append_db(file_name, table, id_el, title):
	with open(f"{file_name}", 'r', encoding="utf-8") as file:
		for item in file:
			if item[-1] == '\n':
				item = item[:-1]
			temp = item.split(',')
		cursor.execute(f"INSERT OR IGNORE INTO {table} ({id_el},{title}) VALUES ({temp[0]},'{temp[1]}')")
	cursor.connection.commit()
			
append_db("level_db.txt","level_education","id_level","title_ed")
append_db("way_db.txt","way","id_way","title_way")
append_db("type_db.txt","type_education","id_type","title_type")

with open("base_db.txt",'r',encoding="utf-8") as db:
	for i in db:
		i = i[:-1].split(',')
		query = f'''
		INSERT OR IGNORE INTO student (id_student,id_level,id_way,id_type_education,fullname,name,secondname,average_score) 
		VALUES ({int(i[0])},{int(i[1])},{int(i[2])},{int(i[3])},'{i[4]}','{str(i[5])}','{str(i[6])}',{float(i[7])})
		'''
		cursor.execute(query)
	print("success")
query_cnt_student = '''SELECT COUNT(id_student) AS COUNT FROM student'''
query_cnt_way = '''SELECT COUNT(id_way) FROM student GROUP BY id_way'''
query_type = '''SELECT COUNT(id_type_education) FROM student GROUP BY id_type_education'''
query_score = '''SELECT MAX(average_score) AS max_score, AVG(average_score) AS avg_score, MIN(average_score) AS min_score FROM student
		GROUP BY id_way'''
query_average_score_way = '''SELECT AVG(average_score) AS avg_way FROM student GROUP BY id_way'''
query_average_score_level = '''SELECT AVG(average_score) AS avg_way FROM student GROUP BY id_level'''
query_average_score_type ='''SELECT AVG(average_score) AS avg_way FROM student GROUP BY id_type_education'''
query_best_student = '''SELECT * FROM student WHERE id_way == 1 ORDER BY average_score'''
query_repeat = '''SELECT fullname, COUNT(fullname) FROM student GROUP BY fullname'''
query_same = '''SELECT fullname, name, secondname, COUNT(*) AS count
    FROM student
    GROUP BY fullname, name, secondname
    HAVING COUNT(*) > 1'''

# первый пункт
print("1) Всего обучается",*cursor.execute(query_cnt_student).fetchall()[0],"человек.")

# второй пункт
res = cursor.execute(query_cnt_way).fetchall()
print()
print("2) Прикладная информатика =",*res[0],"человек.")
print("   Управление персоналом =",*res[1],"человек.")
print("   Реклама и связь с общественностью = ",*res[2],"человек.")
print("   Сервис =",*res[3],"человек.")
print("   Туризм =",*res[4],"человек.")
print("   Экономика =",*res[5],"человек.")

# третий пункт
res = cursor.execute(query_type).fetchall()
print()
print("3) Очная =",*res[0],"человек.")
print("   Заочная =",*res[1],"человек.")
print("   Вечерняя =",*res[2],"человек.")

# четвертый пункт
res = cursor.execute(query_score).fetchall()
print()
print("4) Прикладная информатика:","Max =",res[0][0],"AVG =",round(res[0][1],2),"MIN =",res[0][2])
print("   Управление персоналом:","Max =",res[1][0],"AVG =",round(res[1][1],2),"MIN =",res[1][2])
print("   Реклама и связь с общественностью:","Max =",res[2][0],"AVG =",round(res[2][1],2),"MIN =",res[2][2])
print("   Сервис:","Max =",res[3][0],"AVG =",round(res[3][1],2),"MIN =",res[3][2])
print("   Туризм:","Max =",res[4][0],"AVG =",round(res[4][1],2),"MIN =",res[4][2])
print("   Экономика:","Max =",res[5][0],"AVG =",round(res[5][1],2),"MIN =",res[5][2])

# пятый пункт
res_level = cursor.execute(query_average_score_level).fetchall()
res_way = cursor.execute(query_average_score_way).fetchall()
res_type = cursor.execute(query_average_score_type).fetchall()
print()
print("5) Бакалавр =",round(*res_level[0],2),"Магистратура =",round(*res_level[1],2),"Аспирантура =",round(*res_level[2],2))
print("   Прикладная информатика =",round(*res_way[0],2),'\n',"  Управление персоналом =",round(*res_way[1],2),'\n',"  Реклама и связь с общественностью =",round(*res_way[2],2),'\n',"  Сервис =",round(*res_way[3],2),'\n',"  Туризм =",round(*res_way[4],2),'\n',"  Экономика",round(*res_way[5],2))
print("   Очное =",round(*res_type[0],2),"Заочное =",round(*res_type[1],2),"Вечернее =",round(*res_type[2],2))

# шестой пункт
res = cursor.execute(query_best_student).fetchall()
print()
print("6) Лучшие студенты: ")
print('  ',*res[34])
print('  ',*res[33])
print('  ',*res[32])
print('  ',*res[31])
print('  ',*res[30])

# седьмой пункт
cnt = 0
res = cursor.execute(query_repeat).fetchall()
for i in res:
	if i[1] > 1:
		cnt += i[1]

print()
print("7) Кол-во однофамильцев:",cnt)

# восьмой пункт
res =  cursor.execute(query_same).fetchall()
print()
print("8) Кол-во тесок:")
for i in res:
	print(*i)
	
connection.commit()
connection.close()