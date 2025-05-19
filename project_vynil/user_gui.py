# GUI для пользователей
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, 
                               QVBoxLayout, QWidget, QStackedWidget, QGridLayout,QComboBox,QTextEdit,QMessageBox)
import sys
from PySide6.QtCore import Qt
from datetime import date
from sql_vynil import *


# План:
# Страница с авторизацией
# Страница с жанрами(rock,jazz,post-punk,hip-hop)
# Для каждого жанра по странице  
# Корзина


TRESH = []
ALL_TRESH = []
INFO = []

def find_user():
    phone = input_number_sign_up.text()
    pas = input_password_sign_up.text().strip()
    # print()
    # print(phone,pas)
    res = cursor.execute(f'''SELECT id_user FROM Users 
                         WHERE phone_number = ? AND password = ? ''',(phone,pas)).fetchone()
    if res is not None:
        switch_page_sign_up()
        
        INFO.append(res[0])
    
        input_number_sign_up.clear()
        
        input_password_sign_up.clear()
    else:
        QMessageBox.warning(main_window, "Ошибка", "Зарегистрируйтесь в систему")


def take_user_data():
    try:
        phone = input_phone.text()
        name = input_full_name.text()
        password = input_password.text()
        existing_user = cursor.execute('''SELECT id_user FROM Users WHERE phone_number = ?''', (phone,)).fetchone()
        if existing_user:
            QMessageBox.warning(main_window, "Ошибка", "Пользователь с таким номером телефона уже зарегистрирован")
            return
        if not phone or not name or not password:
            QMessageBox.warning(main_window, "Ошибка", "Все поля должны быть заполнены")
            return

        cursor.execute('''INSERT OR IGNORE INTO Users(phone_number, full_name_user, password) VALUES(?,?,?)''',(phone,name,password))
        new_user_id = cursor.execute('''SELECT id_user FROM Users WHERE phone_number = ?''', (phone,)).fetchone()[0]
        INFO.append(new_user_id)
        switch_page_sign_up()
        input_phone.clear()
        input_full_name.clear()
        input_password.clear()
        connection.commit()
    except:
        QMessageBox.warning(main_window, "Ошибка", "Заполните поля")

def buy_albums():
    global CURRENT_USER_ID, PHONE_NUMBER, ALL_TRESH
    now_date = date.today().isoformat()
    id_user = INFO 
    max_id_check = cursor.execute('''SELECT MAX(id_check) FROM Checks''').fetchone()[0]
    max_id_check += 1
    
    for album in ALL_TRESH:
        req_id = cursor.execute(f'''SELECT id_number 
                                FROM Serial_numbers s
                                JOIN Albums a ON a.id_album = s.id_album
                                WHERE a.name_album = ? AND s.state = 'в продаже'
                                LIMIT ?
                                ''',(album[1],album[3])).fetchall()
        print(req_id)
        for id_number in req_id:
            cursor.execute('''UPDATE Serial_numbers 
                           SET state = 'продан' WHERE id_number = ?''',(id_number[0],))
            cursor.execute('''INSERT INTO Checks(id_check, id_number,id_user,data_order) VALUES (?,?,?,?)''',
                           (max_id_check, id_number[0],id_user[0],now_date))
    
    if len(ALL_TRESH) > 0:
        msg = QMessageBox()
        msg.setWindowTitle("Корзина")
        msg.setText("Отправлена ссылка для оплаты")
        msg.setIcon(QMessageBox.Information)
        msg.exec()
    delete_tresh_now()
    update_tresh_display()     
    
    connection.commit()

def delete_tresh_now():
    text_field.clear()
    ALL_TRESH.clear()
    text_field.setText("Корзина пуста")

def update_tresh_display():
    text_field.clear()  # Очищаем текущее содержимое
    if ALL_TRESH:  # Если корзина не пуста
        for item in ALL_TRESH:
                creator, album, price, quantity = item
                line = f"{creator} - {album}\t{quantity} шт.\t{price * quantity}"
                text_field.append(line)  # Добавляем строку
    else:
        text_field.setText("Корзина пуста")

