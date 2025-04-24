# Весь интерфейс в этом файле 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import req_sql
from datetime import date


cart_items = []
CNT_ITEM_SQL = []
ORDER_SQL = []
now = date.today()

# функция выводящая ошибку 
def error_gui():
    messagebox.showerror("Ошибка", "Произошла ошибка! Проверьте данные.")
    update_list()
    update_trash()

# функция берет информацию сколько продукта осталось
def how_many_have(product):
    req_str = f'''SELECT quantity FROM products WHERE name_product = '{product}' '''
    print(req_sql.bakery_sql(req_str))
    return req_sql.bakery_sql(req_str)[0][0]

# функция по имени продукта берет его id
def id_by_name(product):
    req_str= f'''SELECT id_product FROM products WHERE name_product = '{product}' '''
    return req_sql.bakery_sql(req_str)[0][0]

# функция оформляет чек в файл
def buy_in_trash():
    if len(ORDER_SQL) != 0 and len(CNT_ITEM_SQL) != 0:
        req_sql.create_check_in_file(now,ORDER_SQL,CNT_ITEM_SQL)
        update_trash()
        update_list()
    else:
        error_gui()

# Функция обновляет корзину до исходного значения
def update_trash():
    cart_items.clear()
    CNT_ITEM_SQL.clear()
    ORDER_SQL.clear()
    result_label.config(text="")

# функция отправляет данные в корзину
def save_in_sql():
    global cart_items
    
    # Получаем данные из всех списков и полей ввода
    bread = combo_bread.get()
    bread_qty = entry_bread.get()
    bakery = combo_bakery.get()
    bakery_qty = entry_bakery.get()
    cake = combo_cake.get()
    cake_qty = entry_cake.get()
    snack = combo_snake.get()
    snack_qty = entry_snake.get()
    drink = combo_drinks.get()
    drink_qty = entry_drinks.get()
    
    # Добавляем в корзину только если выбран продукт и указано непревосходящее количество продукта
    if bread != "" and bread_qty:
        if how_many_have(bread)>int(bread_qty):
            cart_items.append((bread, bread_qty))
            ORDER_SQL.append(id_by_name(bread))
            CNT_ITEM_SQL.append(int(bread_qty))
        else:
            error_gui()

    if bakery != "" and bakery_qty:
        if how_many_have(bakery)>int(bakery_qty):
            cart_items.append((bakery, bakery_qty))
            ORDER_SQL.append(id_by_name(bakery))
            CNT_ITEM_SQL.append(int(bakery_qty))
        else:
            error_gui()

    if cake != "" and cake_qty:
        if how_many_have(cake) > int(cake_qty):
            cart_items.append((cake, cake_qty))
            ORDER_SQL.append(id_by_name(cake))
            CNT_ITEM_SQL.append(int(cake_qty))
        else:
            error_gui()

    if snack != "" and snack_qty:
        if how_many_have(snack) > int(snack_qty):
            cart_items.append((snack, snack_qty))
            ORDER_SQL.append(id_by_name(snack))
            CNT_ITEM_SQL.append(int(snack_qty))
        else:
            error_gui()

    if drink != "" and drink_qty:
        if how_many_have(drink) > int(drink_qty):
            cart_items.append((drink, drink_qty))
            ORDER_SQL.append(id_by_name(drink))
            CNT_ITEM_SQL.append(int(drink_qty))
        else:
            error_gui()

    print(ORDER_SQL)
    print(CNT_ITEM_SQL)
    update_cart_display()

# Передаем текст в корзину
def update_cart_display():
    cart_text = "Корзина:\n"
    for item, qty in cart_items:
        cart_text += f"{item}: {qty} шт.\n"
    result_label.config(text=cart_text)

# функция обновляет выпадающие списки и поля ввода
def update_list():
    global cart_items

    # Сбрасываем комбобоксы до исходников
    combo_bread.set("")
    combo_bakery.set("")
    combo_cake.set("")
    combo_snake.set("")
    combo_drinks.set("")
    
    # Очищаем поля ввода 
    entry_bread.delete(0, END)
    entry_bakery.delete(0, END)
    entry_cake.delete(0, END)
    entry_snake.delete(0, END)
    entry_drinks.delete(0, END)

