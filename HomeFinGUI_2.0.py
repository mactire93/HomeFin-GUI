from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import sqlite3
import datetime

root = Tk()
root.title("Home Fin 2022")
root.geometry("300x300")

def update_balance():

    sum_incomes()
    sum_expenses()

    balance = income_balance - expenses_balance

    balance_text.delete('1.0', END)
    # insert balance with 2 decimal place
    balance_text.insert('1.0', ('%.2f'% balance))
    balance_text.insert('2.0', " zł")

def sum_incomes():
    global income_balance
    conn = sqlite3.connect('homefingui.db')
    c = conn.cursor()

    c.execute("SELECT round(SUM(wartość), 2) FROM {}".format(name_income_table))
    
    income_balance = c.fetchone()[0]

    # commit command
    conn.commit()
    # close connection
    conn.close()

    try:
        income_text.delete('1.0', END)
        income_text.insert('1.0', income_balance)
        income_text.insert('2.0', ' zł')
    except:
        income_balance = 0
        income_text.delete('1.0', END)
        income_text.insert('1.0', income_balance)
        income_text.insert('2.0', ' zł')

def sum_expenses():
    
    global expenses_balance

    conn = sqlite3.connect('homefingui.db')
    c = conn.cursor()

    c.execute("SELECT round(SUM(cena), 2) FROM {}".format(name_of_sheet))

    expenses_balance = c.fetchone()[0]

    # commit command
    conn.commit()
    # close connection
    conn.close()
    try:
        expenses_text.delete('1.0', END)
        expenses_text.insert('1.0', expenses_balance)
        expenses_text.insert('2.0', " zł")
    except:
        expenses_balance = 0
        expenses_text.delete('1.0', END)
        expenses_text.insert('1.0', expenses_balance)
        expenses_text.insert('2.0', " zł")

    
def save_income():

    conn = sqlite3.connect('homefingui.db')
    c = conn.cursor()

    if (incomes_source.get() == '' or incomes_source.get() is None) or (incomes_value.get() == '' or incomes_value.get() is None):
        messagebox.showerror("Niepełne dane","Żadne z okien nie może być puste!")
        return
    else:
        c.execute("INSERT INTO {} VALUES (:źródło, :wartość)".format(name_income_table),
                 {
                    'źródło': incomes_source.get(),
                    'wartość': ('%.2f'% float(incomes_value.get())) + ' zł'#insert value with 2 decimal place
                 })
                
        # commit command
        conn.commit()
        # close connection
        conn.close()

        #Clear tree window for update
        for item in income_tree.get_children():
            income_tree.delete(item)

        incomes_source.delete(0, END)
        incomes_value.delete(0, END)

    query_income_db()
    #sum_incomes()
    update_balance()


def open_sheet():
    global name_of_sheet
    global name_income_table
    name_of_sheet = "'"+sheet_name.get()+"'"
    name_income_table = "'"+sheet_name.get()+" inc_omes'"
    enter_billing()
    query_database()
    query_income_db()
    #sum_expenses()
    #sum_incomes()
    update_balance()

def save():

    conn = sqlite3.connect('homefingui.db')
    c = conn.cursor()

    if (category.get() == '' or category.get() is None) or (name.get() == '' or name.get() is None) or (price.get() == '' or price.get() is None):
        messagebox.showerror("Niepełne dane","Żadne z okien nie może być puste!")
        return
    else:
        c.execute("INSERT INTO {} VALUES (:data, :kategoria, :nazwa, :cena)".format(name_of_sheet),
                 {
                    'data': datetime.date.today(),
                    'kategoria': category.get(),
                    'nazwa': name.get(),
                    'cena': ('%.2f'% float(price.get())) + ' zł'#insert price with 2 decimal place
                 })
                
        # commit command
        conn.commit()
        # close connection
        conn.close()

        #Clear tree window for update
        for item in main_tree.get_children():
            main_tree.delete(item)

        #clear entry boxes
        category.delete(0, END)
        name.delete(0, END)
        price.delete(0, END)
    
    query_database()
    #sum_expenses()
    update_balance()

