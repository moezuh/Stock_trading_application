import sqlite3, config
import datetime, calendar, random

def calculatePrices():
    # Calculate the date of today
    today = str(datetime.date.today())
    
    conn = sqlite3.connect(config.DATABASE_PATH)

    db = conn.cursor()
    stock_ids =  db.execute("SELECT id FROM stocks").fetchall()
    for id in stock_ids:
        data = db.execute("SELECT * FROM stock_info WHERE stock_id = " + str(id[0]) + " ORDER BY date DESC").fetchone()
        if data: # If stock was not added today 
            if data[2] == today: # If stock already has a record of today, then just update it with new price value
                # Calculate new price 
                prev_price = int(data[4])
                delta = random.random()
                if random.randint(0, 11) % 2 == 0:
                    new_price = prev_price + delta
                else:
                    new_price = prev_price - delta
                
                # new_price = prev_price + random.randrange(-2 * prev_price, 2 * prev_price, 1)/(prev_price + 1) 
                new_price = round(new_price, 2)

                # Update Close price
                close_price = new_price

                # update high and low
                high = data[5]
                low = data[6]
                if new_price > high:
                    high = new_price
                elif new_price < low:
                    low = new_price

                # update the record into stocks_info table
                db.execute("""UPDATE stock_info SET close = ?, high = ?, low = ? 
                            WHERE date = ? AND stock_id = ?""",(close_price, high, low, str(today), id[0]))
        
            else: # if today's record did not existed
                
                # Opening price would be the closing price of last day market was open
                opening_price = data[4]

                # Calculate new price
                prev_price = int(opening_price)
                delta = random.random()
                if random.randint(0, 9) % 2 == 0:
                    new_price = prev_price + delta
                else:
                    new_price = prev_price - delta
                new_price = round(new_price, 2)
                closing_price = new_price

                # Since it is the first record of the day, high and low would be same as the new price
                high = new_price
                low = new_price

                # Update new record list
                record = list(data)
                record[2] = str(today)
                record[3] = opening_price
                record[4] = closing_price
                record[5] = high
                record[6] = low

                # Insert the new record into stock_info table
                db.execute("""INSERT INTO stock_info (stock_id, date, open, close, high, low, volume)
                            VALUES  (?, ?, ?, ?, ?, ?, ?)""",record[1:])

    
        # Insert record into prices table with new price and time
        db.execute("""INSERT INTO prices (stock_id, timestamp, price)
                    VALUES (?, ?, ?)""", (id[0], str(datetime.datetime.now()), new_price))


    print("\nStocks information:")
    data = db.execute("SELECT * FROM stock_info WHERE date = '" + str(today) + "'").fetchall()
    for item in data:
        print(item)
    # Save changes and close database connection
    conn.commit()
    conn.close()

def finishOrder(price, order):
    # update volume in stocks table
    # update transactions table
    # update user_shares table
    # delete the order from limit_orders
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()

    if order[7] == "BUY":
        # Update new volume
        volume = db.execute("SELECT initial_volume FROM stocks WHERE id = " + str(order[2])).fetchone()[0]
        db.execute("UPDATE stocks SET initial_volume = ? WHERE id = ?", (volume - order[3], order[2]))

        transaction_amount = order[3] * price  # qty*price

        time = str(datetime.datetime.now())[:-7] # date
        # Update transactions table
        db.execute("""INSERT INTO transactions (user_id, time, amount, type)
                        VALUES (?, ?, ?, ?)""", (order[1], time, -transaction_amount, "*SHARE BOUGHT"))

        # Update user shares table
        # Get current shares of the user
        shares = db.execute("SELECT id, Quantity FROM user_shares WHERE user_id = ? AND stock_id = ?", (order[1], order[2])).fetchone()
        if shares: # if user already owns shares in that company, update new shares
            db.execute("UPDATE user_shares SET Quantity = ? WHERE id = ?", (shares[1] + order[3], shares[0]))
        else: # if user does not own any shares in that company, insert new stock
            db.execute("""INSERT INTO user_shares (user_id, stock_id, Quantity)
                          VALUES (?, ?, ?)""", (order[1], order[2], order[3]))

        # Delete the order from limit_orders table
        db.execute("DELETE FROM limit_orders WHERE id = " + str(order[0]))

        # Update new account balance in registered_users table
        balance = db.execute("SELECT account_balance from registered_users WHERE id = " + str(order[1])).fetchone()[0]
        balance -= transaction_amount
        db.execute("UPDATE registered_users SET account_balance = ? WHERE id = ?", (balance, order[1]))

    else:  # Sell
        # Update new volume
        volume = db.execute("SELECT initial_volume FROM stocks WHERE id = " + str(order[2])).fetchone()[0] + order[3]
        db.execute("UPDATE stocks SET initial_volume = ? WHERE id = ?", (volume, order[2]))

        transaction_amount = order[3] * price  # qty*price
        time = str(datetime.datetime.now())[:-7]  # date
        # Update transactions table
        db.execute("""INSERT INTO transactions (user_id, time, amount, type)
                        VALUES (?, ?, ?, ?)""", (order[1], time, transaction_amount, "*SHARE SOLD"))

        # Update user shares table
        # Get current shares of the user
        shares = db.execute("SELECT id, Quantity FROM user_shares WHERE user_id = ? AND stock_id = ?", (order[1], order[2])).fetchone()
        # Update new shares quantity
        if shares[1] - order[3] <= 0:
            db.execute("""DELETE FROM user_shares WHERE user_id = ? AND stock_id = ?""", (order[1], order[2]))
        else:
            db.execute("UPDATE user_shares SET Quantity = ? WHERE id = ?", (shares[1] - order[3], shares[0]))

        # Delete the order from limit_orders table
        db.execute("DELETE FROM limit_orders WHERE id = " + str(order[0]))

        # Update new account balance in registered_users table
        balance = db.execute("SELECT account_balance from registered_users WHERE id = " + str(order[1])).fetchone()[0]
        balance += transaction_amount
        db.execute("UPDATE registered_users SET account_balance = ? WHERE id = ?", (balance, order[1]))

    print(f"{order} has been Executed")
    conn.commit()
    conn.close()

