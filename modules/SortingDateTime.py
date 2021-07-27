import pandas as pd
from db import MongoDB
import os

client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'customers'


class SortingDate:
    """
    Example

    start = '2021-06-06'
    end = '2021-06-07'

    sorting = SortingDate(collection=collection, after_start_date=start, before_end_date=end)
    df = sorting.createDataFrame()

    """

    def __init__(self, collection, after_start_date, before_end_date, channel=None):
        self.colletion = collection
        self.after_start_date = after_start_date
        self.before_end_date = before_end_date
        self.channel = channel

    @staticmethod
    def location_data(df, key, value, result):
        df[key].loc[df[key] == value] = result

    def createDataFrame(self):
        data = db.find(self.colletion, {})
        df = pd.DataFrame(list(data))
        df = df.drop(['_id'], axis=1)
        df['date'] = pd.to_datetime(df['date'])
        self.location_data(df=df, key='channel', value='contact', result='Contact')
        self.location_data(df=df, key='product', value='Mango ERP (Construction)', result='Construction')
        self.location_data(df=df, key='product', value='Mango ERP (Real Estate)', result='RealEstate')
        self.location_data(df=df, key='product', value='Pusit (Consulting)', result='Consulting')
        df1 = df.reset_index()[['date']]
        df1['year'] = [df1.iloc[i, 0].year for i in range(len(df1))]
        df1['month'] = [df1.iloc[i, 0].month for i in range(len(df1))]
        df1['day'] = [df1.iloc[i, 0].day for i in range(len(df1))]
        df1['english_day'] = df1.date.dt.strftime('%a')
        df1 = df1.drop(['date'], axis=1)
        df1 = df1.astype({
            'month': 'category',
            'day': 'category',
            'english_day': 'category'
        })
        dfs = df.merge(df1, left_index=True, right_index=True)
        dfs = dfs.sort_values(by='date')
        dfs = dfs.reset_index()
        dfs.drop(['index'], axis=1)
        after_start_date = dfs['date'] >= self.after_start_date
        before_end_date = dfs['date'] <= self.before_end_date
        # if channel:
        #     and_datetime_channel = after_start_date & before_end_date & channel
        #     filtered_ = dfs.loc[and_datetime_channel]
        #     filtered_['date'] = filtered_['date'].dt.strftime('%d/%m/%Y')
        #     return filtered_
        # else:
        between_two_dates = after_start_date & before_end_date
        filtered_dates = dfs.loc[between_two_dates]
        filtered_dates['date'] = filtered_dates['date'].dt.strftime('%d/%m/%Y')
        return filtered_dates