def query_income_db():
    global records
    
    conn = sqlite3.connect('homefingui.db')
    c = conn.cursor()

    c.execute("SELECT rowid, źródło, wartość FROM {}".format(name_income_table))
    records = c.fetchall()

    # insert data from db to main tree
    count = 0
    for record in records:
        income_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]))
        count += 1

    conn.commit()
    conn.close
    

def query_database():

    global records
    conn = sqlite3.connect('homefingui.db')
    c = conn.cursor()

    c.execute("SELECT rowid, data, kategoria, nazwa, cena FROM {}".format(name_of_sheet))
    records = c.fetchall()

    # insert data from db to main tree
    count = 0
    for record in records:
        main_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2], record[3], record[4]))
        count += 1

    conn.commit()
    conn.close

def validate(string):
    '''
    check if the value is integer or float
    '''
    regex = re.compile(r"(\+|\-)?[0-9.]*$")
    result = regex.match(string)
    return (string == ""
            or (string.count('+') <= 1
                and string.count('-') <= 1
                and string.count('.') <= 1
                and string[0].isdigit()
                and result is not None
                and result.group(0) != ""))

def on_validate(P):
    return validate(P)

def select_record(e):

    global id_contain
    # focus on main tree record
    selected = main_tree.focus()

    # add focused record on value and add values to id_contain
    values = main_tree.item(selected, 'values')
    try:
        id_contain = values[0]
    except:
        return

def remove_expenses():
    # try delete one position from tree. Except - do nothing.
    try:
        # select record from tree and delete it and delete record from db
        x = main_tree.selection()[0]
        main_tree.delete(x)

        conn = sqlite3.connect('homefingui.db')
        c = conn.cursor()

        c.execute("DELETE from {} WHERE oid=(:id)".format(name_of_sheet),
                  {
                    'id': id_contain
                  })
        conn.commit()
        conn.close
        update_balance()
    except:
        return

def select_income(e):
    global income_id

    selected_income = income_tree.focus()
    values = income_tree.item(selected_income, 'values')
    try:
        income_id = values[0]
    except:
        return

def remove_incomes():
    try:
        # select record from tree and delete it and delete record from db
        x = income_tree.selection()[0]
        income_tree.delete(x)

        conn = sqlite3.connect('homefingui.db')
        c = conn.cursor()

        c.execute("DELETE from {} WHERE oid=(:id)".format(name_income_table),
                  {
                    'id': income_id
                  })
        conn.commit()
        conn.close
        update_balance()
    except:
        return



