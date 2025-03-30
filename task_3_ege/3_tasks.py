import pandas as pd
import sqlite3

#Ссылка на задание https://inf-ege.sdamgia.ru/problem?id=37415

# Подключаемся к базе данных в памяти
conn = sqlite3.connect(':memory:')

# Читаем данные из Excel
df = pd.read_excel('3.xlsx', sheet_name='Движение товаров')

# Переименовываем столбцы для удобства
df.columns = ['Operation_ID', 'Operation_Date', 'Store_ID', 'Product_ID', 
              'Package_Count', 'Operation_Type', 'Price']

# Загружаем данные в SQLite
df.to_sql('Inventory_Movement', conn, if_exists='replace', index=False)

# Запрос для решения задачи
query = '''
SELECT 
    SUM(CASE WHEN Operation_Type = 'Поступление' THEN Package_Count ELSE -Package_Count END) AS NetIncrease
FROM Inventory_Movement
WHERE Product_ID = 15
AND Store_ID IN ('M3', 'M9', 'M11', 'M14')
AND Operation_Date BETWEEN '2021-06-01' AND '2021-06-10'
'''

# Выполняем запрос
res = pd.read_sql_query(query, conn)
net_increase = res['NetIncrease'].iloc[0] if not res.empty else 0

print(f"Количество упаковок яиц диетических (артикул 15) в магазинах Заречного района увеличилось на: {net_increase}")

# Закрываем соединение
conn.close()