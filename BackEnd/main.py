import shutup
shutup.please()


from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dataset.tabular_data_collection import load_tabular_dataset, get_tabular_dataset, parse_upload_data
from processing.tabular_data_parse import parse_sheet
from werkzeug.utils import secure_filename
from table import HierarchicalTable
from dataSource import DataSource
import uuid
import os, random
import json
from werkzeug.utils import secure_filename


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'
global insight_length_list
global insight_length1,insight_length2
# namelist = ["Console Sales.xlsx", "Console Sales(cumulative).xlsx", "US Investment Abroad.xlsx", "School Curriculums.xlsx"]
namelist = ["Console Sales.xlsx", "Console Sales(cumulative).xlsx"]
pathlist =["public/Console Sales.xlsx", "public/Console Sales(cumulative).xlsx"]
''' rowlist = [42,42,41,17]
collist = [35,39,15,11] '''

def create_table_insight(name,path):
    requ_id = str(uuid.uuid4())
    name = name.split('.')[0] # remove the postfix(.xlsx) of a file name
    # if there is func_dependency, add it here
    # func_dependency = [(1, 0, 'row')]
    # data_source = DataSource(name, path, requ_id, func_dependency)
    data_source = DataSource(name, path, requ_id)
    global data_table
    data_table = HierarchicalTable(data_source)
    insight_vis_list = data_table.generate_all_results()
    # all_insight=data_table.insight_list_
    # print(all_insight)
    # result = data_table.generate_all_results()
    return str(len(insight_vis_list))


@app.route('/tabulardata', methods=['GET'])
@cross_origin()
def getTabularData():
    tabular_dataset = get_tabular_dataset()
    # print("tabular_dataset#######################")
    # print(tabular_dataset[0:50])
    # tabular_name_list = request.args.get('tabularData[]')
    return tabular_dataset

