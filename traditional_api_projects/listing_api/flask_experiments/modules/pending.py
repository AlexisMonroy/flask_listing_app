import csv
import sqlite3
import os

def pending_check():
    data_folder = 'C:/Users/alexi/dev/ebay_api/ebay_api/traditional_api_projects/listing_api/flask_experiments/data'

    conn = sqlite3.connect(os.path.join(data_folder, 'inventory.db'))

    # Create a PENDING, POSTED tables in the database

    conn.execute('CREATE TABLE IF NOT EXISTS pending (PENDING_ID INTEGER PRIMARY KEY, PRODUCT_ID INTEGER NULL, MARKET_ID TEXT NULL, DATE_TIME TEXT NULL, FOREIGN KEY (MARKET_ID) REFERENCES markets (MARKET_ID), FOREIGN KEY (PRODUCT_ID) REFERENCES books (PRODUCT_ID))')
    conn.execute('CREATE TABLE IF NOT EXISTS posted (PENDING_ID INTEGER PRIMARY KEY, PRODUCT_ID INTEGER NULL, MARKET_ID TEXT NULL, DATE_TIME TEXT NULL, FOREIGN KEY (MARKET_ID) REFERENCES markets (MARKET_ID), FOREIGN KEY (PRODUCT_ID) REFERENCES books (PRODUCT_ID))')

    conn.execute('CREATE TABLE IF NOT EXISTS verify_pending (PENDING_ID INTEGER PRIMARY KEY, PRODUCT_ID INTEGER NULL, MARKET_ID TEXT NULL, DATE_TIME TEXT NULL, FOREIGN KEY (MARKET_ID) REFERENCES markets (MARKET_ID), FOREIGN KEY (PRODUCT_ID) REFERENCES books (PRODUCT_ID))')
    conn.execute('CREATE TABLE IF NOT EXISTS verify_posted (PENDING_ID INTEGER PRIMARY KEY, PRODUCT_ID INTEGER NULL, MARKET_ID TEXT NULL, DATE_TIME TEXT NULL, FOREIGN KEY (MARKET_ID) REFERENCES markets (MARKET_ID), FOREIGN KEY (PRODUCT_ID) REFERENCES books (PRODUCT_ID))')

    #retrieve the product ids from the books table
    #cursor = conn.execute('SELECT ID from books where Title = ?', (book,))
    cursor = conn.cursor() 
    cursor_id = cursor.execute('SELECT ID from books')
    product_ids = cursor_id.fetchall()
    cursor_posted = cursor.execute('SELECT PRODUCT_ID from posted')
    posted_id = cursor_posted.fetchall()
    market_id = 1

    #insert the product ids into the pending table    
    for i in range(0, len(product_ids)):
        pending_id = product_ids[i][0]
        print(pending_id)
        if not any(pending_id in tup for tup in posted_id):
            print("PENDING ID NOT IN POSTED")
            #cursor_id_check = cursor.execute('SELECT PRODUCT_ID FROM pending WHERE PRODUCT_ID = ?', (product_ids[i][0],))
            #conn_result = cursor_id_check.fetchone()
            #if conn_result is None:
            cursor.execute('INSERT OR IGNORE into pending (PENDING_ID, PRODUCT_ID, DATE_TIME, MARKET_ID) VALUES (?, ?, datetime(\'now\', \'localtime\'), ?)', (product_ids[i][0], pending_id, market_id,))
    print("PENDING TABLE UPDATED")
    print(posted_id)
    for i in range(0, len(product_ids)):
        pending_id = product_ids[i][0]
        print(pending_id)
        if not any(pending_id in tup for tup in posted_id):
            print("PENDING ID NOT IN POSTED")
            #cursor_id_check = cursor.execute('SELECT PRODUCT_ID FROM verify_pending WHERE PRODUCT_ID = ?', (product_ids[i][0],))
            #conn_result = cursor_id_check.fetchone()
            #if conn_result is None:
            cursor.execute('INSERT OR IGNORE into verify_pending (PENDING_ID, PRODUCT_ID, DATE_TIME, MARKET_ID) VALUES (?, ?, datetime(\'now\', \'localtime\'), ?)', (product_ids[i][0], pending_id, market_id,))
    print("PENDING TABLE UPDATED")  

    pending_ids_cursor = cursor.execute('SELECT PRODUCT_ID FROM pending')
    pending_ids = pending_ids_cursor.fetchall()

    conn.commit()
    conn.close()

    return pending_ids



