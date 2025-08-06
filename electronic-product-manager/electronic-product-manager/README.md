# Electronic Product Manager

This project is a simple application for managing electronic product data using SQLite. It allows users to insert, update, delete, and select product records. The application is structured to provide a clear separation of concerns, with dedicated modules for database management, sample data generation, and product definitions.

## Project Structure

```
electronic-product-manager
├── src
│   ├── main.py               # Entry point of the application
│   ├── db_manager.py         # Database management functions
│   ├── sample_data.py        # Sample data generation
│   └── types
│       └── product.py        # Product data structure
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Features

- **Insert Products**: Add new products to the database.
- **Update Products**: Modify existing product details.
- **Delete Products**: Remove products from the database.
- **Select Products**: Retrieve product details by ID or get all products.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd electronic-product-manager
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage Examples

- To insert a new product, call the `insert_product` method with the product ID, name, and price.
- To update a product, use the `update_product` method with the product ID and new details.
- To delete a product, call `delete_product` with the product ID.
- To retrieve a product's details, use `select_product` with the product ID.
- To get a list of all products, call `select_all_products`.

## Sample Data

The project includes a function to generate and insert 100 sample product records into the database for testing purposes. This can be executed by calling the `generate_sample_data()` function from the `sample_data.py` module.

## License

This project is licensed under the MIT License.