@app.route('/getblockinsight', methods=['POST'])
@cross_origin()
def getblockinsight():
    data = request.get_json()  # 获取JSON数据
    file_id = data.get('file_id')  # 从JSON数据中获取file_id参数
    # 先做一组test数据
    test_block_insight_data1=[
    {'Block_index': 1, 'insight_location(header)': ((), ('2013',)), 'insight_location4': [2, 41, 3, 6], 
     'insight_list':
        [
        {'Insight_index': 1,
         'vega_json':{
                "data": {
                "values": [
                    {"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43},
                    {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53},
                    {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}
                ]},"mark": "bar","encoding": {"x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},"y": {"field": "b", "type": "quantitative"}}
            },
        },
        {'Insight_index': 2,
         'vega_json':{
                "data": {
                "values": [
                    {"a": "A", "b": 288}, {"a": "B", "b": 558}, {"a": "C", "b": 438},
                    {"a": "D", "b": 918}, {"a": "E", "b": 818}, {"a": "F", "b": 538},
                    {"a": "G", "b": 198}, {"a": "H", "b": 878}, {"a": "I", "b": 528}
                ]},"mark": "bar","encoding": {"x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},"y": {"field": "b", "type": "quantitative"}}
            },
        },
        ]
    },
    {'Block_index': 2, 'insight_location(header)': (('Sony',), ('2017',)), 'insight_location4': [22, 33, 19, 22], 
     'insight_list':
        [
         {'Insight_index': 1,
         'vega_json':{
            "data": {
            "values": [
             {"category": "2013 - MAR", "value": 60.0}, 
             {"category": "2013 - JUN", "value": 140.0}, 
             {"category": "2013 - SEP", "value": 70.0}, 
             {"category": "2013 - DEC", "value": 40.000000000000036}, 
             {"category": "2014 - MAR", "value": 159.99999999999991}, 
             {"category": "2014 - JUN", "value": 200.00000000000006}, 
             {"category": "2014 - SEP", "value": 59.99999999999994}, 
             {"category": "2014 - DEC", "value": 70.00000000000006}, 
             {"category": "2015 - MAR", "value": 149.99999999999991}, 
             {"category": "2015 - JUN", "value": 120.00000000000011}, 
             {"category": "2015 - SEP", "value": 439.99999999999994}, 
             {"category": "2015 - DEC", "value": 120.00000000000011}, 
             {"category": "2016 - MAR", "value": 29.999999999999805}, 
             {"category": "2016 - JUN", "value": 109.99999999999987}, 
             {"category": "2016 - SEP", "value": 80.00000000000007}, 
             {"category": "2016 - DEC", "value": 50.00000000000027}, 
             {"category": "2017 - MAR", "value": 139.9999999999997}, 
             {"category": "2017 - JUN", "value": 50.00000000000027}, 
             {"category": "2017 - SEP", "value": 29.999999999999805}, 
             {"category": "2017 - DEC", "value": 20.000000000000018}]
             }, 
            "mark": {"type": "trail"}, 
            "encoding": {
             "x": {"field": "category", "type": "nominal", "sort": ["2013 - MAR", "2013 - JUN", "2013 - SEP", "2013 - DEC", "2014 - MAR", "2014 - JUN", "2014 - SEP", "2014 - DEC", "2015 - MAR", "2015 - JUN", "2015 - SEP", "2015 - DEC", "2016 - MAR", "2016 - JUN", "2016 - SEP", "2016 - DEC", "2017 - MAR", "2017 - JUN", "2017 - SEP", "2017 - DEC"]}, 
             "y": {"field": "value", "type": "quantitative"}, "size": {"field": "value", "type": "quantitative"}, 
             "tooltip": [{"field": "category", "type": "nominal"}, {"field": "value", "type": "quantitative"}]
             }
            }
        },
        {'Insight_index': 2,
         'vega_json':{
                "data": {
                "values": [
                    {"a": "A", "b": 288}, {"a": "B", "b": 558}, {"a": "C", "b": 438},
                    {"a": "D", "b": 918}, {"a": "E", "b": 818}, {"a": "F", "b": 538},
                    {"a": "G", "b": 198}, {"a": "H", "b": 878}, {"a": "I", "b": 528}
                ]},"mark": "bar","encoding": {"x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},"y": {"field": "b", "type": "quantitative"}}
            },
         },
         {'Insight_index': 3,
         'vega_json':{
                "data": {
                "values": [
                    {"a": "A", "b": 188}, {"a": "B", "b": 258}, {"a": "C", "b": 338},
                    {"a": "D", "b": 418}, {"a": "E", "b": 518}, {"a": "F", "b": 338},
                    {"a": "G", "b": 298}, {"a": "H", "b": 178}, {"a": "I", "b": 228}
                ]},"mark": "bar","encoding": {"x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},"y": {"field": "b", "type": "quantitative"}}
            },
        },
        ]
     }
    ]
    
    test_block_insight_data2=[
    {'Block_index': 1, 'insight_location(header)': (('Sony', 'PlayStation 3 (PS3)'), ()), 'insight_location4': [22, 25, 3, 22], 'insight_list':[{'Insight_index': 1},{'Insight_index': 2}]},
    {'Block_index': 2, 'insight_location(header)': (('Nintendo', 'Wii U (WiiU)', 'Europe'), ()), 'insight_location4': [18, 18, 3, 22], 'insight_list':[{'Insight_index': 1},{'Insight_index': 2}]},
    {'Block_index': 3, 'insight_location(header)': ((), ('2013',)), 'insight_location4': [2, 41, 3, 6], 'insight_list':[{'Insight_index': 1},{'Insight_index': 2}]},
    {'Block_index': 4, 'insight_location(header)': ((), ('2015',)), 'insight_location4': [2, 41, 11, 14], 'insight_list':[{'Insight_index': 1},{'Insight_index': 2}]},
    ]
    if(file_id == 1):
        return jsonify(test_block_insight_data1)
    if(file_id == 2):
        return jsonify(test_block_insight_data2)
    

    
    
@app.route('/getallinsight', methods=['POST'])
@cross_origin()
def get_table_insight():
    data = request.get_json()  # 获取JSON数据
    file_id = data.get('file_id')  # 从JSON数据中获取file_id参数
    return insight_length_list[file_id-1]

@app.route('/getupload', methods=['GET','POST'])
@cross_origin()
def file_upload():
    # requ_data = {
    #     'file': request.files.get('file'),
    #     # 'file_info': dict(request.form)
    # }
    # resp_data = resp_file_upload(requ_data)
    
    requ_data = request.files.get('file')
    # suffix = requ_data.filename.split(".")[-1]
    # file_path = 'public/upload_temp.' + suffix
    file_name = secure_filename(requ_data.filename)
    file_path = "public/upload_" + file_name
    requ_data.save(file_path)
    data = parse_upload_data(file_name)
    #print("parse_data", data)

    os.remove(file_path)  # 删除本地的文件
    return data

    # return "upload ok"

# def resp_file_upload(requ_data):
#     # 保存文件
#     file_content = requ_data['file']
#     file_name = requ_data['file'].filename
#     file_path = 'public/' + file_name
#     if os.path.exists(file_path):
#         return { 'msg': '该文件已存在'}
#     else:
#     	file_content.save(file_path)
#     	return { 'msg': '保存文件成功' }

# @app.route('/uploadtabulardata', methods=['GET'])
# @cross_origin()
# def getUploadTabularData():
#     file_name = request.args.get("name")
#     file_name = secure_filename(file_name)
#     data = parse_upload_data(file_name)
#     print("parse_data", data)
#     path = "public/upload_" + file_name
#     os.remove(path)  # 删除本地的文件
#     return data




if __name__ == "__main__":

    # print('run 0.0.0.0:14450')
    load_tabular_dataset()
    # tabular_dataset = get_tabular_dataset()
    
    # 这部分需要复原 
    insight_length_list=[]
    insight_length1=create_table_insight(namelist[0],pathlist[0])
    # insight_length2=create_table_insight(namelist[1],pathlist[1])

    insight_length_list.append(insight_length1)
    # insight_length_list.append(insight_length2)
    # # print("all_insights:")
    # # print(all_insights)
    # # print("___all_insights end___")
    # print("insight_length1:::")
    # print(insight_length1)
    # print("insight_length2:::")
    # print(insight_length2)
    
    app.run(host='0.0.0.0', port=14450, debug=True)


