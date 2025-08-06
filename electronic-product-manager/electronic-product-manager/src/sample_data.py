def generate_sample_data(db_manager):
    sample_products = [
        (i, f"Product {i}", round(i * 10.99, 2)) for i in range(1, 101)
    ]
    
    for product_id, product_name, price in sample_products:
        db_manager.insert_product(product_id, product_name, price)