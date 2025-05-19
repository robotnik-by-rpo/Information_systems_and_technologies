# GUI для работников компании
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, 
                               QVBoxLayout, QWidget, QStackedWidget, QComboBox, QMessageBox)
import sys
from PySide6.QtCore import Qt

from PySide6.QtGui import QIntValidator
from sql_vynil import *

def find_user():
    code = input_number_sign_up.text()
    pas = input_password_sign_up.text().strip()
    
    res = cursor.execute(f'''SELECT id_employee FROM Employees 
                         WHERE code_employee = ? AND password = ? ''',(code,pas)).fetchone()
    if res is not None:
        go_menu()
        input_number_sign_up.clear()
        
        input_password_sign_up.clear()
    else:
        QMessageBox.warning(main_window, "Ошибка", "Проверьте данные")

def load_suppliers():
   
    supplier_combo.clear()
    supplier_combo.addItem("Выберите поставщика", None)
    suppliers = cursor.execute("SELECT id_supplier, name_supplier FROM Suppliers").fetchall()
    for supplier in suppliers:
        supplier_combo.addItem(supplier[1], supplier[0])

def load_branches():
    
    branch_combo.clear()
    branch_combo.addItem("Выберите филиал", None)
    branches = cursor.execute("SELECT id_branch, address FROM Branch_stores").fetchall()
    for branch in branches:
        branch_combo.addItem(branch[1], branch[0])

def load_creators_for_serial():
   
    all_creator.clear()
    all_creator.addItem("Выберите исполнителя", None)
    creators = cursor.execute("SELECT id_creator, name_creator FROM Creators").fetchall()

    for creator in creators:
        all_creator.addItem(creator[1], creator[0])

def load_albums_for_serial(creator_id):
    
    all_album.clear()
    all_album.addItem("Выберите альбом", None)
    if creator_id:
        albums = cursor.execute("SELECT id_album, name_album FROM Albums WHERE id_creator = ?", (creator_id,)).fetchall()
        
        for album in albums:
            all_album.addItem(album[1], album[0])

def add_serial_number_to_db():
   
    serial_number = input_serial_number.text().strip()
    if len(serial_number) < 8:
        QMessageBox.warning(main_window, "Ошибка", "Серийный номер должен содержать 8 символов")
        return
    album_id = all_album.currentData()
    supplier_id = supplier_combo.currentData()
    branch_id = branch_combo.currentData()
    price = input_price.text().strip()
    
    # Проверка заполнения полей
    if not serial_number:
        QMessageBox.warning(main_window, "Ошибка", "Введите серийный номер")
        return
    if not album_id:
        QMessageBox.warning(main_window, "Ошибка", "Выберите альбом")
        return
    if not supplier_id:
        QMessageBox.warning(main_window, "Ошибка", "Выберите поставщика")
        return
    if not branch_id:
        QMessageBox.warning(main_window, "Ошибка", "Выберите филиал")
        return
    if not price or not price.isdigit():
        QMessageBox.warning(main_window, "Ошибка", "Введите корректную цену")
        return
    
    existing_serial = cursor.execute("SELECT id_number FROM Serial_numbers WHERE serial_number = ?", 
                                   (serial_number,)).fetchone()
    if existing_serial:
        QMessageBox.warning(main_window, "Ошибка", "Такой серийный номер уже существует в базе данных")
        return

    try:
        cursor.execute('''INSERT INTO Serial_numbers 
                       (id_supplier, id_album, id_branch, state, serial_number, price) 
                       VALUES (?, ?, ?, 'в продаже', ?, ?)''',
                       (supplier_id, album_id, branch_id, serial_number, int(price)))
        connection.commit()
        QMessageBox.information(main_window, "Успех", "Серийный номер добавлен")
        input_serial_number.clear()
        input_price.clear()
    except:
        QMessageBox.critical(main_window, "Ошибка", "Не удалось добавить серийный номер")

def go_menu():
    input_creator.clear()
    input_album.clear()
    input_serial_number.clear()
    input_price.clear()
    stacked_widget.setCurrentIndex(1)

def go_sign_up():
    input_number_sign_up.clear()
    input_password_sign_up.clear()
    stacked_widget.setCurrentIndex(0)

def go_creator():
    input_creator.clear()
    combo_genre.setCurrentIndex(0)
    stacked_widget.setCurrentIndex(2)

