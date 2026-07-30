import pymysql

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="0000",
    database="inventorydb",
    charset="utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)

    # 새 상품 추가
    def insert_product(self, product_name, price, stock):
        sql = "INSERT INTO product (product_name,price,stock) VALUES (%s,%s,%s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (product_name, price, stock))
                conn.commit()
                return True
            except Exception as error:
                conn.rollback()
                print("상품 등록 실패:", repr(error))
                return False
    # 재고 추가
    def insert_stock(self, product_name,  number):
        sql = "UPDATE product SET stock = (%s) + stock WHERE product_name = (%s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (number , (product_name)))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return

    def insert_or_update_product(self, product_name, price, number):
        select_sql ="SELECT product_id FROM product WHERE product_name = %s"
        insert_sql = "INSERT INTO product (product_name, price, stock) VALUES (%s, %s, %s)"
        update_sql = "UPDATE product SET price = %s, stock = stock + %s WHERE product_name = %s"

        with self.connect() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(select_sql, (product_name,))
                    product = cursor.fetchone()

                    if product:
                        cursor.execute(
                            update_sql,
                            (price, number, product_name),
                        )
                        result = "updated"
                    else:
                        cursor.execute(
                            insert_sql,
                            (product_name, price, number),
                        )
                        result = "inserted"

                conn.commit()
                return result
            except Exception:
                conn.rollback()
                
    # 모든 제품 조회
    def fetch_product(self):
            sql = "SELECT * FROM product"
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchall()  # [(customer_id, product_name, number, datetime)]

    # 재고 조회
    def fetch_stock(self, product_name):
        sql = "SELECT stock FROM product WHERE product_name = %s"
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql,(product_name))
                return cursor.fetchone()  # [(stock),]
    # 재고 사용
    def update_stock(self, product_name,  number):
        sql = "UPDATE product SET stock = stock -(%s)  WHERE product_name = (%s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (number , product_name))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return

            
    # 상세 주문 추가 - 주문 테이블 추가
    def insert_order(self, product_name, number):
        sql = "INSERT INTO orders ( product_name,number) VALUES (%s,%s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, ( product_name, number))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    # 주문 정보
    def insert_customer(self,  name, total, phone, datetime):
            sql = "INSERT INTO customer ( name,total,phone,datetime) VALUES (%s,%s,%s,%s)"
            with self.connect() as conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(sql, ( name, total, phone,datetime))
                    conn.commit()
                    return True
                except Exception:
                    conn.rollback()
                    return False

    # 주문 조회
    # def fetch_order(self, product_name, number):
    #     sql = "SELECT * FROM customers (product_name,number) VALUES (%s,%s)"
    #     with self.connect() as conn:
    #         with conn.cursor() as cursor:
    #             cursor.execute(sql,product_name, number)
    #             return cursor.fetchall()  # [(customer_id, product_name, number, datetime)]