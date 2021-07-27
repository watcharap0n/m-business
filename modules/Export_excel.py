import pandas as pd
from typing import Any


class ExportExcel:
    def __init__(self, db: Any, collection: str, id: list):
        self.db = db
        self.collection = collection
        self.id = id

    def excel(self):
        data = []
        for i in self.id:
            v = self.db.find_one(collection=self.collection, query={'id': i})
            v = dict(v)
            del v['_id']
            data.append(v)

        index = len(data)
        index = [i + 1 for i in range(index)]
        df = pd.DataFrame(data, index=index)
        df['channel'].loc[df['channel'] == 'contact'] = 'Contact'
        df['product'].loc[df['product'] == 'Mango ERP (Construction)'] = 'Construction'
        df['product'].loc[df['product'] == 'Mango ERP (Real Estate)'] = 'RealEstate'
        df['product'].loc[df['product'] == 'Real Estates'] = 'RealEstate'
        df['product'].loc[df['product'] == 'Pusit (Consulting)'] = 'Consulting'
        df = df.drop(['id'], axis=1)
        writer = pd.ExcelWriter('static/excels/customers.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        return writer