# Функция где собран весь интерфейс и рабочий билд
def main_gui():
    # объявление переменных
    global combo_bakery, combo_bread, combo_cake, combo_drinks, combo_snake
    global entry_bakery, entry_bread, entry_cake, entry_drinks, entry_snake, result_label

    # Создание gui
    root = Tk()
    root['bg'] = "#FEE3A2"
    root.title('Пекарня "Съешь ещё этих мягких французских булок да выпей чаю"')
    root.geometry('640x480')
    root.resizable(False, False)

    button_frame = Frame(root, bg="#FEE3A2")
    button_frame.grid(row=5, column=0, columnspan=4, pady=10,padx = 50)

    # Выпадающие списки
    combo_bread = ttk.Combobox(
        root,
        values = ["Багет","Пан-де-кампань","Пан-де-сель","Пан-комплет","Фюгасс"],
        state = "readonly",
        width = 25,
        height = 15
    )
    combo_bread.set("")
    combo_bread.grid(row = 0, column = 0, padx = 10, pady = 10)
    entry_bread = Entry(root,width = 7)
    entry_bread.grid(row=0,column=1, padx = 10, pady = 10)
    
    combo_bakery = ttk.Combobox(
        root,
        values = ["Круассан","Пэн-о-шоколад","Шуссон-о-пом","Бриошь","Эклер"],
        state = "readonly",
        width = 25,
        height = 15
    )
    combo_bakery.set("")
    combo_bakery.grid(row = 1, column = 0, padx = 10, pady = 10)
    entry_bakery = Entry(root,width = 7)
    entry_bakery.grid(row=1,column=1, padx = 10, pady = 10)

    combo_cake = ttk.Combobox(
        root,
        values = ["Тарт-о-ситрон","Тарт-о-пом","Миллефёй","Макарон","Опера"],
        state = "readonly",
        width = 25,
        height = 15
        )
    combo_cake.set("")
    combo_cake.grid(row=2,column=0,padx = 10, pady = 10)
    entry_cake = Entry(root,width = 7)
    entry_cake.grid(row=2,column=1,padx = 10, pady = 10)

    combo_snake = ttk.Combobox(root,
        values = ["Киш",'Сэндвичи','Фокачча'],
        state = "readonly",
        width = 25,
        height = 15
        )
    combo_snake.set("")
    combo_snake.grid(row=3,column=0,padx = 10, pady = 10)
    entry_snake = Entry(root,width = 7)
    entry_snake.grid(row=3,column=1,padx = 10, pady = 10)

    combo_drinks = ttk.Combobox(root,
        values = ['Американо','Эспрессо','Капучино','Латте','Моккачино',
                  'Флэт уайт','Двойной эсперессо','Раф','Макиато','Зеленый чай','Черный чай'],
        state = "readonly",
        width = 25,
        height = 15
        )
    combo_drinks.set("")
    combo_drinks.grid(row=4,column=0,padx = 10, pady = 10)
    entry_drinks = Entry(root,width = 7)
    entry_drinks.grid(row=4,column=1,padx = 10, pady = 10)

    style_b = ttk.Style()
    style_b.theme_use("clam")
    style_b.configure("Custom.TButton", background="#F3C301", foreground="black")
    style_b.map("Custom.TButton",
          background=[("active", "#D4A017")],  # Цвет при нажатии
          foreground=[("active", "white")])
    
    # Кнопки
    save_button = ttk.Button(button_frame, text="В корзину", style= "Custom.TButton",command=save_in_sql)
    save_button.grid(row=0,column=0,padx = 5, pady = 10)
    
    update_button = ttk.Button(button_frame, text="Обновить выпадающие списки", style= "Custom.TButton",command=update_list)
    update_button.grid(row=0,column=1,padx = 5, pady = 10)

    update_trash_btn = ttk.Button(button_frame, text = "Обновить корзину",style= "Custom.TButton",command = update_trash)
    update_trash_btn.grid(row=0, column = 2, padx = 5, pady = 10)

    buy_btn = ttk.Button(button_frame, text = "Оплатить",style= "Custom.TButton",command = buy_in_trash)
    buy_btn.grid(row=0, column = 3, padx = 5, pady = 10)

    # Окно с текстом корзины
    result_label = ttk.Label(root, text="", font=('Arial', 10),width = 25)
    result_label.grid(row=9,column=0,padx = 10, pady = 5)

    root.mainloop()
    return "success"

if __name__=="__main__":
    
    main_gui()
    
    