def go_album():
    input_album.clear()
    creator_combo.setCurrentIndex(0)
    stacked_widget.setCurrentIndex(3)

def go_serial_number():
    input_serial_number.clear()
    input_price.clear()
    supplier_combo.setCurrentIndex(0)
    branch_combo.setCurrentIndex(0)
    all_creator.setCurrentIndex(0)
    all_album.setCurrentIndex(0)
    load_suppliers()
    load_branches()
    load_creators_for_serial()
    stacked_widget.setCurrentIndex(4)

def add_creator_to_db():
    creator_name = input_creator.text().strip()
    genre_id = combo_genre.currentData()
    
    if not creator_name:
        QMessageBox.warning(main_window, "Ошибка", "Введите имя музыканта")
        return
    if not genre_id:
        QMessageBox.warning(main_window, "Ошибка", "Выберите жанр")
        return
    
    existing_creator = cursor.execute("SELECT id_creator FROM Creators WHERE name_creator = ? AND id_genre = ?", 
                                    (creator_name, genre_id)).fetchone()
    if existing_creator:
        QMessageBox.warning(main_window, "Ошибка", "Такой музыкант уже существует в базе данных")
        return
        
    try:
        cursor.execute("INSERT INTO Creators (name_creator, id_genre) VALUES (?, ?)", 
                      (creator_name, genre_id))
        connection.commit()
        QMessageBox.information(main_window, "Успех", "Музыкант добавлен")
        input_creator.clear()
        load_creators()
    except:
        QMessageBox.critical(main_window, "Ошибка", "Не удалось добавить музыканта")

def add_album_to_db():
    album_name = input_album.text().strip()
    creator_id = creator_combo.currentData()
    
    if not album_name:
        QMessageBox.warning(main_window, "Ошибка", "Введите название альбома")
        return
    if not creator_id:
        QMessageBox.warning(main_window, "Ошибка", "Выберите исполнителя")
        return
     # Проверка на существование альбома
    existing_album = cursor.execute("SELECT id_album FROM Albums WHERE name_album = ? AND id_creator = ?", 
                                   (album_name, creator_id)).fetchone()
    if existing_album:
        QMessageBox.warning(main_window, "Ошибка", "Такой альбом уже существует в базе данных")
        return

    try:
        cursor.execute("INSERT INTO Albums (name_album, id_creator) VALUES (?, ?)", 
                      (album_name, creator_id))
        connection.commit()
        QMessageBox.information(main_window, "Успех", "Альбом добавлен")
        input_album.clear()
    except:
        QMessageBox.critical(main_window, "Ошибка", f"Не удалось добавить альбом")

# Функция для загрузки исполнителей в ComboBox
def load_creators():
    creator_combo.clear()
    creator_combo.addItem("Выберите исполнителя", None)
    creators = cursor.execute("SELECT id_creator, name_creator FROM Creators").fetchall()
    for creator in creators:
        creator_combo.addItem(creator[1], creator[0])

app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Baudlier's vinyl for employees")
main_window.setFixedSize(680,480)

all_album = QComboBox()

central_widget = QWidget()
main_layout = QVBoxLayout()
stacked_widget = QStackedWidget()

# Страница входа в систему 
page_sign_up = QWidget()
page_sign_up_layout = QVBoxLayout()

label_sign_up = QLabel("Страница входа в систему")
label_sign_up.setAlignment(Qt.AlignmentFlag.AlignCenter)
input_number_sign_up = QLineEdit()
input_number_sign_up.setPlaceholderText("Введите номер сотрудника")

input_password_sign_up = QLineEdit()
input_password_sign_up.setPlaceholderText("Введите пароль")
button_to_page_work = QPushButton("Войти в систему")
button_to_page_work.clicked.connect(find_user)

page_sign_up_layout.addWidget(label_sign_up)
page_sign_up_layout.addWidget(input_number_sign_up)
page_sign_up_layout.addWidget(input_password_sign_up)
page_sign_up_layout.addWidget(button_to_page_work)
page_sign_up.setLayout(page_sign_up_layout)

# меню действий
page_menu = QWidget()
page_menu_layout= QVBoxLayout()