def populate_hip_hop_creators():
    combo_creator_hip_hop.clear()  # Очищаем текущий список
    combo_creator_hip_hop.addItem("Выберите исполнителя")  # Добавляем заглушку
    # Запрашиваем исполнителей для жанра hip-hop (id_genre = 1)
    creators = cursor.execute("SELECT id_creator, name_creator FROM Creators WHERE id_genre = 1").fetchall()
    for creator in creators:
        combo_creator_hip_hop.addItem(creator[1], creator[0])  # name_creator, id_creator как userData

def many_albums():
    msg = QMessageBox()
    msg.setWindowTitle("Альбомы")
    msg.setText("Уменьшите кол-во альбомов на покупку")
    msg.setIcon(QMessageBox.Information)
    msg.exec()

def cnt_album(name_album):
    try:
        res = cursor.execute(f'''SELECT 
        COUNT(s.id_number) AS 'Количество в продаже'
        FROM Albums a
        JOIN Serial_numbers s ON a.id_album = s.id_album
        WHERE a.name_album = '{name_album}' AND s.state = 'в продаже'
        GROUP BY a.name_album;
        ''')
        return res.fetchone()[0]
    except:
        msg = QMessageBox()
        msg.setWindowTitle("Альбомы")
        msg.setText("Альбома нет в продаже")
        msg.setIcon(QMessageBox.Information)
        msg.exec()

# Функция для обновления списка альбомов на основе выбранного музыканта
def update_hip_hop_albums(index):
    combo_album_hip_hop.clear()  # Очищаем текущий список альбомов
    text_hip_hop.clear()
    combo_album_hip_hop.addItem("Выберите альбом")  # Добавляем заглушку
    # Получаем id_creator из выбранного элемента
    creator_id = combo_creator_hip_hop.itemData(index)
    if creator_id:
        # Запрашиваем альбомы для выбранного исполнителя
        albums = cursor.execute('''
            SELECT a.name_album, 
           (SELECT MIN(price) FROM Serial_numbers 
            WHERE id_album = a.id_album AND state = 'в продаже') as price
            FROM Albums a
            WHERE a.id_creator = ?
                                    
        ''', (creator_id,)).fetchall()
    
        for album in albums:
            name, price = album
            display_text = f"{name} - {price if price else 'Нет в продаже'}"
            combo_album_hip_hop.addItem(display_text, (name, price))
    
def message_tresh():
    msg = QMessageBox()
    msg.setWindowTitle("Корзина")
    msg.setText("Товар добавлен в корзину")
    msg.setIcon(QMessageBox.Information)
    msg.exec()

def message_quantity():
    QMessageBox.warning(main_window, "Ошибка", "Выберите кол-во и товар из списка")

def message_error():
    QMessageBox.warning(main_window, "Ошибка", "Выберите товар из списка")

def add_tresh_hip_hop():
    try:
        TRESH.clear()
        creator = combo_creator_hip_hop.currentText()
        album_data = combo_album_hip_hop.currentData()
        album_text = combo_album_hip_hop.currentText()
        quantity = int(text_hip_hop.text())
        if creator != "Выберите исполнителя" and album_text != "Выберите альбом":
            if album_data:
                album_name, price = album_data
                for item in ALL_TRESH:
                    if item[0] == creator and item[1] == album_name:
                        QMessageBox.warning(main_window, "Ошибка", "Этот альбом уже в корзине")
                        return
                if quantity>0 and quantity <= cnt_album(album_name) and price:
                    ALL_TRESH.append((creator,album_name,price,quantity))
                    text_hip_hop.setText("")
                    message_tresh()
                
                    # print(TRESH)
                    # print(ALL_TRESH)
                else:
                    many_albums()
                    return
                    
        else:
            message_error()
    except:
        pass