def checkLimitOrders(is_market_open):
    conn = sqlite3.connect(config.DATABASE_PATH)
    db = conn.cursor()
    
    if is_market_open:
        # Get all the limit orders
        orders = db.execute("SELECT * FROM limit_orders").fetchall()

        # Get the stock_id's along with the current prices of the most recent date
        data = db.execute("""SELECT stock_id, close FROM stock_info WHERE date = (
                                SELECT date FROM stock_info ORDER BY date DESC LIMIT 1)""").fetchall()

        # Create a dictionary of stock_id's and current price for faster search
        stock_prices = dict()   # {stock_id : current_price}
        for item in data:
            if item[0] not in stock_prices:
                stock_prices[item[0]] = item[1]

        # Get the user_id's along with the current account balance
        data = db.execute("""SELECT id, account_balance FROM registered_users WHERE administrator = 0""").fetchall()

        # Create a dictionary of user_id's and current account balance for faster search
        users = dict()   # {stock_id : current_price}
        for item in data:
            if item[0] not in users:
                users[item[0]] = item[1]    
        
        # Check prices of the orders
        for order in orders:
            if order[7] == "BUY" and stock_prices[order[2]] <= order[4] and users[order[1]] >= order[4]*order[3]:  # Need to add a check for market open and close
                finishOrder(stock_prices[order[2]], order)
            elif order[7] == "SELL" and stock_prices[order[2]] >= order[4]:
                finishOrder(stock_prices[order[2]], order)
    
    # Check for expiry date of the limit order
    today = datetime.date.today()
    exp_date = str(today - datetime.timedelta(days = 1)) # Expired orders will be removed on first execution of this script the next day 
    
    db.execute("DELETE FROM limit_orders WHERE expiry_time = '" + exp_date + "'") 

    # Close connection
    conn.commit()
    conn.close()

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
print(f"\n\nMarket opening time: {open_time[:2]}:{open_time[2:]}, Market closing time: {close_time[:2]}:{close_time[2:]}")

is_market_open = False

if data[0] == 1:  # Market is scheduled to be open today
    time = str(datetime.datetime.now())
    hour = time[11:13]
    min = time[14:16]
    print(f"time right now: {hour}:{min}")
    if int(hour) > int(open_time[:2]) and int(hour) < int(close_time[:2]):
        is_market_open = True
        print("Market open right now")
        calculatePrices()
    elif int(hour) == int(open_time[:2]) and int(hour) == int(close_time[:2]):
        if int(min) >= int(open_time[2:]) and int(min) <= int(close_time[2:]):
            is_market_open = True
            print("Market open right now")
            calculatePrices()
    elif int(hour) == int(open_time[:2]) and int(hour) < int(close_time[:2]):
        if int(min) >= int(open_time[2:]):
            is_market_open = True
            print("Market open right now")
            calculatePrices()
    elif int(hour) > int(open_time[:2]) and int(hour) == int(close_time[:2]):
        if int(min) <= int(close_time[2:]):
            is_market_open = True
            print("Market open right now")
            calculatePrices()         
    else:
        print("Market closed right now")
else:
    print("Market closed today")

# Check for limit orders
checkLimitOrders(is_market_open)