add_creator= QPushButton("Добавить музыканта")
add_creator.clicked.connect(go_creator)
add_album = QPushButton("Добавить альбом")
add_album.clicked.connect(go_album)
add_serial_number = QPushButton("Добавить серийный номер")
add_serial_number.clicked.connect(go_serial_number)
out_system = QPushButton("Выйти из системы")
out_system.clicked.connect(go_sign_up)

page_menu_layout.addWidget(add_creator)
page_menu_layout.addWidget(add_album)
page_menu_layout.addWidget(add_serial_number)
page_menu_layout.addWidget(out_system)
page_menu.setLayout(page_menu_layout)

# добавить автора

page_creator = QWidget()
page_creator_layout = QVBoxLayout()



input_creator = QLineEdit()
input_creator.setPlaceholderText("Введите имя музыканта")
page_creator_layout.addWidget(input_creator)


combo_genre = QComboBox()
combo_genre.addItem("Выберите жанр")
genres = cursor.execute("SELECT id_genre, name_genre FROM Genre").fetchall()
for genre in genres:
    combo_genre.addItem(genre[1], genre[0])
page_creator_layout.addWidget(combo_genre)

append_creator = QPushButton("Добавить автора")
append_creator.clicked.connect(add_creator_to_db)
page_creator_layout.addWidget(append_creator)

back_from_creator = QPushButton("Вернуться в меню")
back_from_creator.clicked.connect(go_menu)
page_creator_layout.addWidget(back_from_creator)
page_creator_layout.addWidget(input_creator)
page_creator_layout.addWidget(append_creator)
page_creator.setLayout(page_creator_layout)

# Добавить альбом
page_album = QWidget()
page_album_layout = QVBoxLayout()
creator_combo = QComboBox()
load_creators() 
input_album = QLineEdit()
input_album.setPlaceholderText("Введите название альбома")
append_album = QPushButton("Добавить альбом")
append_album.clicked.connect(add_album_to_db)
back_from_album = QPushButton("Вернутся в меню")
back_from_album.clicked.connect(go_menu)


page_album_layout.addWidget(creator_combo)
page_album_layout.addWidget(input_album)
page_album_layout.addWidget(append_album)
page_album_layout.addWidget(back_from_album)
page_album.setLayout(page_album_layout)

#Добавить серийный номер

page_serial_number = QWidget()
page_serial_number_layout = QVBoxLayout()

# Выбор поставщика
label_supplier = QLabel("Выберите поставщика:")
label_supplier.setAlignment(Qt.AlignmentFlag.AlignCenter)
page_serial_number_layout.addWidget(label_supplier)

supplier_combo = QComboBox()
load_suppliers()
page_serial_number_layout.addWidget(supplier_combo)



branch_combo = QComboBox()
load_branches()
page_serial_number_layout.addWidget(branch_combo)

all_creator = QComboBox()
all_creator.currentIndexChanged.connect(lambda: load_albums_for_serial(all_creator.currentData()))
load_creators_for_serial()
page_serial_number_layout.addWidget(all_creator)
page_serial_number_layout.addWidget(all_album)

# Поле для серийного номера
input_serial_number = QLineEdit()
input_serial_number.setPlaceholderText("Введите серийный номер")
input_serial_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
page_serial_number_layout.addWidget(input_serial_number)

# Поле для цены
input_price = QLineEdit()
input_price.setPlaceholderText("Введите цену")
input_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
input_price.setValidator(QIntValidator(1, 999999))  # Только цифры
page_serial_number_layout.addWidget(input_price)

# Кнопка добавления
append_serial = QPushButton("Добавить серийный номер")
append_serial.clicked.connect(add_serial_number_to_db)
page_serial_number_layout.addWidget(append_serial)

# Кнопка возврата
back_from_serial = QPushButton("Вернуться в меню")
back_from_serial.clicked.connect(go_menu)
page_serial_number_layout.addWidget(back_from_serial)


page_serial_number.setLayout(page_serial_number_layout)

# Добавление всех листов
stacked_widget.addWidget(page_sign_up)
stacked_widget.addWidget(page_menu)
stacked_widget.addWidget(page_creator)
stacked_widget.addWidget(page_album)
stacked_widget.addWidget(page_serial_number)

main_layout.addWidget(stacked_widget)
central_widget.setLayout(main_layout)
main_window.setCentralWidget(central_widget)


# Запуск приложения
main_window.show()
app.exec()