def jazz_creator():
    combo_creator_jazz.clear()
    combo_creator_jazz.addItem("Выберите исполнителя")
    creators = cursor.execute("SELECT id_creator, name_creator FROM Creators WHERE id_genre = 2").fetchall()
    for creator in creators:
        combo_creator_jazz.addItem(creator[1], creator[0])

def update_jazz_albums(index):
    combo_album_jazz.clear()
    text_jazz.clear()
    combo_album_jazz.addItem("Выберите альбом")
    creator_id = combo_creator_jazz.itemData(index)
    if creator_id:
        albums = cursor.execute('''
            SELECT a.name_album, 
           (SELECT MIN(price) FROM Serial_numbers 
            WHERE id_album = a.id_album AND state = 'в продаже') as price
            FROM Albums a
            WHERE a.id_creator = ?
    
        ''', (creator_id,)).fetchall()
        for album in albums:
            name, price = album
            display_text = f"{name} - {price if price else 'Нет в продаже'}"
            combo_album_jazz.addItem(display_text, (name, price))

def add_tresh_jazz():
    try:
        TRESH.clear()
        creator = combo_creator_jazz.currentText()
        album_data = combo_album_jazz.currentData()
        album_text = combo_album_jazz.currentText()
        quantity = int(text_jazz.text())
        if creator != "Выберите исполнителя" and album_text != "Выберите альбом":
            if album_data:
                album_name, price = album_data
                for item in ALL_TRESH:
                        if item[0] == creator and item[1] == album_name:
                            QMessageBox.warning(main_window, "Ошибка", "Этот альбом уже в корзине")
                            return
                if quantity>0 and quantity <= cnt_album(album_name) and price:
                    ALL_TRESH.append((creator,album_name,price,quantity))
                    message_tresh()
                    text_jazz.setText("")
                    # print(TRESH)
                else:
                    many_albums()
        else:
            message_error()
    except:
        pass


def rock_creator():
    combo_creator_rock.clear()
    combo_creator_rock.addItem("Выберите исполнителя")
    creators = cursor.execute("SELECT id_creator, name_creator FROM Creators WHERE id_genre = 3").fetchall()
    for creator in creators:
        combo_creator_rock.addItem(creator[1], creator[0])
    
def update_rock_albums(index):
    combo_album_rock.clear()
    text_rock.clear()
    combo_album_rock.addItem("Выберите альбом")
    creator_id = combo_creator_rock.itemData(index)
    if creator_id:
        albums = cursor.execute('''
             SELECT a.name_album, 
           (SELECT MIN(price) FROM Serial_numbers 
            WHERE id_album = a.id_album AND state = 'в продаже') as price
            FROM Albums a
            WHERE a.id_creator = ?
        ''', (creator_id,)).fetchall()
        for album in albums:
            name, price = album
            display_text = f"{name} - {price if price else 'Нет в продаже'}"
            combo_album_rock.addItem(display_text, (name, price))

def add_tresh_rock():
    try:
        TRESH.clear()
        creator = combo_creator_rock.currentText()
        album_data = combo_album_rock.currentData()
        album_text = combo_album_rock.currentText()
        quantity = int(text_rock.text())
        if creator != "Выберите исполнителя" and album_text != "Выберите альбом":
            if album_data:
                album_name, price = album_data
                for item in ALL_TRESH:
                        if item[0] == creator and item[1] == album_name:
                            QMessageBox.warning(main_window, "Ошибка", "Этот альбом уже в корзине")
                            return
                if quantity>0 and quantity <= cnt_album(album_name) and price:
                    ALL_TRESH.append((creator,album_name,price,quantity))
                    message_tresh()
                    text_rock.setText("")
                    # print(TRESH)
                else:
                    many_albums()
        else:
            message_error()
    except:
        pass

def post_punk_creator():
    combo_creator_post_punk.clear()
    combo_creator_post_punk.addItem("Выберите исполнителя")
    creators = cursor.execute("SELECT id_creator, name_creator FROM Creators WHERE id_genre = 4").fetchall()
    for creator in creators:
        combo_creator_post_punk.addItem(creator[1], creator[0])

