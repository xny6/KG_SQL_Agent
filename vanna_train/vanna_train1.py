from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={'model': 'mistral'})

vn.connect_to_mysql(host='10.4.160.88', dbname='my_database', user='xny_remote', password='ny20050417', port=3306)

def train_vn(vn):
    vn.train(ddl='''
    CREATE TABLE brands (
        brand_id INT NOT NULL AUTO_INCREMENT,
        brand_name VARCHAR(100),
        PRIMARY KEY (brand_id)
    );
    ''')

    vn.train(ddl='''
    CREATE TABLE customers (
        customer_id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(255),
        phone_number VARCHAR(50),
        address TEXT,
        registration_date DATE,
        PRIMARY KEY (customer_id),
        UNIQUE (email)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE orders (
        order_id INT NOT NULL AUTO_INCREMENT,
        customer_id INT,
        order_date DATE,
        total_amount DECIMAL(10,2),
        status VARCHAR(50),
        shipping_address TEXT,
        warranty_status VARCHAR(20),
        manufacturing_batch_id VARCHAR(50),
        PRIMARY KEY (order_id),
        CONSTRAINT orders_ibfk_1 FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE order_items (
        order_item_id INT NOT NULL AUTO_INCREMENT,
        order_id INT,
        product_id INT,
        quantity INT,
        unit_price DECIMAL(10,2),
        PRIMARY KEY (order_item_id),
        CONSTRAINT order_items_ibfk_1 FOREIGN KEY (order_id) REFERENCES orders(order_id),
        CONSTRAINT order_items_ibfk_2 FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE products (
        product_id INT NOT NULL AUTO_INCREMENT,
        product_name VARCHAR(255),
        price DECIMAL(10,2),
        stock_quantity INT,
        category VARCHAR(100),
        brand_id INT,
        release_date DATE,
        is_active TINYINT(1),
        PRIMARY KEY (product_id),
        CONSTRAINT products_ibfk_1 FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE product_feature (
        feature_id INT NOT NULL AUTO_INCREMENT,
        product_id INT,
        question TEXT,
        feature TEXT,
        PRIMARY KEY (feature_id),
        CONSTRAINT product_feature_ibfk_1 FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE product_reviews (
        id INT NOT NULL AUTO_INCREMENT,
        review_id INT,
        product_id INT,
        customer_id INT,
        rating INT,
        comment VARCHAR(255),
        review_date VARCHAR(255),
        is_approved VARCHAR(255),
        PRIMARY KEY (id)
        -- 未定义外键，如需要可添加：
        -- FOREIGN KEY (product_id) REFERENCES products(product_id),
        -- FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    ''')

    vn.train(ddl='''
    CREATE TABLE purchase_orders (
        purchase_order_id INT NOT NULL AUTO_INCREMENT,
        supplier_id INT,
        order_date DATE,
        expected_delivery_date DATE,
        total_cost DECIMAL(10,2),
        PRIMARY KEY (purchase_order_id),
        CONSTRAINT purchase_orders_ibfk_1 FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    );
    ''')

    vn.train(ddl='''
    CREATE TABLE returns (
        return_id INT NOT NULL AUTO_INCREMENT,
        order_id INT,
        product_id INT,
        return_reason VARCHAR(255),
        return_date DATE,
        refund_amount DECIMAL(10,2),
        status VARCHAR(50),
        PRIMARY KEY (return_id),
        CONSTRAINT returns_ibfk_1 FOREIGN KEY (order_id) REFERENCES orders(order_id),
        CONSTRAINT returns_ibfk_2 FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    ''')

    vn.train(ddl='''
    CREATE TABLE suppliers (
        supplier_id INT NOT NULL AUTO_INCREMENT,
        supplier_name VARCHAR(255),
        contact_person VARCHAR(255),
        phone VARCHAR(20),
        supplied_product_type VARCHAR(50),
        PRIMARY KEY (supplier_id)
    );
    ''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN in_ear_detection INT;''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN wireless_charging INT;''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN wireless_charging INT;''')

    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN fast_charging INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN eSIM INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN WiFi_6 INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN fingerprint_unlock INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN face_unlock INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Dual_4G INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Dual_SIM INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN has_3_5mm_headphone_jack INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN NFC INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN blueteeth_calls INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN IP_68 INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN auto_brightness INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN women_health INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN LE_audio INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Microsoft_swift_pair INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Google_fast_pair INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN custom_EQ_settings INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN ANC INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN Dual_connection INT;''')
    vn.train(ddl='''
    ALTER TABLE my_database.products
    ADD COLUMN in_ear_detection INT;''')


def train2(vn):
    vn.train(question='Get purchase date, products and warranty status for David Beltran\'s order',sql='''SELECT `orders`.`order_date`, `products`.`product_name`, `warranty_status`
    FROM orders
    JOIN customers ON orders.customer_id = customers.customer_id
    JOIN order_items ON orders.order_id = order_items.order_id
    JOIN products ON order_items.product_id = products.product_id
    WHERE customers.first_name = 'David' AND customers.last_name = 'Beltran'
    ''')

def train3(vn):
    vn.train(question='Get and price of Ear (a), CMF Buds Pro 2, Buds Pro earbuds, Ear (stick), Nothing Ear Stick earbuds, CMF Buds 2, Ear (1) earbuds, or other devices with similar names.',
        sql=r"""SELECT `products`.`product_name`, `products`.`price`
            FROM products
            WHERE `product_name` IN ('Ear (a)', 'CMF Buds Pro 2', 'Buds Pro earbuds', 'Ear (stick)', 'Nothing Ear Stick earbuds', 'CMF Buds 2', 'Ear (1) earbuds')
            OR `product_name` LIKE '%Ear%' OR `product_name` LIKE '%Buds%'
            ORDER BY `product_name` ASC

        """)
    
    vn.train(question='Get the price of Nothing Ear 2, CMF Buds Pro 2, Ear (stick), Buds Pro Earbuds, Nothing Ear (a), and Ear (a), or other earphones with similar names that support Active Noise Cancellation.',
        sql=r"""SELECT `products`.`product_name`, `products`.`price`
                FROM products
                WHERE `product_name` IN ('Ear (a)', 'CMF Buds Pro 2', 'Buds Pro earbuds', 'Ear (stick)', 'Nothing Ear Stick earbuds', 'CMF Buds 2', 'Ear (1) earbuds')
                OR `product_name` LIKE '%Ear%' OR `product_name` LIKE '%Buds%'
                ORDER BY `product_name` ASC

            """
    )

    vn.train(question='Get the name and price of the devices which support NFC',
        sql=r"""SELECT `products`.`product_name`, `products`.`price`
                FROM products
                WHERE `products`.`NFC` = 1
            """
    )

    vn.train(question='Get the name and price of the devices which support NFC',
        sql=r"""SELECT `products`.`product_name`, `products`.`price`
                FROM products
                WHERE `products`.`NFC` = 1
            """
    )
    vn.train(question = 'Get the name and price of Nothing Phone (1), Nothing Phone 2, iPhone, Samsung Galaxy series, Google Pixel phones, or other devices with similar name.',
        sql=r'''SELECT products.product_name, products.price
                FROM products
                WHERE products.product_name LIKE '%Nothing%' OR products.product_name LIKE '%iPhone%' OR products.product_name LIKE '%Samsung Galaxy%' OR products.product_name LIKE '%Google Pixel%'
            ''')








# train_vn(vn)
# train2(vn)
# train3(vn)

question = 'Get the name and price of Nothing Phone (1), Nothing Phone 2, iPhone, Samsung Galaxy series, Google Pixel phones, or other devices with similar name.'
sql= vn.generate_sql(question=question, allow_llm_to_see_data=True)
answer=vn.run_sql(sql=sql)
print('==============================================================')
print(f'SQL: {sql}')
print(f'Answer: {answer}')
# vn.ask(question=question, allow_llm_to_see_data=True,visualize=False)
# from vanna.flask import VannaFlaskApp
# app = VannaFlaskApp(vn)
# app.run()








