from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey
from tabulate import tabulate

class Sqlite_client:
    db_engine = None

    def __init__(self, engine: str, table: str):
        engine_url = '%s:///%s.db' % (engine, table)
        self.db_engine = create_engine(engine_url)


    def create_database(self):
        metadata = MetaData()
        wallet = Table('wallet', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String, nullable=False),
                        Column('balance', Float, nullable=False)
                        )

        movement = Table('movement', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('wallet_id', Integer, ForeignKey('wallet.id')),
                        Column('type', String, nullable=False),
                        Column('value', Float, nullable=False)

                        )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return
        print (query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
                return (result.fetchall())
                for row in result:
                    pass
                    return row
                    #print(row) # print(row[0], row[1], row[2])
                result.close()
            except Exception as e:
                print(e)

    def create_wallet(self, name: str, value: float):
        query = 'INSERT INTO wallet (name, balance) VALUES ("%s", %d)' % (name, value)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def delete_wallet(self, id: int):
        query = ' DELETE FROM wallet WHERE id = %d;' % id
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)
    
    def check_balance(self, id: int):
        query = 'SELECT balance FROM wallet WHERE wallet.id = %d;' % id
        with self.db_engine.connect() as connection:
            try:
                conn = connection.execute(query)
                result = conn.fetchall() 
                conn.close() 
                if result == []:
                    print("Unable to find wallet ID")
                    return False
                else:
                    return result[0][0]
            except Exception as e:
                print(e)

    def transfer(self, wallet_source: int, wallet_destination: int, value: int):
        if value < 0:
            return 'Unable to transfer negative amounts'

        wallet_source_balance = self.check_balance(wallet_source)
        wallet_source_balance = wallet_source_balance - value

        wallet_destination_balance = self.check_balance(wallet_destination)
        wallet_destination_balance = wallet_destination_balance + value

        if wallet_source_balance < 0 or wallet_destination_balance < 0:
            return 'Unable to make the transfer, not enough balance in source wallet'
      
        with self.db_engine.connect() as connection:
            try:
                query = f'UPDATE wallet SET balance = {wallet_source_balance} WHERE id = {wallet_source};'
                connection.execute(query)
                query = f'UPDATE wallet SET balance = {wallet_destination_balance} WHERE id = {wallet_destination};'
                connection.execute(query)
            except Exception as e:
                print(e)
        return f"Wallet Source {wallet_source_balance}, Wallet Destination {wallet_destination_balance}"


db = Sqlite_client('sqlite', 'wallet')
db.create_database()
#db.create_wallet('Bank', 30)
#db.create_wallet('Wallet', 0)


print(tabulate(db.execute_query('SELECT * FROM wallet'), headers=["Wallet ID", "Name", "Balance"], tablefmt="grid"))
print(db.transfer(1, 2, 9.5))
print(tabulate(db.execute_query('SELECT * FROM wallet'), headers=["Wallet ID", "Name", "Balance"], tablefmt="grid"))




#balance = db.check_balance(1)
#db.delete_wallet(1)
#balance = db.check_balance(1)


