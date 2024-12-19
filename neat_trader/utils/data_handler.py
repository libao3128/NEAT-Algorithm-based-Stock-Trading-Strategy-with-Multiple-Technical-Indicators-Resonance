import sqlite3
import pandas as pd
import numpy as np
import random
import datetime

class DataHandler:
    def __init__(self, db_path='data/mydatabase.db'):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_random_data(self, is_test=False, num_date=365):
        con = self._connect()
        tickers = pd.read_sql('SELECT DISTINCT Ticker FROM Price', con)

        ticker = np.random.choice(tickers['Ticker'].tolist())
        dates = pd.read_sql(f'SELECT Datetime FROM Price WHERE Ticker="{ticker}"', con)
        dates = pd.to_datetime(dates['Datetime'])
        start_date = dates.max()
        end_date = dates.min()

        time_between_dates = start_date - end_date
        try:
            days_between_dates = int(time_between_dates.days - 365 - num_date - 30)
            random_number_of_days = random.randrange(days_between_dates)
        except:
            return self.get_random_data()

        random_date = end_date + datetime.timedelta(days=random_number_of_days)
        if not is_test:
            start_date = random_date
            end_date = start_date + datetime.timedelta(days=int(num_date + 30))
        else:
            end_date = dates.max()
            start_date = dates.min()

        query = f'SELECT * FROM Price WHERE Ticker="{ticker}"' \
                f' AND Datetime>=DATETIME({start_date.timestamp()}, "unixepoch")' \
                f' AND Datetime<=DATETIME({end_date.timestamp()}, "unixepoch")'

        data = pd.read_sql(query, con)
        data.index = pd.DatetimeIndex(data['Datetime'])
        con.close()
        return data
    
def get_price(period, interval):
    file_name = 'data/price_sp500_'+interval+'_'+period+'.xlsx'
    if os.path.exists(file_name):
        price = pd.read_excel(file_name)
    else:
        sp500 = pd.read_excel('data/sp500.xlsx', header=2, index_col=0)
        price = yf.download(list(sp500['Symbol']), period=period, interval=interval)
        price.to_excel(file_name)
    return price

if __name__ == '__main__':
    price = get_price(period='20y', interval='1d')
    
