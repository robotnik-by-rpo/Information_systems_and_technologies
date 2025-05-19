import sqlite3
from sql_vynil import *

profit = cursor.execute('''SELECT 
        bs.address AS 'Филиал',
        SUM(sn.price) AS 'Общая выручка'
    FROM Serial_numbers sn
    JOIN Branch_stores bs ON sn.id_branch = bs.id_branch
    WHERE sn.state = 'продан'
    GROUP BY bs.id_branch, bs.address
    ORDER BY SUM(sn.price) DESC
    ''').fetchall()

best_album = cursor.execute('''SELECT 
    c.name_creator AS 'Исполнитель',
    a.name_album AS 'Альбом',
    COUNT(*) AS 'Количество продаж'
    FROM Checks ch
    JOIN Serial_numbers sn ON ch.id_number = sn.id_number
    JOIN Albums a ON sn.id_album = a.id_album
    JOIN Creators c ON a.id_creator = c.id_creator
    WHERE sn.state = 'продан'
    GROUP BY a.id_album, c.name_creator, a.name_album
    ORDER BY COUNT(*) DESC
    ''').fetchall()

profitable_album = cursor.execute('''SELECT 
    c.name_creator AS 'Исполнитель',
    a.name_album AS 'Альбом',
    SUM(sn.price) AS 'Общая выручка'
    FROM Checks ch
    JOIN Serial_numbers sn ON ch.id_number = sn.id_number
    JOIN Albums a ON sn.id_album = a.id_album
    JOIN Creators c ON a.id_creator = c.id_creator
    WHERE sn.state = 'продан'
    GROUP BY a.id_album
    ORDER BY SUM(sn.price) DESC
    ''').fetchall()

print(*profit,sep='\n')
print()
print(*best_album,sep="\n")
print()
print(*profitable_album,sep='\n')