def update_post_punk_albums(index):
    combo_album_post_punk.clear()
    text_post_punk.clear()
    combo_album_post_punk.addItem("Выберите альбом")
    creator_id = combo_creator_post_punk.itemData(index)
    if creator_id:
        albums = cursor.execute('''
             SELECT a.name_album, 
           (SELECT MIN(price) FROM Serial_numbers 
            WHERE id_album = a.id_album AND state = 'в продаже') as price
            FROM Albums a
            WHERE a.id_creator = ?
        ''', (creator_id,)).fetchall()
        for album in albums:
            name, price = album
            display_text = f"{name} - {price if price else 'Нет в продаже'}"
            combo_album_post_punk.addItem(display_text, (name, price))

def add_tresh_post_punk():
    try:
        TRESH.clear()
        creator = combo_creator_post_punk.currentText()
        album_data = combo_album_post_punk.currentData()
        album_text = combo_album_post_punk.currentText()
        quantity = int(text_post_punk.text())
        if creator != "Выберите исполнителя" and album_text != "Выберите альбом":
            if album_data:
                album_name, price = album_data
                for item in ALL_TRESH:
                        if item[0] == creator and item[1] == album_name:
                            QMessageBox.warning(main_window, "Ошибка", "Этот альбом уже в корзине")
                            return
                if quantity>0 and quantity <= cnt_album(album_name) and price:
                    ALL_TRESH.append((creator,album_name,price,quantity))
                    message_tresh()
                    text_post_punk.setText("")
                    # print(ALL_TRESH)
                    # print(TRESH)
                else:
                    many_albums()
        else:
            message_error()
    except:
        pass


app = QApplication(sys.argv)

main_window = QMainWindow()
main_window.setWindowTitle("Baudlier's vinyl")
main_window.setFixedSize(680,480)

# Создание центрального виджета для перемотки страниц
central_widget = QWidget()
main_layout = QVBoxLayout()
stacked_widget = QStackedWidget()

# Страница входа в систему 
page_sign_up = QWidget()
page_sign_up_layout = QVBoxLayout()

label_sign_up = QLabel("Страница входа в систему")
label_sign_up.setAlignment(Qt.AlignmentFlag.AlignCenter)
input_number_sign_up = QLineEdit()
input_number_sign_up.setPlaceholderText("Введите номер")

input_password_sign_up = QLineEdit()
input_password_sign_up.setPlaceholderText("Введите пароль")
button_to_page_genre = QPushButton("Войти в систему")
button_registration = QPushButton("Зарегистрироваться")

page_sign_up_layout.addWidget(label_sign_up)
page_sign_up_layout.addWidget(input_number_sign_up)
page_sign_up_layout.addWidget(input_password_sign_up)
page_sign_up_layout.addWidget(button_to_page_genre)
page_sign_up_layout.addWidget(button_registration)
page_sign_up.setLayout(page_sign_up_layout)

# Страница с выбором жанра
page_genre = QWidget()
page_genre_layout = QGridLayout()

hip_hop_button = QPushButton("Hip-hop")
jazz_button = QPushButton("Jazz")
post_punk_button = QPushButton("Post-punk")
rock_button = QPushButton("Rock")
tresh = QPushButton("Корзина")

out_account = QPushButton("Выйти из системы")

page_genre_layout.addWidget(hip_hop_button,0,0)
page_genre_layout.addWidget(jazz_button,0,1)
page_genre_layout.addWidget(post_punk_button,1,0)
page_genre_layout.addWidget(rock_button,1,1)
page_genre_layout.addWidget(tresh, 2, 0, 1, 2)
page_genre_layout.addWidget(out_account,3,0, 1, 2)
page_genre_layout.setSpacing(10)
page_genre_layout.setContentsMargins(20,20,20,20)
page_genre.setLayout(page_genre_layout)

