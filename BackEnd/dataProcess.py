import os
import uuid
from dataSource import DataSource
from table import HierarchicalTable

filename = 'Console Sales.xlsx'
filepath = os.path.join('uploads', filename)

if __name__ == '__main__':
    #  get dataSource
    name = filename
    req_id = str(uuid.uuid4())
    data_source = DataSource(name, filepath, req_id)
    data_table = HierarchicalTable(data_source)
    result = data_table.generate_all_results()