def enter_billing():
    """
    Make window where can you add new billing to exist sheet (table)
    """
    # global function
    global new_billing
    global category
    global name
    global price
    global main_tree
    global income_tree
    global incomes_source
    global incomes_value
    global income_text
    global expenses_text
    global balance_text
    
    # display billing window
    new_billing = Tk()
    new_billing.title(sheet_name.get())
    new_billing.geometry("800x600")

    # create frames
    billing_frame = LabelFrame(new_billing, text="Wprowadź pozycje")
    billing_frame.grid(row=0, column=0, padx=2.5, pady=2.5)
    
    incomes_frame = LabelFrame(new_billing, text="Przychody")
    incomes_frame.grid(row=0, column=1)

    balance_frame = LabelFrame(new_billing, text="Podsumowanie")
    balance_frame.grid(row=2, column=0, padx=2.5, pady=2.5)

    #create text boxes
    category = Entry(billing_frame, width=20)
    category.grid(row=1, column=0, padx=20)

    name = Entry(billing_frame, width=20)
    name.grid(row=1, column=1, padx=20)

    price = Entry(billing_frame, width=20, validate="key")
        # for on_validate:
    vcmd = (price.register(on_validate), '%P')
    price.config(validatecommand=vcmd)
    price.grid(row=1, column=2, padx=20)

    incomes_source = Entry(incomes_frame, width=20)
    incomes_source.grid(row=1, column=0, padx=5)

    incomes_value = Entry(incomes_frame, width=20, validate="key")
    vcmd =(incomes_value.register(on_validate), '%P')
    incomes_value.config(validatecommand=vcmd)
    incomes_value.grid(row=1, column=1, padx=5)

    #Create text box labels
    category_label = Label(billing_frame, text="Kategoria")
    category_label.grid(row=0, column=0)

    name_label = Label(billing_frame, text="Nazwa")
    name_label.grid(row=0, column=1)

    price_label = Label(billing_frame, text="Cena")
    price_label.grid(row=0, column=2)

    incomes_source_label= Label(incomes_frame, text="Źródło")
    incomes_source_label.grid(row=0, column=0)

    incomes_value_label= Label(incomes_frame, text="Wartość")
    incomes_value_label.grid(row=0, column=1)

    income_label_02 = Label(balance_frame, text="Przychody")
    income_label_02.grid(row=0, column = 0)

    expenses_label = Label(balance_frame, text="Wydatki")
    expenses_label.grid(row=1, column = 0)

    balance_label = Label(balance_frame, text="Bilans")
    balance_label.grid(row=2, column=0)

    # Create text widget

    income_text = Text(balance_frame, width=20, height=1)
    income_text.grid(row=0, column=1)

    expenses_text = Text(balance_frame, width=20, height=1)
    expenses_text.grid(row=1, column=1)

    balance_text = Text(balance_frame, width=20, height=1)
    balance_text.grid(row=2, column=1)

    # create buttons
    save_button = Button(billing_frame, text="Zapisz", command=save)
    save_button.grid(row=2,column=0, pady=5)

    save_incomes = Button(incomes_frame, text="Zapisz", command=save_income)
    save_incomes.grid(row=2,column=0, pady=5)

    delete_button = Button(billing_frame, text="Usuń rekord", command=remove_expenses)
    delete_button.grid(row=2,column=1, pady=5)

    delete_income_btn = Button(incomes_frame, text="Usuń przychód", command=remove_incomes)
    delete_income_btn.grid(row=2, column=1, pady=5)

    # Create tree
    
    # create and configure tree frame
    main_tree_frame = LabelFrame(new_billing, text="Twoje wydatki")
    main_tree_frame.grid(row=1, column=0, ipadx=10, ipady=2.5, padx=2.5, pady=2.5)
    
    # add scrollbar to frame
    main_tree_scroll = Scrollbar(main_tree_frame)
    main_tree_scroll.pack(side=RIGHT, fill=Y)
    
    # add treeview to frame
    main_tree=ttk.Treeview(main_tree_frame, yscrollcommand=main_tree_scroll.set)
    main_tree['columns']=("Id","Data","Kategoria", "Nazwa", "Cena")
    
    # configure columns in treeview
    main_tree.column("#0", width=0, stretch=NO)
    main_tree.column("Id", anchor=W, width=40)
    main_tree.column("Data", anchor=W, width=80)
    main_tree.column("Kategoria", anchor=W, width=120)
    main_tree.column("Nazwa", anchor=CENTER, width=120)
    main_tree.column("Cena", anchor=W, width=80)
    
    # configure headings on columns
    main_tree.heading("#0", text="Label", anchor=W)
    main_tree.heading("Id", text="Id", anchor=W)
    main_tree.heading("Data", text="Data", anchor=W)
    main_tree.heading("Kategoria", text="Kategoria", anchor=W)
    main_tree.heading("Nazwa", text="Nazwa", anchor=CENTER)
    main_tree.heading("Cena", text="Cena", anchor=W)

    #pack treeview on frame
    main_tree.pack()
    
    # configure scrollbar
    main_tree_scroll.config(command=main_tree.yview)

    # Bind the treeview
    main_tree.bind("<ButtonRelease-1>", select_record)
    


    # create income tree
    # tree frame
    income_tree_frame = LabelFrame(new_billing, text="Spis przychodów")
    income_tree_frame.grid(row=1, column=1, ipadx=10, ipady=2.5, padx=2.5, pady=2.5)
    # scrollbar
    income_tree_scroll = Scrollbar(income_tree_frame)
    income_tree_scroll.pack(side=RIGHT, fill=Y)
    # tree
    income_tree=ttk.Treeview(income_tree_frame, yscrollcommand=income_tree_scroll.set)
    income_tree['columns']=("Id","Źródło","Wartość")
    # columns
    income_tree.column("#0", width=0, stretch=NO)
    income_tree.column("Id", anchor=W, width=40)
    income_tree.column("Źródło", anchor=W, width=100)
    income_tree.column("Wartość", anchor=W, width=100)
    # headings
    income_tree.heading("#0", text="Label", anchor=W)
    income_tree.heading("Id", text="Id", anchor=W)
    income_tree.heading("Źródło", text="Źródło", anchor=W)
    income_tree.heading("Wartość", text="Wartość", anchor=W)
    # pack tree in frame and configure scrollbar
    income_tree.pack()
    income_tree_scroll.config(command=income_tree.yview)

    # Bind the treeviev
    income_tree.bind("<ButtonRelease-1>", select_income)

    

