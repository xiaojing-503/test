from utils.save_json_file import save_json_file
from utils.read_json_file import read_json_file
from skeleton.sql_skeleton import get_sql_skeleton,get_sql_schema
from skeleton.sql_value import extract_values
from skeleton.mapping import get_table_column_value
from utils.get_sql_schema_prompt import format_database_schema

bird_file_path='/root/Schema-Value/data/bird/dataset/filtered_empty_skeleton_schema3_copy.json'
BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
data=read_json_file(bird_file_path)

new_data = []  

for item in data:  
    full_schema = item['schema_sequence']  
    question = item['question'] + ' ' + item['evidence']  
    pred_sql = item['err_pred']  
    err_type = item['err_type']  
    db_id = item['db_id']  

    # print(pred_sql)

    # 假设get_sql_skeleton，get_sql_schema和extract_values是已定义的函数  
    skeleton = get_sql_skeleton(pred_sql)  
    sql_schemas = get_sql_schema(pred_sql)  
    values = extract_values(pred_sql)  

    # 假设get_table_column_value是已定义的函数，用来获取映射关系  
    schema_mapping = get_table_column_value(BIRD_DATABASE, db_id, sql_schemas, values)  

    # 假设format_database_schema是已定义的函数，用来格式化架构  
    new_schema = format_database_schema(schema_mapping)  

    # 构建新的条目  
    new_item = {  
        'db_id': db_id,  
        'question': question,  
        'pred_sql': pred_sql,  
        'err_type': err_type,  
        'full_schema': full_schema,  
        'new_schema': new_schema,  
        'skeleton': skeleton  
    }  

    # 将新条目添加到新数据列表中  
    new_data.append(new_item)  

save_json_file("/root/Schema-Value/data/bird/dataset/dev_1275.json",new_data)