# Страница c пластинками hip-hop
combo_creator_hip_hop = QComboBox()
combo_creator_hip_hop.currentIndexChanged.connect(update_hip_hop_albums)
combo_album_hip_hop = QComboBox()
text_hip_hop = QLineEdit()
text_hip_hop.setPlaceholderText("Введите кол-во")
page_hip_hop = QWidget()
page_hip_hop_layout = QVBoxLayout()

tresh_hip_hop = QPushButton("Добавить в корзину")
tresh_hip_hop.clicked.connect(add_tresh_hip_hop)
back_genre_hip_hop = QPushButton("Вернуться к жанрам")
page_hip_hop_layout.addWidget(combo_creator_hip_hop)
page_hip_hop_layout.addWidget(combo_album_hip_hop)
page_hip_hop_layout.addWidget(text_hip_hop)
page_hip_hop_layout.addWidget(tresh_hip_hop)
page_hip_hop_layout.addWidget(back_genre_hip_hop)
page_hip_hop.setLayout(page_hip_hop_layout)


# Страница с пластинками jazz
combo_creator_jazz = QComboBox()
combo_creator_jazz.currentIndexChanged.connect(update_jazz_albums)
combo_album_jazz = QComboBox()
text_jazz = QLineEdit()
text_jazz.setPlaceholderText("Введите кол-во")
page_jazz = QWidget()
page_jazz_layout = QGridLayout()

tresh_jazz = QPushButton("Добавить в корзину")
tresh_jazz.clicked.connect(add_tresh_jazz)
back_genre_jazz = QPushButton("Вернутся к жанрам")
page_jazz_layout.addWidget(combo_creator_jazz)
page_jazz_layout.addWidget(combo_album_jazz)
page_jazz_layout.addWidget(text_jazz)
page_jazz_layout.addWidget(tresh_jazz)
page_jazz_layout.addWidget(back_genre_jazz)
page_jazz.setLayout(page_jazz_layout)

# Страница с пластинками rock
combo_creator_rock = QComboBox()
combo_creator_rock.currentIndexChanged.connect(update_rock_albums)
combo_album_rock = QComboBox()
text_rock = QLineEdit()
text_rock.setPlaceholderText("Введите кол-во")
page_rock = QWidget()
page_rock_layout = QGridLayout()

tresh_rock = QPushButton("Добавить в корзину")
tresh_rock.clicked.connect(add_tresh_rock)
back_genre_rock = QPushButton("Вернутся к жанрам")
page_rock_layout.addWidget(combo_creator_rock)
page_rock_layout.addWidget(combo_album_rock)
page_rock_layout.addWidget(text_rock)
page_rock_layout.addWidget(tresh_rock)
page_rock_layout.addWidget(back_genre_rock)
page_rock.setLayout(page_rock_layout)

#Страница с пластинками post-punk
page_post_punk = QWidget()
page_post_punk_layout = QGridLayout()
combo_creator_post_punk = QComboBox()
combo_creator_post_punk.currentIndexChanged.connect(update_post_punk_albums)
combo_album_post_punk = QComboBox()
text_post_punk = QLineEdit()
text_post_punk.setPlaceholderText("Введите кол-во")

tresh_post_punk = QPushButton("Добавить в корзину")
tresh_post_punk.clicked.connect(add_tresh_post_punk)
back_genre_post_punk = QPushButton("Вернутся к жанрам")
page_post_punk_layout.addWidget(combo_creator_post_punk)
page_post_punk_layout.addWidget(combo_album_post_punk)
page_post_punk_layout.addWidget(text_post_punk)
page_post_punk_layout.addWidget(tresh_post_punk)
page_post_punk_layout.addWidget(back_genre_post_punk)
page_post_punk.setLayout(page_post_punk_layout)

# Страница Корзины
page_tresh = QWidget()
page_tresh_layout = QVBoxLayout()

text_field = QTextEdit()
text_field.setReadOnly(True)

update_tresh_display()
    
sell_btn = QPushButton("Оплатить")
sell_btn.clicked.connect(buy_albums)
back_genre = QPushButton("Вернутся к жанрам")