def new_table():
    """
    Create a new table with choosen name
    """
    # Create variable with name of sheet and add single quotes to make table name with spaces
    global name_of_sheet
    global name_income_table
    
    name_of_sheet = "'"+sheet_name.get()+"'"
    name_income_table = "'"+sheet_name.get()+" inc_omes'"
    # connect exist db or make new db
    try:
        conn = sqlite3.connect('homefingui.db')
        c = conn.cursor()
        create_table= "CREATE TABLE {}(data, kategoria, nazwa, cena)".format(name_of_sheet)
        c.execute(create_table)

        create_income_table= "CREATE TABLE {}(źródło, wartość)".format(name_income_table)
        c.execute(create_income_table)

        # commit command
        conn.commit()
        # close connection
        conn.close()

        enter_billing()
        new_sheet.destroy()
    except:
        messagebox.showerror("Błędna nazwa!","Tabela o takiej nazwie już istnieje!")

    

def make_new_sheet():
    """
    Create new window to make and save new table
    """
    global new_sheet
    new_sheet = Tk()
    new_sheet.title("Nowy okres rozliczeniowy")
    new_sheet.geometry("250x150")

    # create global function
    global sheet_name

    # Create a text boxes
    sheet_name = Entry(new_sheet, width=30)
    sheet_name.grid(row=0, column=1, padx=20)
    # Create text box labels
    sheet_name_label = Label(new_sheet, text="Nazwa")
    sheet_name_label.grid(row=0, column=0)
    # Create a 'create sheet' button
    create_sheet_button = Button(new_sheet, text="Stwórz", command=new_table)
    create_sheet_button.grid(row=1,column=1, columnspan=1, pady=10,padx=10, ipadx=60)

def query_db_names():

    global options
    conn = sqlite3.connect('homefingui.db')
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' and name NOT LIKE '%inc_omes';")
    # search for the name of tables which do not have 'inc_omes' in the second part of their name
    results = c.fetchall()
    options = []

    for result in results:
        options.extend(result)

    # commit command
    conn.commit()
    # close connection
    conn.close()
    
    

def open_sheet_window():
    """
    Open exist sheet
    """
    try:
        global new_sheet
        new_sheet = Tk()
        new_sheet.title("Otwórz okres rozliczeniowy")
        new_sheet.geometry("200x150")

        # create global function
        global sheet_name

        # Create comboboxes
        query_db_names()

        sheet_name = ttk.Combobox(new_sheet, value=options)
        sheet_name.current(0)
        sheet_name.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        
        # Create a 'open sheet' button
        create_sheet_button = Button(new_sheet, text="Otwórz", command=open_sheet)
        create_sheet_button.grid(row=1, column=1, columnspan=1, pady=10, padx=10, ipadx=60)
    except:
        messagebox.showerror("Brak rozliczeń","Brak rozliczeń!")
        new_sheet.destroy()
        return


# Create 'New' button

new_button = Button(root, text="Nowy arkusz", command=make_new_sheet)
new_button.grid(row=0,column=0, columnspan=2,pady=10,padx=10, ipadx=100)

open_button = Button(root, text="Otwórz arkusz", command=open_sheet_window)
open_button.grid(row=1,column=0,columnspan=2,pady=10,padx=10, ipadx=100)

root.mainloop()
