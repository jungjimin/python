# filepath: electronic-product-manager/electronic-product-manager/src/main.py
import sqlite3
from db_manager import DBManager
from sample_data import generate_sample_data

def main():
    db_manager = DBManager("electronic_products.db")
    
    # Uncomment the line below to generate sample data
    # generate_sample_data(db_manager)

    while True:
        print("\nElectronic Product Manager")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View Product")
        print("5. View All Products")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            product_id = input("Enter Product ID: ")
            product_name = input("Enter Product Name: ")
            price = float(input("Enter Product Price: "))
            db_manager.insert_product(product_id, product_name, price)
            print("Product added successfully.")
        
        elif choice == '2':
            product_id = input("Enter Product ID to update: ")
            product_name = input("Enter new Product Name: ")
            price = float(input("Enter new Product Price: "))
            db_manager.update_product(product_id, product_name, price)
            print("Product updated successfully.")
        
        elif choice == '3':
            product_id = input("Enter Product ID to delete: ")
            db_manager.delete_product(product_id)
            print("Product deleted successfully.")
        
        elif choice == '4':
            product_id = input("Enter Product ID to view: ")
            product = db_manager.select_product(product_id)
            if product:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
            else:
                print("Product not found.")
        
        elif choice == '5':
            products = db_manager.select_all_products()
            for product in products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
        
        elif choice == '6':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()