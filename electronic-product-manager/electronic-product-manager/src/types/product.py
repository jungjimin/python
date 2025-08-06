class Product:
    def __init__(self, product_id, product_name, price):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price

    def __repr__(self):
        return f"Product(id={self.product_id}, name='{self.product_name}', price={self.price})"