class DBManager:
    def __init__(self, db_path):
        import sqlite3
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        self.connection.commit()

    def insert_product(self, product_id, product_name, price):
        self.cursor.execute("INSERT INTO products (product_id, product_name, price) VALUES (?, ?, ?)",
                            (product_id, product_name, price))
        self.connection.commit()

    def update_product(self, product_id, product_name, price):
        self.cursor.execute("UPDATE products SET product_name = ?, price = ? WHERE product_id = ?",
                            (product_name, price, product_id))
        self.connection.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        self.connection.commit()

    def select_product(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        return self.cursor.fetchone()

    def select_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()