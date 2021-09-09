from tkinter import *
from tkinter import messagebox
import sqlite3, datetime, calendar, config

# Global variable
global logged_in_user

def master_frame():
    root.geometry("750x450")
    # frame
    global initial_frame
    
    initial_frame = LabelFrame(root, padx=5, pady=5)
    initial_frame.pack(padx=10, pady=10)


    # Labels
    username_label = Label(initial_frame, text="User Name", width=12, font=('Arial',10,'bold'), justify=CENTER)
    username_label.grid(row=1, column=0, pady=(5, 2))
    password_label = Label(initial_frame, text="Password", width=12, font=('Arial',10,'bold'), justify=CENTER)
    password_label.grid(row=2, column=0, pady=(2, 5))
    text = "_____________________________or_____________________________"
    label = Label(initial_frame, text=text, width=34, font=('Arial',10,'bold'), justify=CENTER)
    label.grid(row=8, column=0, columnspan=2, pady=2)

    # Entry Boxes
    entry = Entry(initial_frame, width=32, fg='white', bg='black', font=('Arial',12,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, padx=10, pady=25)
    entry.insert(0, 'Login to continue')
    username_entry = Entry(initial_frame, width=20, borderwidth=3, font=("Arial", 13))
    username_entry.grid(row=1, column=1, pady=(5, 2), padx=(3, 50))
    password_entry = Entry(initial_frame, width=20, borderwidth=3, show="*", font=("Arial", 13))
    password_entry.grid(row=2, column=1, pady=(2, 5), padx=(3, 50))

    # Buttons        
    user_login_button = Button(initial_frame, text="Sign In", font=('Comic Sans MS',10),
                                command=lambda: userSignIn(username_entry.get(), password_entry.get()),
                                activebackground='gray', activeforeground='white', bg='#59BE59', fg='white', borderwidth=3)
    user_login_button.grid(row=6, column=0, columnspan=2, ipadx=140, pady=(25, 5))
    admin_login_button = Button(initial_frame, text="Sign In as Administrator", font=('Comic Sans MS',10),
                                command=lambda: adminSignIn(username_entry.get(), password_entry.get()),
                                activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    admin_login_button.grid(row=7, column=0, columnspan=2, ipadx=70, pady=(5, 5))
    signup_button = Button(initial_frame, text="Create New Account", font=('Comic Sans MS',10), command=signUp,
                            activebackground='gray', activeforeground='white', bg='#EEF74F', fg='black', borderwidth=3)
    signup_button.grid(row=9, column=0, columnspan=2, ipadx=85, pady=(10, 25))


# functions
def userFrame():
    # destroy initial frame
    initial_frame.destroy()

    # signup frame
    global user_frame
    user_frame = LabelFrame(root, padx=5, pady=5)
    user_frame.pack(padx=10, pady=10)
    
    # Entry
    entry = Entry(user_frame, width=32, fg='white', bg='black', font=('Arial',12,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, padx=10, pady=25)
    entry.insert(0, 'Welcome ' + logged_in_user[1])

    # buttons
    view_stocks_button = Button(user_frame, text="View Stocks", padx=10, font=('Comic Sans MS',10), command=lambda: viewStocksSummary(1),
                                activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    view_stocks_button.grid(row=1, column=0, columnspan=2, ipadx=110)
    limit_order_button = Button(user_frame, text="Limit Order settings", font=('Comic Sans MS',10), padx=10, command=lambda: displayOrders(1),
                                activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    limit_order_button.grid(row=2, column=0, columnspan=2, ipadx=79)
    portfolio_button = Button(user_frame, text="Portfolio", padx=10, font=('Comic Sans MS',10), command=displayPortfolio,
                              activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    portfolio_button.grid(row=3, column=0, columnspan=2, ipadx=123)
    transaction_history_button = Button(user_frame, text="Transactions History", padx=10, font=('Comic Sans MS',10), command=displayTransactions,
                                        activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    transaction_history_button.grid(row=4, column=0, columnspan=2, ipadx=76)
    cash_button = Button(user_frame, text="Deposit/Withdraw Cash", padx=10, font=('Comic Sans MS',10), command=DepositWithdraw,
                         activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    cash_button.grid(row=5, column=0, columnspan=2, ipadx=65)
    logout_button = Button(user_frame, text="Logout", padx=10, font=('Comic Sans MS',10), command=lambda: logout(0),
                           activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    logout_button.grid(row=6, column=0, columnspan=2, ipadx=132)


def displayOrders(frame_number):
    global order_frame
    if frame_number == 1:
        user_frame.destroy()
    elif frame_number == 2:
        order_frame.destroy()
    
    # limit order frame
    order_frame = LabelFrame(root, padx=5, pady=5)
    order_frame.pack(padx=10, pady=10)

    # Set Geometry
    root.geometry("1000x500")

    # Get all the limit orders for current user
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    orders = db.execute("""SELECT limit_orders.id, stocks.companyname, stocks.stockticker, limit_orders.price, limit_orders.quantity,  
                         limit_orders.expiry_time, limit_orders.cur_time, type
                         FROM stocks 
                         JOIN limit_orders ON limit_orders.stock_id = stocks.id
                         WHERE limit_orders.user_id = """ + str(logged_in_user[0])
                         + """ LIMIT 10""").fetchall()

    conn.commit()
    conn.close()

    # Entry
    entry = Entry(order_frame, width=74, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=10, pady = 20)
    entry.insert(0, "LIMIT ORDERS")
    
    entry_texts = ["S.NO", "COMPANY", "TICKER", "PRICE", "QTY", "EXP. DATE", "ORDER DATE", "TYPE"]
    for i in range(len(entry_texts)):
        if i == 0:
            e = Entry(order_frame, width=5, fg='white', bg='black', font=('Arial',9,'bold'), justify=CENTER)
        else:
            e = Entry(order_frame, width=13, fg='white', bg='black', font=('Arial',9,'bold'), justify=CENTER)
        e.grid(row=1, column=i)
        e.insert(0, entry_texts[i])

    for i in range(10):
        for j in range(9):
            if j == 0:
                e = Entry(order_frame, width=6, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                e.grid(row=i+2, column=j)
                e.insert(0, i + 1)
            elif j == 8:
                if i < len(orders):
                    view_button = Button(order_frame, text="Cancel Order", font=('Comic Sans MS',6), padx=7, fg = 'red',
                                        command=lambda i=i: cancelOrder(orders[i][0])) # send order id of the order to be cancelled
                    view_button.grid(row=i+2, column=j+1, padx=2)
            else:
                e = Entry(order_frame, width=15, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                e.grid(row=i+2, column=j)
                if i < len(orders):
                    e.insert(END, orders[i][j])

    # Buttons
    user_back_button = Button(order_frame, text="Back", font=('Comic Sans MS',10), padx=10,
                              activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,
                              command=lambda: userBack(3))
    user_back_button.grid(row=12, column=3, columnspan=3, pady=20, ipadx=60)


def cancelOrder(order_id):
    # Pop out confirmation message
    message = messagebox.askyesno("Confrimation", "Are you sure you want to cancel this order!")
    
    # Redirect user back to display limit orders if they select no
    if message == False:
        displayOrders(2)
    else:
        # Else delete the limit order
        conn = sqlite3.connect(config.DATABASE_PATH)
        db = conn.cursor()

        db.execute("DELETE FROM limit_orders WHERE id = " + str(order_id))

        conn.commit()
        conn.close()

    # Redirect user to display limit orders
        displayOrders(2)


def displayPortfolio():
    user_frame.destroy()
    global display_portfolio_frame
    display_portfolio_frame = LabelFrame(root, padx=5, pady=5)
    display_portfolio_frame.pack(padx=10, pady=10)
    
    # Set geometry of the window
    root.geometry("800x490")
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    # Get current Account balance
    data = db.execute("SELECT account_balance FROM registered_users WHERE id =" + str(logged_in_user[0])).fetchone()
    account_balance = round(data[0], 2)

    # fetch companyname, ticker and owned stock information from user_shares and stocks table
    data = db.execute("""SELECT stocks.companyname, stocks.stockticker, user_shares.Quantity 
                         FROM stocks 
                         JOIN user_shares ON user_shares.stock_id = stocks.id
                         WHERE user_shares.user_id = """ + str(logged_in_user[0]) + """
                         ORDER BY user_shares.Quantity DESC LIMIT 7""").fetchall()
    
    conn.commit()
    conn.close()

    # Entry
    # Heading
    entry = Entry(display_portfolio_frame, width=54, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=6, pady = 20)
    entry.insert(0, logged_in_user[1].upper() + "'S PORTFOLIO")

    # Cash Information
    entry = Entry(display_portfolio_frame, width=72, fg='white', bg='black', font=('Arial',10,'bold'), justify=CENTER)
    entry.grid(row=1, column=0, columnspan=6, pady=(0, 10))
    entry.insert(0, "ACCOUNT INFORMATION")
    
    label = Label(display_portfolio_frame, text=" : ", font=('Arial',10,'bold'))
    label.grid(row=2, column=3, pady=(10, 30))

    label_headings = ["ACCOUNT BALANCE ($)", account_balance]
    for i in range(2):
        if i == 0:
            entry = Entry(display_portfolio_frame, width=22, fg='white', bg='green', font=('Arial',10,'bold'), justify=CENTER)
            entry.grid(row=2, column=1, pady=(10, 30), columnspan=3)
            entry.insert(0, label_headings[i])
        else:
            entry = Entry(display_portfolio_frame, width=17, fg='green', font=('Arial',10, 'bold'), justify=LEFT)
            entry.grid(row=2, column=3, columnspan=2, pady=(10, 30), padx=(30, 25))
            entry.insert(0, label_headings[i])

    # Display Stock information
    entry = Entry(display_portfolio_frame, width=72, fg='white', bg='black', font=('Arial',10,'bold'), justify=CENTER)
    entry.grid(row=3, column=0, columnspan=6, pady=(0, 10))
    entry.insert(0, "STOCKS INFORMATION")
    
    # Display title
    label_headings = ["S.NO", "COMPANY NAME", "TICKER", "SHARES QTY"]
    for i in range(4):
        if i == 0:
            entry = Entry(display_portfolio_frame, width=7, fg='white', bg='black', font=('Arial',9,'bold'), justify=CENTER)
        else:
            entry = Entry(display_portfolio_frame, width=24, fg='white', bg='black', font=('Arial',9,'bold'), justify=CENTER)
        entry.grid(row=4, column=i + 1)
        entry.insert(1, label_headings[i])

    # Display owned stocks
    for i in range(7):
        for j in range(4):
            if j == 0: # For serial numbers
                entry = Entry(display_portfolio_frame, width=8, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                entry.grid(row=i+5, column=j + 1)
                entry.insert(0, i+1)
            else: # For data
                entry = Entry(display_portfolio_frame, width=27, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                entry.grid(row=i+5, column=j + 1)
                if i < len(data):
                    entry.insert(0, data[i][j - 1])

    # Button
    back_button = Button(display_portfolio_frame, text="Back", font=('Comic Sans MS',10),
                         activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,
                         command=lambda: userBack(5))
    back_button.grid(row=i+6, column=3, pady=20, ipadx=70)

def displayTransactions():
    user_frame.destroy()
    root.geometry("800x450")
    global display_trans_frame, logged_in_user
    display_trans_frame = LabelFrame(root, padx=5, pady=5)
    display_trans_frame.pack(padx=10, pady=10)

    # Get transaction details from database
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    # Get all the transactions 
    transactions = db.execute("""SELECT id, time, amount, type FROM transactions WHERE user_id = 
                              """ + str(logged_in_user[0]) + " ORDER BY time DESC LIMIT 10").fetchall()
                            
    conn.cursor()
    conn.close()

    # Entry
    # Main heading
    entry = Entry(display_trans_frame, width=51, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=4, pady = 20)
    entry.insert(0, "TRANSACTIONS HISTORY")

    # Display Headings
    label_headings = ["S.NO.", "TIME", "AMOUNT", "TYPE"]
    for i in range(4):
        if i == 0:
            entry = Entry(display_trans_frame, width=10, fg='white', bg='black', font=('Arial',10,'bold'), justify=CENTER)
        else:
            entry = Entry(display_trans_frame, width=19, fg='white', bg='black', font=('Arial',10,'bold'), justify=CENTER)
        entry.grid(row=1, column=i)
        entry.insert(0, label_headings[i])

    # Display transaction details
    for i in range(10):
        for j in range(4):
            if j == 0:
                entry = Entry(display_trans_frame, width=13, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                entry.grid(row=i+2, column=j)
                entry.insert(0, i+1)
            else:
                entry = Entry(display_trans_frame, width=24, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                entry.grid(row=i+2, column=j)
                if i < len(transactions):
                    entry.insert(0, transactions[i][j])

    # Label
    text = "Note: Transaction type starting with an '*' indicates that it resulted due to limit order completion"
    label = Label(display_trans_frame, text=text, font=('Comic Sans MS',8), fg='red')
    label.grid(row=i+3, column=0, columnspan=4, pady=(5, 10))

    # Button
    back_button = Button(display_trans_frame, text="Back", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,command=lambda: userBack(2))
    back_button.grid(row=i+4, column=1, columnspan=2, padx=(50, 0), pady=10, ipadx=80)


def viewStock(selected_stock):
    view_summary_frame.destroy()
    root.geometry("800x450")
    global view_stock_frame, logged_in_user
    view_stock_frame = LabelFrame(root, padx=5, pady=5)
    view_stock_frame.pack(padx=10, pady=10)
    
    # Display attributes of the selected stock
    # Entry
    # Main heading
    entry = Entry(view_stock_frame, width=38, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, pady=20)
    entry.insert(0, "TRADE STOCKS OF " + selected_stock[1].upper())
    
    label_headings = ["COMPANY", "TICKER", "CURRENT PRICE", "OPENING PRICE", "HIGH", "LOW", "VOLUME", "MARKET CAPITALIZATION"]
    n = len(selected_stock)
    for i in range(n - 1):
        entry = Entry(view_stock_frame, width=25, fg='white', bg='green', font=('Arial',10,'bold'), justify=CENTER)
        entry.grid(row=i+1, column=0)
        entry.insert(0, label_headings[i])

        entry = Entry(view_stock_frame, width=25, font=('Arial',10,'bold'), fg='green', justify=CENTER)
        entry.grid(row=i+1, column=1)
        entry.insert(0, str(selected_stock[i+1]))
    

    # Buttons
    # Buy button
    if selected_stock[7] ==0:  # if volume = 0, then disable the button
        buy_button = Button(view_stock_frame, text="Buy", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, state=DISABLED)
    else:
        buy_button = Button(view_stock_frame, text="Buy", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: buyStock(selected_stock, 1))
    buy_button.grid(row=n+2, column=0, pady=20, ipadx=91)
    
    # Sell button
    # Check if user has shares in this company
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    data = db.execute("SELECT * FROM user_shares WHERE user_id = ? AND stock_id = ?", (logged_in_user[0], selected_stock[0])).fetchone()

    conn.commit()
    conn.close()

    if not data: # If user doesn't own any shares in the company, disable the button
        sell_button = Button(view_stock_frame, text="Sell", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, state=DISABLED)
    else:
        sell_button = Button(view_stock_frame, text="Sell", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: sellStock(selected_stock, 1))
    sell_button.grid(row=n+2, column=1, pady=20, ipadx=90)
    
    back_button = Button(view_stock_frame, text="Back", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: backStock(1))
    back_button.grid(row=n+3, column=0, columnspan=2, pady=10, ipadx=202)


def sellStock(selected_stock, frame_number):
    if frame_number == 1:
        view_stock_frame.destroy()
    elif frame_number == 2:
        limit_order_frame.destroy()

    root.geometry("600x450")
    global sell_stock_frame
    sell_stock_frame = LabelFrame(root, padx=5, pady=5)
    sell_stock_frame.pack(padx=10, pady=10)

    # Get quantity of shares owned by the user
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    data = db.execute("SELECT * FROM user_shares WHERE user_id = ? AND stock_id = ?", (logged_in_user[0], selected_stock[0])).fetchone()

    conn.commit()
    conn.close()

    # Labels
    # Main heading
    entry = Entry(sell_stock_frame, width=38, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, pady = 20)
    entry.insert(0, "SELL SHARES OF " + selected_stock[1].upper())

    label_text = ["OWNED SHARES OF " + selected_stock[2], "QTY OF SHARES ", "MKT PRICE ($)"]
    for i in range(len(label_text)):
        label = Label(sell_stock_frame, text=label_text[i], font=('Arial',9,'bold'), pady=10, padx=10)
        label.grid(row=i+1, column=0)
    
    text="__________________________or__________________________"
    label = Label(sell_stock_frame, text=text, font=('Arial',9,'bold'), padx=10)
    label.grid(row=6, column=0, columnspan=2)

    # Entries
    available_quantity_entry = Entry(sell_stock_frame, width=20, font=('Arial',10,'bold'), justify=CENTER)
    available_quantity_entry.grid(row=1, column=1)
    available_quantity_entry.insert(0, data[3])
    quantity_entry = Entry(sell_stock_frame, width=20, font=('Arial',10,'bold'), justify=CENTER)
    quantity_entry.grid(row=2, column=1)
    price_entry = Entry(sell_stock_frame, width=20, font=('Arial',10,'bold'), justify=CENTER)
    price_entry.grid(row=3, column=1)
    price_entry.insert(0,selected_stock[3])

    # Buttons
    sell_button = Button(sell_stock_frame, text="Sell", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: sellfunction(selected_stock, int(quantity_entry.get())))
    sell_button.grid(row=4, column=0, columnspan=2, pady=(15, 5), ipadx=193)
    back_button = Button(sell_stock_frame, text="Back", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: backStock(2.2))
    back_button.grid(row=5, column=0, columnspan=2, pady=(5, 15), ipadx=190)
    limit_order_button = Button(sell_stock_frame, text="Set a Limit Order", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#F09F31', fg='black', borderwidth=3, command=lambda: limitOrder(selected_stock, "SELL"))
    limit_order_button.grid(row=7, column=0, columnspan=2, pady=(10, 5), ipadx=138)


def limitOrder(stock, task):
    if task == "BUY":
        buy_stock_frame.destroy()
    elif task == "SELL":
        sell_stock_frame.destroy()

    global limit_order_frame
    limit_order_frame = LabelFrame(root, padx=5, pady=5)
    limit_order_frame.pack(padx=10, pady=10)
    root.geometry("600x400")

    # Labels
    # Main heading
    entry = Entry(limit_order_frame, width=38, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=3, pady = 20)
    entry.insert(0, "SET A LIMIT ORDER")
    print_string = "NUMBER OF SHARES"
    label = Label(limit_order_frame, text=print_string, font=('Arial',9,'bold'))
    label.grid(row=1, column=0, pady=10)
    label = Label(limit_order_frame, text="LIMIT PRICE ($)", font=('Arial',9,'bold'))
    label.grid(row=2, column=0, pady=10)
    label = Label(limit_order_frame, text="EXPIRY DATE", font=('Arial',9,'bold'))
    label.grid(row=3, column=0, pady=(15, 0))
    label = Label(limit_order_frame, text="mm", font=('Arial',7,'normal', 'italic'), fg='green')
    label.grid(row=4, column=1, pady=(0, 10))
    label = Label(limit_order_frame, text="dd", font=('Arial',7,'normal', 'italic'), fg='green')
    label.grid(row=4, column=2, pady=(0, 10))

    # Entry's
    quantity_entry = Entry(limit_order_frame, width=20, borderwidth=3, font=('Arial',10,'bold'), justify=CENTER)
    quantity_entry.grid(row=1, column=1, columnspan=2, padx=10)
    price_entry = Entry(limit_order_frame, width=20, borderwidth=3, font=('Arial',10,'bold'), justify=CENTER)
    price_entry.grid(row=2, column=1, columnspan=2, padx=10)
    month_entry = Entry(limit_order_frame, width=6, borderwidth=3, font=('Arial',10,'bold'), justify=CENTER)
    month_entry.grid(row=3, column=1, pady=(15, 0))
    date_entry = Entry(limit_order_frame, width=6, borderwidth=3, font=('Arial',10,'bold'), justify=CENTER)
    date_entry.grid(row=3, column=2, pady=(15, 0))

    # Buttons
    if task == "SELL":
        set_button = Button(limit_order_frame, text="Set Order", font=('Comic Sans MS',10), activebackground='gray', 
                            activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,
                            command=lambda: setOrder("SELL", stock, int(quantity_entry.get()), float(price_entry.get()),
                            month_entry.get(), date_entry.get()))
        back_button = Button(limit_order_frame, text="Back", font=('Comic Sans MS',10), activebackground='gray', 
                             activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: sellStock(stock, 2))
    elif task == "BUY":
        set_button = Button(limit_order_frame, text="Set Order", font=('Comic Sans MS',10), activebackground='gray', 
                            activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,
                            command=lambda: setOrder("BUY", stock, int(quantity_entry.get()), float(price_entry.get()),
                            month_entry.get(), date_entry.get()))
        back_button = Button(limit_order_frame, text="Back", font=('Comic Sans MS',10), activebackground='gray', 
                             activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: buyStock(stock, 2))
    
    set_button.grid(row=7, column=0, pady=15, ipadx=65)
    back_button.grid(row=7, column=1, columnspan=2, pady=15, ipadx=90)


def setOrder(type, stock, qty, price, month, date):
    # Get Current time
    cur_time = str(datetime.datetime.now())[:10]

    # Set expiry time in the format yyyy-mm-dd
    exp_time = '2021-' + month + '-' + date

    # Store the order in limit_orders table
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    db.execute("""INSERT INTO limit_orders (user_id, stock_id, quantity, price, expiry_time, cur_time, type)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""", (logged_in_user[0], stock[0], qty, price, exp_time, cur_time, type))
    
    data = db.execute("SELECT * FROM limit_orders").fetchall()
    
    conn.commit()
    conn.close()

    # redirect user to stocks Summary
    viewStocksSummary(2)
    

def sellfunction(stock, qty):
    # Check if owned shares were less than entered quantity
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    # Get quantity of shares owned
    data = db.execute("SELECT * FROM user_shares WHERE user_id = ? AND stock_id = ?", (logged_in_user[0], stock[0])).fetchone()

    if data[3] < qty: # If qty entered exceeds user's shares in the company, pop an error message
        message = messagebox.showerror("Error", "Entered quantity exceeds owned shares, Please enter a valid quantity!")
        conn.commit()
        conn.close()
        sellStock(stock, 2)
    else:
        # Calculate total
        total = qty * stock[3]
        
        # Get transaction time
        time = str(datetime.datetime.now())

        # Update new balance
        logged_in_user[5] += total

        # update volume
        volume = stock[-2] + qty

        # Update databases
        # Update transactions table
        db.execute("""INSERT INTO transactions (user_id, time, amount, type)
                    VALUES (?, ?, ?, ?)""", (logged_in_user[0], time[:-7], total, "SHARE SOLD"))

        # Update user_shares table
        if data[3] - qty == 0: # Delete record from user_shares if user owns 0 shares after selling
            db.execute("""DELETE FROM user_shares 
                        WHERE user_id = ? AND stock_id = ?""", (logged_in_user[0], stock[0]))
        else:
            db.execute("""UPDATE user_shares
                        SET Quantity = ? WHERE id = ?""", (data[3] - qty, data[0]))

        # Update new account balance in registered users table
        db.execute("""UPDATE registered_users
                    SET account_balance = ? WHERE id = ?""", (logged_in_user[5], logged_in_user[0]))

        # Update volume in stocks table
        db.execute("""UPDATE stocks
                    SET initial_volume = ? WHERE id = ?""", (volume, stock[0]))
        
        conn.commit()
        conn.close()
        # Transaction successful pop up
        message = messagebox.showinfo("Success", "Transaction Successfull")

        backStock(2.2)

def buyStock(selected_stock, frame_number):
    if frame_number == 1:
        view_stock_frame.destroy()
    elif frame_number == 2:
        limit_order_frame.destroy()
    
    root.geometry("600x450")
    global buy_stock_frame
    buy_stock_frame = LabelFrame(root, padx=5, pady=5)
    buy_stock_frame.pack(padx=10, pady=10)

    label_text = ["AVAILABLE SHARES OF " + selected_stock[2], "QTY OF SHARES ", "MKT PRICE ($)"]
    for i in range(len(label_text)):
        label = Label(buy_stock_frame, text=label_text[i], font=('Arial',9,'bold'), pady=10, padx=10)
        label.grid(row=i+1, column=0)

    # Entries
    # Main heading
    entry = Entry(buy_stock_frame, width=38, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, pady = 20)
    entry.insert(0, "BUY SHARES OF " + selected_stock[1].upper())
    available_quantity_entry = Entry(buy_stock_frame, width=20, font=('Arial',10,'bold'), justify=CENTER)
    available_quantity_entry.grid(row=1, column=1)
    available_quantity_entry.insert(0, selected_stock[-2])
    quantity_entry = Entry(buy_stock_frame, width=20, font=('Arial',10,'bold'), justify=CENTER)
    quantity_entry.grid(row=2, column=1)
    price_entry = Entry(buy_stock_frame, width=20, font=('Arial',10,'bold'), justify=CENTER)
    price_entry.grid(row=3, column=1)
    price_entry.insert(0,selected_stock[3])


    # Labels
    text="_________________________or_________________________"
    label = Label(buy_stock_frame, text=text, font=('Arial',9,'bold'), padx=10)
    label.grid(row=6, column=0, columnspan=2)

    # Buttons
    buy_button = Button(buy_stock_frame, text="Buy", font=('Comic Sans MS',10), activebackground='gray', 
                        activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, 
                        command=lambda: buyfunction(selected_stock, int(quantity_entry.get())))
    buy_button.grid(row=4, column=0, columnspan=2, pady=(15, 5), ipadx=193)
    back_button = Button(buy_stock_frame, text="Back", font=('Comic Sans MS',10), activebackground='gray', 
                         activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: backStock(2.1))
    back_button.grid(row=5, column=0, columnspan=2, pady=(10, 5), ipadx=187)
    limit_order_button = Button(buy_stock_frame, text="Set a Limit Order", font=('Comic Sans MS',10), activebackground='gray', 
                                activeforeground='white', bg='#F09F31', fg='white', borderwidth=3, 
                                command=lambda: limitOrder(selected_stock, "BUY"))
    limit_order_button.grid(row=7, column=0, columnspan=2, pady=(10, 15), ipadx=135)


def buyfunction(stock, qty):
    total = qty * stock[3]
    # If account balance is less than total, give error
    if logged_in_user[5] < total:
        message = messagebox.showerror("Error", "Account Balance is not sufficient!")
        backStock(2.1)
    else:
        # Get transaction time
        time = str(datetime.datetime.now())

        # Update new balance
        logged_in_user[5] -= total

        # update volume
        volume = stock[-2] - qty

        # Update databases
        conn = sqlite3.connect(config.DATABASE_PATH)
        db = conn.cursor()

        # Update transactions table
        db.execute("""INSERT INTO transactions (user_id, time, amount, type)
                    VALUES (?, ?, ?, ?)""", (logged_in_user[0], time[:-7], -total, "SHARE BOUGHT"))

        # Update user_shares table
        # Check if user already has stock
        data = db.execute("SELECT id, Quantity FROM user_shares WHERE user_id = ? AND stock_id = ?", (logged_in_user[0], stock[0])).fetchone()

        if not data: # Insert new record if user didn't had the stock
            db.execute("""INSERT INTO user_shares (user_id, stock_id, Quantity)
                        VALUES (?, ?, ?)""", (logged_in_user[0], stock[0], qty))
        else:
            db.execute("""UPDATE user_shares
                        SET Quantity = ? WHERE id = ?""", (data[1] + qty, data[0]))

        # Update registered users table
        db.execute("""UPDATE registered_users
                    SET account_balance = ? WHERE id = ?""", (logged_in_user[5], logged_in_user[0]))

        # Update stocks table
        db.execute("""UPDATE stocks
                    SET initial_volume = ? WHERE id = ?""", (volume, stock[0]))
        
        conn.commit()
        conn.close()
        # Transaction successful pop up
        message = messagebox.showinfo("Success", "Transaction Successfull")

        backStock(2.1)


def backStock(frame_number):
    if frame_number == 1:
        view_stock_frame.destroy()
    elif frame_number == 2.1:
        buy_stock_frame.destroy()
    elif frame_number == 2.2:
        sell_stock_frame.destroy()
    
    viewStocksSummary(3)


def isMarketOpen():
    date = str(datetime.date.today())
    date_format = date[-2:] + " " + date[5:7] + " " + date[:4]
    born = datetime.datetime.strptime(date_format, '%d %m %Y').weekday()
    day = calendar.day_name[born].lower()

    # Check if market is open today
    conn = sqlite3.connect(config.DATABASE_PATH)

    db = conn.cursor()
    
    data = list(db.execute("SELECT " + day + ", market_open, market_close FROM market").fetchone())
    
    conn.commit()
    conn.close()

    open_time = data[1]
    close_time = data[2]

    if data[0] == 0:
        return False
    else:
        time = str(datetime.datetime.now())
        hour = time[11:13]
        min = time[14:16]

        if int(hour) > int(open_time[:2]) and int(hour) < int(close_time[:2]):
            return True
        elif int(hour) == int(open_time[:2]) and int(hour) == int(close_time[:2]):
            if int(min) >= int(open_time[2:]) and int(min) <= int(close_time[2:]):
                return True
        elif int(hour) == int(open_time[:2]) and int(hour) < int(close_time[:2]):
            if int(min) >= int(open_time[2:]):
                return True
        elif int(hour) > int(open_time[:2]) and int(hour) == int(close_time[:2]):
            if int(min) <= int(close_time[2:]):
                return True
        else:
            return False

def viewStocksSummary(frame_number):
    if frame_number == 1:
        user_frame.destroy()
    elif frame_number == 2:
        limit_order_frame.destroy()

    root.geometry("1000x500")
    global view_summary_frame
    view_summary_frame = LabelFrame(root, padx=5, pady=5)
    view_summary_frame.pack(padx=10, pady=10)

    available_stocks = []
    # connect to the database
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    # get stock id and stock ticker for every stock in the stocks table
    stocks = db.execute("SELECT id, companyname, stockticker, initial_volume FROM stocks").fetchall()
    for stock in stocks:
        temp = []
        data = db.execute("""SELECT close, open, high, low FROM stock_info WHERE date =  (
                             SELECT date FROM stock_info ORDER BY date DESC LIMIT 1) AND stock_id = """ + str(stock[0])).fetchone()
        
        temp.append(list(stock)[0])  # id,
        temp.append(list(stock)[1])  # company
        temp.append(list(stock)[2])  # ticker
        temp += list(data)  # close, open, high, low
        temp.append(list(stock)[3])  # volume
        
        # Calculate market Capitalization
        temp.append(int(data[0] * stock[3]))  # Market Capitalization = cur price * volume

        available_stocks.append(temp)
        
    conn.commit()
    conn.close()

    # Entry
    entry = Entry(view_summary_frame, width=66, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=10, pady = 20)
    entry.insert(0, "STOCK MARKET SUMMARY")

    heading_entries = ["S#", "Ticker", "Cur. price", "Open", "High", "Low", "Volume", "Market Cap."]
    for i in range(len(heading_entries)):
        if i == 0:
            heading_entry = Entry(view_summary_frame, width=3, fg='white', bg='black', font=('Arial',9,'bold'), justify=CENTER)
        else:
            heading_entry = Entry(view_summary_frame, width=12, fg='white', bg='black', font=('Arial',9,'bold'), justify=CENTER)
        heading_entry.grid(row=1, column=i)
        heading_entry.insert(END, heading_entries[i])

    for i in range(10):
        for j in range(9):
            if j == 0:
                e = Entry(view_summary_frame, width=3, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                e.grid(row=i+2, column=j)
                e.insert(0, i + 1)
            elif j == 8:
                if i < len(available_stocks):
                    view_button = Button(view_summary_frame, text="Trade", font=('Comic Sans MS',6), padx=7, fg='green',
                                        command=lambda i=i: viewStock(available_stocks[i])) # send info of selected stock
                    if not isMarketOpen():
                        view_button['state'] = DISABLED
                    view_button.grid(row=i+2, column=j+1, padx=2)
            else:
                e = Entry(view_summary_frame, width=14, fg='blue', font=('Arial',8, 'bold'), justify=CENTER)
                e.grid(row=i+2, column=j)
                if i < len(available_stocks):
                    e.insert(END, available_stocks[i][j+1])

    # Buttons
    user_back_button = Button(view_summary_frame, text="Back", font=('Comic Sans MS',10), padx=10,
                              activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, 
                              command=lambda: userBack(1))
    user_back_button.grid(row=12, column=3, columnspan=3, pady=20, ipadx=80)

def DepositWithdraw(): 
    user_frame.destroy()

    # Set root geometry
    root.geometry("650x400")
    global deposit_withdraw_frame
    deposit_withdraw_frame = LabelFrame(root, padx=5, pady=5)
    deposit_withdraw_frame.pack(padx=10, pady=10)

    # connect to the database
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    stocks = db.execute("SELECT * FROM stocks").fetchall()

    conn.commit()
    conn.close()

    # Label
    amount_label = Label(deposit_withdraw_frame, width=25, text="ENTER AMOUNT ($)", font=('Arial',9,'bold'), bg='black', fg='white')
    amount_label.grid(row=1, column=0, pady=10)

    # Entry
    # Main heading
    entry = Entry(deposit_withdraw_frame, width=39, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, pady = 20)
    entry.insert(0, "DEPOSIT OR WITHDRAW CASH")
    # Amount entry
    amount_entry = Entry(deposit_withdraw_frame, width=28, borderwidth=3, justify=CENTER)
    amount_entry.grid(row=1, column=1, pady=10)

    # Buttons
    deposit_button = Button(deposit_withdraw_frame, text="Deposit", font=('Comic Sans MS',10), padx=10,
                            activebackground='gray', activeforeground='white', fg='#00D168', borderwidth=3,
                            command=lambda: despositCash(int(amount_entry.get())))
    deposit_button.grid(row=2, column=0, pady=(30, 0), ipadx=70)
    withdraw_button = Button(deposit_withdraw_frame, text="Withdraw", font=('Comic Sans MS',10), padx=10,
                            activebackground='gray', activeforeground='white', fg='#F2574A', borderwidth=3,
                            command=lambda: withdrawCash(int(amount_entry.get())))
    withdraw_button.grid(row=2, column=1, pady=(30, 0), ipadx=60)
    user_back_button = Button(deposit_withdraw_frame, text="Back", font=('Comic Sans MS',10), padx=10,
                              activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,
                              command=lambda: userBack(4))
    user_back_button.grid(row=3, column=0, columnspan=2, pady=20, ipadx=80)


def userBack(frame_number):
    if frame_number == 1:
        view_summary_frame.destroy()
    elif frame_number == 2:
        display_trans_frame.destroy()
    elif frame_number == 3:
        order_frame.destroy()
    elif frame_number == 4:
        deposit_withdraw_frame.destroy()
    elif frame_number == 5:
        display_portfolio_frame.destroy()
    
    userFrame()


def despositCash(amount):
    global logged_in_user
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    # Update user's account 
    logged_in_user[5] = int(logged_in_user[5]) + amount

    # Get current time
    time = str(datetime.datetime.now())
    
    # Update transactions table
    db.execute("""INSERT INTO transactions (user_id, time, amount, type)
                    VALUES (?, ?, ?, ?)""", (logged_in_user[0], time[:-7], amount, "CASH DEPOSIT"))

    # Update new account balance in registered_users table  
    db.execute("UPDATE registered_users SET account_balance=? WHERE id=?", (logged_in_user[5], logged_in_user[0]))

        
    conn.commit()
    conn.close()

    userBack(4)


def withdrawCash(amount):
    global logged_in_user

    if amount > int(logged_in_user[5]):  # Throw error if cash withdraw amount is greater then account balance
        message = messagebox.showerror("Error", "Entered amount was greater than the account balance, please enter a valid value")
        deposit_withdraw_frame.destroy()
        DepositWithdraw()
    else:
        conn = sqlite3.connect(config.DATABASE_PATH)
        db = conn.cursor()
        logged_in_user[5] = int(logged_in_user[5]) - amount
        
         # Get current time
        time = str(datetime.datetime.now())
    
        # Update transactions table
        db.execute("""INSERT INTO transactions (user_id, time, amount, type)
                    VALUES (?, ?, ?, ?)""", (logged_in_user[0], time[:-7], -amount, "CASH WITHDRAW"))

        # Update account balance in registered_users table
        db.execute("UPDATE registered_users SET account_balance=? WHERE id=?", (logged_in_user[5], logged_in_user[0]))
            
        conn.commit()
        conn.close()

        userBack(4)


def logout(isAdmin):
    if isAdmin == 0:  # Looping here from user's frame
        user_frame.destroy()
    else:
        admin_frame.destroy()
    master_frame()


def adminFrame():
    # destroy initial frame
    initial_frame.destroy()

    # signup frame
    global admin_frame
    admin_frame = LabelFrame(root, padx=5, pady=5)
    admin_frame.pack(padx=10, pady=10)
    
    # Entry
    entry = Entry(admin_frame, width=37, fg='white', bg='black', font=('Arial',12,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, padx=10, pady=25)
    entry.insert(0, 'Welcome ' + logged_in_user[1])

    # buttons
    create_stocks_button = Button(admin_frame, text="Create Stocks", padx=10, font=('Comic Sans MS',10), command=createStocks,
                                  activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    create_stocks_button.grid(row=1, column=0, columnspan=2, ipadx=128)
    market_hours_button = Button(admin_frame, text="Change Market hours", font=('Comic Sans MS',10), padx=10, command=marketHours,
                                 activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    market_hours_button.grid(row=2, column=0, columnspan=2, ipadx=102)
    market_schedule_button = Button(admin_frame, text="Change Market Schedule", font=('Comic Sans MS',10), padx=10, command=marketSchedule,
                                    activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3)
    market_schedule_button.grid(row=3, column=0, columnspan=2, ipadx=87)
    logout_button = Button(admin_frame, text="Logout", padx=10, font=('Comic Sans MS',10), activebackground='gray', 
                           activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: logout(1))
    logout_button.grid(row=4, column=0, columnspan=2, ipadx=160)

def adminBack(frame_number):
    if frame_number == 1:
        create_stock_frame.destroy()
    elif frame_number == 2:
        market_schedule_frame.destroy()  # Need to add the functionality
    elif frame_number == 3:
        market_hour_frame.destroy()  # Need to add the functionality

    adminFrame()


def changeHours(opening_hours, closing_hours):
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    schedule = list(db.execute("SELECT * from market").fetchone())
    schedule[-2] = opening_hours
    schedule[-1] = closing_hours

    db.execute("""DELETE FROM market""")
    db.execute("""INSERT INTO market (monday, tuesday, wednesday, thursday, friday, saturday, sunday, market_open, market_close)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", schedule[1:])
    
    conn.commit()
    conn.close()
    
    adminBack(3)

def marketHours():
    admin_frame.destroy()
    global market_hour_frame
    market_hour_frame = LabelFrame(root, padx=5, pady=5)
    market_hour_frame.pack(padx=10, pady=10)

    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()
    data = db.execute("SELECT market_open, market_close FROM market").fetchone()
    
    conn.commit()
    conn.close()

    if not data:
        curr_market_hours_label = Label(market_hour_frame, text="No market hours set", font=('Comic Sans MS',10))

    else:
        market_open = data[0]
        market_close = data[1]
        text="CURRENT MARKET HOURS:  " + market_open[:2] + ':' + market_open[2:] + ' to ' + market_close[:2] + ':' + market_close[2:]
        curr_market_hours_label = Label(market_hour_frame, text=text, fg='#3853D2', font=('Arial',10,'bold'), padx=10)
    curr_market_hours_label.grid(row=1, column=0, columnspan=4, pady=10)

    # labels
    # Main Heading
    entry = Entry(market_hour_frame, width=32, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=4, pady = 25)
    entry.insert(0, "MARKET HOURS SETTINGS")

    opening_subheading_label = Label(market_hour_frame, text="NEW OPENING TIME", width=38, fg='white', 
                                     bg='#3853D2', font=('Arial',10,'bold'), justify=CENTER)
    opening_subheading_label.grid(row=2, column=0, columnspan=4, pady=(20, 10))
    open_hour_label = Label(market_hour_frame, text="hour (hh)", font=('Arial',8,'bold'))
    open_hour_label.grid(row=3, column=0)
    open_min_label = Label(market_hour_frame, text="minute (mm)", font=('Arial',8,'bold'))
    open_min_label.grid(row=3, column=2)
    opening_subheading_label = Label(market_hour_frame, text="NEW CLOSING TIME", width=38, fg='white', 
                                     bg='#3853D2', font=('Arial',10,'bold'), justify=CENTER)
    opening_subheading_label.grid(row=4, column=0, columnspan=4, pady = (20, 10))
    close_hour_label = Label(market_hour_frame, text="hour (hh)", font=('Arial',8,'bold'))
    close_hour_label.grid(row=5, column=0)
    close_min_label = Label(market_hour_frame, text="minute (mm)", font=('Arial',8,'bold'))
    close_min_label.grid(row=5, column=2)

    # Entry boxes
    open_hour_entry = Entry(market_hour_frame, width=5, borderwidth=3)
    open_hour_entry.grid(row=3, column=1)
    open_min_entry = Entry(market_hour_frame, width=5, borderwidth=3)
    open_min_entry.grid(row=3, column=3)
    close_hour_entry = Entry(market_hour_frame, width=5, borderwidth=3)
    close_hour_entry.grid(row=5, column=1)
    close_min_entry = Entry(market_hour_frame, width=5, borderwidth=3)
    close_min_entry.grid(row=5, column=3)

    # Buttons
    okay_button = Button(market_hour_frame, text="Okay", padx=10, font=('Comic Sans MS',10), activebackground='gray', 
                           activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, 
                        command=lambda: changeHours(open_hour_entry.get() + open_min_entry.get(),
                        close_hour_entry.get() + close_min_entry.get()))
    okay_button.grid(row=6, column=0, columnspan=2, pady=25, ipadx=59)
    admin_back_button = Button(market_hour_frame, text="Back", padx=10, font=('Comic Sans MS',10), activebackground='gray', 
                           activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: adminBack(3))
    admin_back_button.grid(row=6, column=2, columnspan=2, pady=25, ipadx=59)


def changeSchedule(new_schedule):
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    data = db.execute("SELECT * from market").fetchone()
    if data:
        schedule = [x for x in new_schedule]
        schedule.append(data[-2])
        schedule.append(data[-1])
    else:
        schedule = [x for x in new_schedule]
        schedule.append('0800')  # default market open value
        schedule.append('1500')  # default market close value

    db.execute("""DELETE FROM market""")
    db.execute("""INSERT INTO market (monday, tuesday, wednesday, thursday, friday, saturday, sunday, market_open, market_close)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", schedule)
    
    conn.commit()
    conn.close()
    
    adminBack(2)

def marketSchedule():
    admin_frame.destroy()
    global market_schedule_frame
    market_schedule_frame = LabelFrame(root, padx=5, pady=5)
    market_schedule_frame.pack(padx=10, pady=10)

    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()
    data = db.execute("SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM market").fetchone()
    
    conn.commit()
    conn.close()
    
    if not data or data == (None, None, None, None, None, None, None):
        curr_market_hours_label = Label(market_schedule_frame, text="Market schedule not set", font=('Comic Sans MS',10))

    else:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        print_schedule = "CURRENT SCHEDULE: "
        for i in range(len(data)):
            if data[i] == 1:
                print_schedule = print_schedule + days[i]
                print_schedule = print_schedule + ", "
        curr_market_hours_label = Label(market_schedule_frame, fg='#3853D2', text=print_schedule[:-2], font=('Arial',10,'bold'))
    curr_market_hours_label.grid(row=1, column=0, columnspan=7, pady=10)

    # labels
    # Main Heading
    entry = Entry(market_schedule_frame, width=38, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=7, pady = 25)
    entry.insert(0, "MARKET SCHEDULE SETTINGS")
    opening_subheading_label = Label(market_schedule_frame, text="CREATE NEW SCHEDULE", fg='white', bg='#3853D2', font=('Arial',10,'bold'), width=45)
    opening_subheading_label.grid(row=2, column=0, columnspan=7, pady=(25, 10))
    mon_label = Label(market_schedule_frame, text="Mon", font=('Arial',7,'bold'))
    mon_label.grid(row=3, column=0)
    tue_label = Label(market_schedule_frame, text="Tue", font=('Arial',7,'bold'))
    tue_label.grid(row=3, column=1)
    wed_label = Label(market_schedule_frame, text="Wed", font=('Arial',7,'bold'))
    wed_label.grid(row=3, column=2)
    thur_label = Label(market_schedule_frame, text="Thu", font=('Arial',7,'bold'))
    thur_label.grid(row=3, column=3)
    fri_label = Label(market_schedule_frame, text="Fri", font=('Arial',7,'bold'))
    fri_label.grid(row=3, column=4)
    sat_label = Label(market_schedule_frame, text="Sat", fg='red', font=('Arial',7,'bold'))
    sat_label.grid(row=3, column=5)
    sun_label = Label(market_schedule_frame, text="Sun", fg='red', font=('Arial',7,'bold'))
    sun_label.grid(row=3, column=6)

    # tkinter variables
    isMon = IntVar()
    isTue = IntVar()
    isWed = IntVar()
    isThu = IntVar()
    isFri = IntVar()
    isSat = IntVar()
    isSun = IntVar()

    # Check buttons
    mon_check = Checkbutton(market_schedule_frame, variable=isMon)
    mon_check.grid(row=4, column=0)
    tue_check = Checkbutton(market_schedule_frame, variable=isTue)
    tue_check.grid(row=4, column=1)
    wed_check = Checkbutton(market_schedule_frame, variable=isWed)
    wed_check.grid(row=4, column=2)
    thur_check = Checkbutton(market_schedule_frame, variable=isThu)
    thur_check.grid(row=4, column=3)
    fri_check = Checkbutton(market_schedule_frame, variable=isFri)
    fri_check.grid(row=4, column=4)
    sat_check = Checkbutton(market_schedule_frame, variable=isSat)
    sat_check.grid(row=4, column=5)
    sun_check = Checkbutton(market_schedule_frame, variable=isSun)
    sun_check.grid(row=4, column=6)

    # Buttons
    okay_button = Button(market_schedule_frame, text="Set", padx=10, font=('Comic Sans MS',10), activebackground='gray', 
                           activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, 
                        command=lambda: changeSchedule(str(isMon.get())+str(isTue.get())+str(isWed.get())+str(isThu.get())+str(isFri.get())+str(isSat.get())+str(isSun.get())))
    okay_button.grid(row=5, column=0, columnspan=7, pady=(20, 5), ipadx=194)
    admin_back_button = Button(market_schedule_frame, text="Back", padx=10, font=('Comic Sans MS',10), activebackground='gray', 
                           activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: adminBack(2))
    admin_back_button.grid(row=6, column=0, columnspan=7, pady=(5, 20), ipadx=190)


def createStocks():
    admin_frame.destroy()

    # signup frame
    global create_stock_frame
    create_stock_frame = LabelFrame(root, padx=5, pady=5)
    create_stock_frame.pack(padx=10, pady=10)

    # Labels
    company_name_label = Label(create_stock_frame, text="COMPANY NAME", font=('Arial',10, 'bold'), padx=10)
    company_name_label.grid(row=1, column=0)
    ticker_label = Label(create_stock_frame, text="TICKER", font=('Arial',10, 'bold'), padx=10)
    ticker_label.grid(row=2, column=0)
    volume_label = Label(create_stock_frame, text="INITIAL VOLUME",  font=('Arial',10, 'bold'), padx=10)
    volume_label.grid(row=3, column=0)
    init_price_label = Label(create_stock_frame, text="INITIAL PRICE", font=('Arial',10, 'bold'), padx=10)
    init_price_label.grid(row=4, column=0)

    # Entry Boxes
    # Main Heading
    entry = Entry(create_stock_frame, width=41, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=2, pady = 25)
    entry.insert(0, "CREATE A NEW STOCK")

    # Need to remove these entry boxes as global
    global company_name_entry, ticker_entry, volume_entry, init_price_entry
    company_name_entry = Entry(create_stock_frame, width=30, borderwidth=3)
    company_name_entry.grid(row=1, column=1)
    ticker_entry = Entry(create_stock_frame, width=30, borderwidth=3)
    ticker_entry.grid(row=2, column=1)
    volume_entry = Entry(create_stock_frame, width=30, borderwidth=3)
    volume_entry.grid(row=3, column=1)
    init_price_entry = Entry(create_stock_frame, width=30, borderwidth=3)
    init_price_entry.grid(row=4, column=1)

    # buttons
    add_button = Button(create_stock_frame, text="Add Stock", font=('Comic Sans MS',10), padx=10,
                        activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,
                        command=lambda: insertStock([company_name_entry.get(), ticker_entry.get(), volume_entry.get(), init_price_entry.get()]))
    add_button.grid(row=5, column=0, pady=25, ipadx=60)
    back_button = Button(create_stock_frame, text="Back", font=('Comic Sans MS',10), padx=10,
                              activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3,
                              command=lambda: adminBack(1))
    back_button.grid(row=5, column=1, pady=25, ipadx=95)

def userSignIn(username, password):
    global logged_in_user
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()
    try:
        data = db.execute("SELECT * FROM registered_users WHERE username = ? AND password = ?", [username, password]).fetchone()
        if len(data) == 0:  # invalid credentials
            # Pop out an error message on invalid credentials
            message = messagebox.showerror("Error", "Bad username and password combination")
        else:
            logged_in_user = list(data)
            userFrame()
    except:
        message = messagebox.showerror("Error", "Bad username and password combination")
        

    conn.commit()
    conn.close()


def adminSignIn(username, password):
    global logged_in_user
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()
    try:
        data = db.execute("SELECT * FROM registered_users WHERE username = ? AND password = ?", [username, password]).fetchone()
        conn.commit()
        conn.close()
        if not data or data[-1] == 0:  # invalid credentials or user is not an admin
            message = messagebox.showerror("Error", "Bad username and password combination")
        else:
            logged_in_user = list(data)
            adminFrame()  
    except:
        message = messagebox.showerror("Error", "Bad username and password combination")      


def signUp():
    # destroy initial frame
    initial_frame.destroy()

    # signup frame
    global signup_frame
    signup_frame = LabelFrame(root, padx=5, pady=5)
    signup_frame.pack(padx=10, pady=10)

    # set root geometry
    root.geometry("700x400")

    # Labels
    fullname_label = Label(signup_frame, text="Full Name", padx=10, font=('Arial',9,'bold'))
    fullname_label.grid(row=1, column=0)
    username_label = Label(signup_frame, text="Username", padx=10, font=('Arial',9,'bold'))
    username_label.grid(row=2, column=0)
    email_label = Label(signup_frame, text="Email", padx=10, font=('Arial',9,'bold'))
    email_label.grid(row=3, column=0)
    password_label = Label(signup_frame, text="Password", padx=10, font=('Arial',9,'bold'))
    password_label.grid(row=4, column=0)

    # Entry Boxes
    # Main heading
    entry = Entry(signup_frame, width=51, fg='white', bg='brown', font=('Arial',13,'bold'), justify=CENTER)
    entry.grid(row=0, column=0, columnspan=4, pady = 20)
    entry.insert(0, "SIGN UP")
    global fullname_signup_entry, username_signup_entry, email_signup_entry, password_signup_entry
    fullname_signup_entry = Entry(signup_frame, width=50, borderwidth=5)
    fullname_signup_entry.grid(row=1, column=1)
    username_signup_entry = Entry(signup_frame, width=50, borderwidth=5)
    username_signup_entry.grid(row=2, column=1)
    email_signup_entry = Entry(signup_frame, width=50, borderwidth=5)
    email_signup_entry.grid(row=3, column=1)
    password_signup_entry = Entry(signup_frame, width=50, borderwidth=5, show="*")
    password_signup_entry.grid(row=4, column=1)

    # Check box
    isAdmin = IntVar()
    isAdmin.set(0)  # Normal user selected by default 

    admin_checkbox = Checkbutton(signup_frame, text="Register as an administrator", font=('Arial',9,'bold'), variable=isAdmin)
    admin_checkbox.grid(row=5, column=0, columnspan=2, pady=10)

    # Buttons
    submit_button = Button(signup_frame, text="Sign Up", font=('Comic Sans MS',10), padx=10,
                        activebackground='gray', activeforeground='white', bg='#3853D2', fg='white', borderwidth=3, command=lambda: insertRecord(isAdmin.get()))
    submit_button.grid(row=6, column=0, columnspan=2, ipadx=95, pady=10, padx=(52, 0))


def insertRecord(isAdmin):
    # isAdmin = 0 for normal user and 1 for administrator
    record = [fullname_signup_entry.get(), username_signup_entry.get(), email_signup_entry.get(), 
            password_signup_entry.get(), 0, isAdmin]  # Account would contain $0 cash initially
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    db.execute("""INSERT INTO registered_users (fullname, username, email, password, account_balance, administrator)
                VALUES (?, ?, ?, ?, ?, ?)""", record)
    
    conn.commit()
    conn.close()

    # destroy the window
    signup_frame.destroy()
    master_frame()


def insertStock(new_stock):
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()
    
    db.execute("""INSERT INTO stocks (companyname, stockticker, initial_volume, initialprice)
                VALUES (?, ?, ?, ?)""", new_stock)

    # Get stock_id
    id = db.execute("SELECT id FROM stocks WHERE companyname=? AND stockticker=?", new_stock[:2]).fetchone()
    volume = new_stock[2]
    date = str(datetime.date.today())
    price = new_stock[-1]
    # initialize stock_info table as well
    db.execute("""INSERT INTO stock_info (stock_id, date, open, close, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (id[0], date, price, price, price, price, volume))
    
    conn.commit()
    conn.close()

    # destroy the window
    create_stock_frame.destroy()
    adminFrame()

# main function
if __name__ == '__main__':

    # root window
    root = Tk()
    root.title("Stock Trading Application")
    root.geometry("700x300")
    root.iconbitmap("./stocks.ico")

    # create databases
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()
    
    # Keeps track of all the registered users along with their current account balance
    db.execute("""CREATE TABLE IF NOT EXISTS registered_users (
                id INTEGER PRIMARY KEY,
                fullname TEXT,
                username TEXT,
                email TEXT,
                password TEXT,
                account_balance INTEGER,
                administrator INTEGER)""")

    # Keeps track of all the stocks registered with the application, along with their initial values
    db.execute("""CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY,
                companyname TEXT,
                stockticker TEXT,
                initial_volume INTEGER,
                initialprice FLOAT)""")  # Need to change 

    # Keeps track various parameter of each stock on each market day
    db.execute("""CREATE TABLE IF NOT EXISTS stock_info (
                id INTEGER PRIMARY KEY,
                stock_id INTEGER,
                date TEXT,
                open FLOAT,
                close FLOAT,
                high FLOAT,
                low FLOAT,
                volume INTEGER,
                FOREIGN KEY (stock_id) REFERENCES stock (id))""")

    # Records history of all the price fluctuation since registration of the stock. Can be used to create trend plots
    db.execute("""CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY,
                stock_id INTEGER,
                timestamp TEXT,
                price FLOAT,
                FOREIGN KEY (stock_id) REFERENCES stock (id))""")
    
    # Records all information related to market
    db.execute("""CREATE TABLE IF NOT EXISTS market (
                id INTEGER PRIMARY KEY,
                monday INTEGER,
                tuesday INTEGER,
                wednesday INTEGER,
                thursday INTEGER,
                friday INTEGER,
                saturday INTEGER,
                sunday INTEGER,
                market_open TEXT,
                market_close TEXT)""")

    # Records information on all transactions
    db.execute("""CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                time TEXT,
                amount FLOAT,
                type TEXT,
                FOREIGN KEY (user_id) REFERENCES registered_users (id))""")

    # Record information on user shares
    db.execute("""CREATE TABLE IF NOT EXISTS user_shares(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                stock_id INTEGER,
                Quantity INTEGER,
                FOREIGN KEY (user_id) REFERENCES registered_users (id),
                FOREIGN KEY (stock_id) REFERENCES stock (id))""")

    # Record information on all limit orders
    db.execute("""CREATE TABLE IF NOT EXISTS limit_orders(
                id INTEGER PRIMARY KEY,
		        user_id INTEGER,
                stock_id INTEGER,
		        quantity INTEGER,
		        price FLOAT,
                expiry_time TEXT,
                cur_time TEXT,
		        type TEXT,
                FOREIGN KEY (user_id) REFERENCES registered_users (id),
                FOREIGN KEY (stock_id) REFERENCES stock (id))""")

    conn.commit()
    conn.close()

    master_frame()

    root.mainloop()