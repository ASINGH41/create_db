import sqlite3

db = sqlite3.connect('db/ecomm.db')
def createDB():
    db.execute(
        '''
            CREATE TABLE IF NOT EXISTS PRODUCTS
            (
                ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
                NAME           TEXT   NOT NULL
            );
        '''
    )

    db.execute(
        '''
            CREATE TABLE IF NOT EXISTS ORDERS
            (
                ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
                USERNAME TEXT NOT NULL,
                PHONE TEXT NOT NULL,
                PRODUCT_ID INT NOT NULL,
                IS_DELIVERY BOOLEAN NOT NULL,
                ADDRESS TEXT NULL,
                WHEN_ TEXT NOT NULL,
                TOPPINGS TEXT NULL,
                FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS(ID)
            );
        '''
    )

    db.execute(
        '''
            CREATE TABLE IF NOT EXISTS PRODUCT_TOPPINGS
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME TEXT NOT NULL,
                PRODUCT_ID TEXT NOT NULL,
                FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCTS(ID)
            )
        '''
    )
    cursorObj = db.cursor()
    products = [
        {
            "name" : "Pizza",
            "toppings" : ["Pepperoni","Mushrooms","BlackOlives","Pineapple"]
        }, 
        {
            "name" : "Sub",
            "toppings" : ["Lettuce","Tomato","BlackOlives","Pineapple"]
        }, 
    ]
    for product in products:
        cursorObj.execute(
            '''
                INSERT INTO PRODUCTS(name) VALUES(?)
            ''', [product["name"]])
        product_id = cursorObj.lastrowid
        for topping in product["toppings"]:
            cursorObj.execute(
                '''
                    INSERT INTO PRODUCT_TOPPINGS(name, product_id) VALUES(? ,?)
                ''', [topping, product_id]
            )
    db.commit()



    db.close()


# driver function
if __name__ == '__main__':
    createDB()