delete_tresh = QPushButton("Обновить корзину")
delete_tresh.clicked.connect(delete_tresh_now)
page_tresh_layout.addWidget(text_field)
page_tresh_layout.addWidget(sell_btn)
page_tresh_layout.addWidget(delete_tresh)
page_tresh_layout.addWidget(back_genre)
page_tresh.setLayout(page_tresh_layout)

# Страница регистрации пользователя

page_regisration = QWidget()
text_info = QLabel("Регистрация пользователя")
text_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
page_regisration_layout = QVBoxLayout()
input_phone = QLineEdit()
input_phone.setPlaceholderText("Введите номер телефона")
input_full_name = QLineEdit()
input_full_name.setPlaceholderText("Как к вам обращаться")
input_password = QLineEdit()
input_password.setPlaceholderText("Придумайте пароль")
appande_user = QPushButton("Зарегистрироваться")
appande_user.clicked.connect(take_user_data)

page_regisration_layout.addWidget(text_info)
page_regisration_layout.addWidget(input_phone)
page_regisration_layout.addWidget(input_full_name)
page_regisration_layout.addWidget(input_password)
page_regisration_layout.addWidget(appande_user)
page_regisration.setLayout(page_regisration_layout)

# Связывание листов
stacked_widget.addWidget(page_sign_up) # Страница регистрация
stacked_widget.addWidget(page_genre) # Страница с жанрами
stacked_widget.addWidget(page_hip_hop) # Страница с hip-hop
stacked_widget.addWidget(page_jazz) # Страница с jazz
stacked_widget.addWidget(page_rock) # Страница с rock
stacked_widget.addWidget(page_post_punk) #Страница с post-punk
stacked_widget.addWidget(page_tresh) # Страница с корзиной
stacked_widget.addWidget(page_regisration) # Страница с регистрацией 

main_layout.addWidget(stacked_widget)
central_widget.setLayout(main_layout)
main_window.setCentralWidget(central_widget)

# Переход на следующую страницу
def switch_page_sign_up():
    stacked_widget.setCurrentIndex(1)

def switch_page_hip_hop():
    populate_hip_hop_creators()  # Заполняем список исполнителей при переходе
    combo_album_hip_hop.clear()  # Очищаем список альбомов
    combo_album_hip_hop.addItem("Выберите альбом")
    stacked_widget.setCurrentIndex(2)

def switch_page_jazz():
    jazz_creator()
    combo_album_jazz.clear()
    combo_album_jazz.addItem("Выберите альбом")
    stacked_widget.setCurrentIndex(3)

def switch_page_rock():
    rock_creator()
    combo_album_rock.clear()
    combo_album_rock.addItem("Выберите альбом")
    stacked_widget.setCurrentIndex(4)

def switch_page_post_punk():
    post_punk_creator()
    combo_album_post_punk.clear()
    combo_album_post_punk.addItem("Выберите альбом")
    stacked_widget.setCurrentIndex(5)

def back_sign_up():
    INFO.clear()
    stacked_widget.setCurrentIndex(0)

def go_tresh():
    update_tresh_display()
    stacked_widget.setCurrentIndex(6)

def go_registrtion():
    stacked_widget.setCurrentIndex(7)

# Связываем кнопки к их функциям
button_to_page_genre.clicked.connect(find_user)
hip_hop_button.clicked.connect(switch_page_hip_hop)
jazz_button.clicked.connect(switch_page_jazz)
rock_button.clicked.connect(switch_page_rock)
post_punk_button.clicked.connect(switch_page_post_punk)
back_genre_hip_hop.clicked.connect(switch_page_sign_up)
back_genre_jazz.clicked.connect(switch_page_sign_up)
back_genre_post_punk.clicked.connect(switch_page_sign_up)
back_genre_rock.clicked.connect(switch_page_sign_up)
out_account.clicked.connect(back_sign_up)
back_genre.clicked.connect(switch_page_sign_up)
tresh.clicked.connect(go_tresh)
button_registration.clicked.connect(go_registrtion)

# Запуск приложения
main_window.show()
app.exec()


