import pandas as pd
from typing import Any, Optional
from datetime import datetime
import numpy as np

class DataColumnFilter:
    """
    Example

    start = '2021-06-06'
    end = '2021-06-07'

    sorting = DataColumnFilter(collection=collection, after_start_date=start, before_end_date=end)
    df = sorting.createDataFrame()

    """

    def __init__(
            self, database: Any,
            collection: str,
            after_start_date: Optional[str] = None,
            before_end_date: Optional[str] = None,
            channel: Optional[str] = None,
            product: Optional[str] = None,
            id: Optional[list] = None
    ):
        self.database = database
        self.colletion = collection
        self.after_start_date = after_start_date
        self.before_end_date = before_end_date
        self.channel = channel
        self.product = product
        self.id = id

    @staticmethod
    def location_data(dataframe, key, value, result):
        dataframe[key].loc[dataframe[key] == value] = result

    def filter_data(self, dataframe):
        self.location_data(dataframe=dataframe, key='channel', value='contact', result='Contact')
        self.location_data(dataframe=dataframe, key='product', value='Mango ERP (Construction)', result='Construction')
        self.location_data(dataframe=dataframe, key='product', value='Mango ERP (Real Estate)', result='RealEstate')
        self.location_data(dataframe=dataframe, key='product', value='Pusit (Consulting)', result='Consulting')

    def sorting_data(self):
        data = self.database.find(self.colletion, {})
        df = pd.DataFrame(list(data))
        df = df.drop(['_id'], axis=1)
        df['date'] = pd.to_datetime(df['date'])
        self.filter_data(df)
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
        if self.channel:
            dfs = dfs.loc[dfs['channel'] == self.channel]
        if self.product:
            dfs = dfs.loc[dfs['product'] == self.product]

        d = datetime.strptime(self.after_start_date, '%Y-%m-%d')
        self.after_start_date = "{}-{}-{}".format(d.year, d.day, d.month)

        d = datetime.strptime(self.before_end_date, '%Y-%m-%d')
        self.before_end_date = "{}-{}-{}".format(d.year, d.day, d.month)

        after_start_date = dfs['date'] >= self.after_start_date
        before_end_date = dfs['date'] <= self.before_end_date
        between_two_dates = after_start_date & before_end_date
        filtered_dates = dfs.loc[between_two_dates]
        filtered_dates['date'] = filtered_dates['date'].dt.strftime('%d/%m/%Y')
        filtered_dates = filtered_dates.replace(np.nan, '', regex=True)
        return filtered_dates

    def export_excel(self):
        data = []
        for i in self.id:
            v = self.database.find_one(self.colletion, query={'id': i})
            v = dict(v)
            del v['_id']
            data.append(v)

        index = len(data)
        index = [i + 1 for i in range(index)]
        df = pd.DataFrame(data, index=index)
        self.filter_data(df)
        df = df.drop(['id'], axis=1)
        writer = pd.ExcelWriter('static/excels/customers.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        return writer
