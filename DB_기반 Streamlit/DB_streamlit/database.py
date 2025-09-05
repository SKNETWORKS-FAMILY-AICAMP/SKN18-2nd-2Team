import pymysql


class Database:
    def __init__(self, host, port, user, password, db, table) -> None:
        self.connection = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.table = table

    def connect(self):
        """데이터베이스와 연결"""
        try:
            self.connection = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, 
                                              database=self.db, charset="utf8")
        except Exception as e:
            print(e)
            print("Connection error")
        else:
            print("connected!")

    def insert(self, data: dict):
        """연결된 데이터베이스에 한 행 삽입"""
        columns = list(data.keys())
        values  = [data[c] for c in columns]  # 순서 고정

        columns_str   = ", ".join(f"`{c}`" for c in columns)
        placeholders  = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {self.table} ({columns_str}) VALUES ({placeholders});"

        cur = self.connection.cursor()
        try:
            cur.execute(query, tuple(values))   # ← execute + tuple(values)
            self.connection.commit()
            return cur.lastrowid
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            cur.close()

    def delete(self):
        """연결된 데이터베이스에 데이터 삭제"""
        cur = self.connection.cursor()
        query = f"DELETE FROM {self.table}"
        try:
            cur.execute(query)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            self.logger.warning(f"Deletion failed: {e}")
            raise e
        else:
            self.logger.info(f"Successfully delete {self.table} table")

    def read_data(self, customer_id):
        """연결된 데이터베이스에 데이터 읽기"""
        cur = self.connection.cursor()
        query = f"SELECT * FROM {self.table} WHERE customer_id = {customer_id} LIMIT 1;"
        try:
            cur.execute(query)
        except Exception as e:
            raise e
        return cur.fetchall()
    
    def read_all_data(self):
        cur = self.connection.cursor()
        query = f"SELECT * FROM {self.table};"
        try:
            cur.execute(query)
            rows =cur.fetchall()
            cols = [desc[0] for desc in cur.description]
        except Exception as e:
            raise e
        return rows, cols
    
    def read_all_data_df(self, lowercase_cols: bool = True):
        query = f"SELECT * FROM {self.table};"
        cur = self.connection.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()                               # [(...), (...), ...]
            cols = [desc[0] for desc in cur.description]        # 컬럼명 추출
        finally:
            cur.close()
        df = pd.DataFrame(rows, columns=cols)
        if lowercase_cols:
            df.columns = [c.lower() for c in df.columns]
        return df
    
    def close_connection(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
