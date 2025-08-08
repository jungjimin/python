import sqlite3
import os

class ProductModel:
    def __init__(self, db_name="ProductList.db"):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self._create_table()

    def _create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Price INTEGER
            );
        """)
        self.con.commit()

    def add_product(self, name, price):
        self.cur.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", (name, price))
        self.con.commit()

    def update_product(self, prod_id, name, price):
        self.cur.execute("UPDATE Products SET Name = ?, Price = ? WHERE id = ?;", (name, price, prod_id))
        self.con.commit()

    def delete_product(self, prod_id):
        self.cur.execute("DELETE FROM Products WHERE id = ?;", (prod_id,))
        self.con.commit()

    def get_all_products(self):
        self.cur.execute("SELECT * FROM Products;")
        return self.cur.fetchall()

    def close(self):
        self.con.close()
