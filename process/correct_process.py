from utils.save_json_file import save_json_file
from utils.read_json_file import read_json_file
from skeleton.sql_skeleton import get_sql_skeleton,get_sql_schema
from skeleton.sql_value import extract_values
from skeleton.mapping import get_table_column_value
from utils.get_sql_schema_prompt import format_database_schema
from utils.get_full_schema_prompt import parse_schema_to_string
import json
import re
import numpy as np
from utils.get_response import get_deepseek_response
from utils.process_llm_output_sql import format_sql_to_single_line
import sqlite3
import re


def replace_special_characters_in_sql(file_path,save_path):

    content = read_json_file(file_path)
    for item in content:
        sql1=item['sql1']
        sql2=item['sql2']
        # 替换所有的 \“、` 等字符为 ”
        # \“ 替换为 ”
        # content = sql1.replace(r'\"', "''")
        # ` 替换为 ”
        sql1 = sql1.replace("`", "\"")
        sql2 = sql2.replace("`", "\"")

        item['sql1']=sql1
        item['sql2']=sql2
    
    save_json_file(save_path,content)

import os
def get_all_columns_for_db(database_path, db_id, tables):
    # Construct the full path to the database  
    database_name = os.path.join(database_path, db_id, f"{db_id}.sqlite")  
    
    # Set to hold unique column names across all specified tables  
    columns = set()  

    # Connect to the SQLite database  
    try:  
        connection = sqlite3.connect(database_name)  
        cursor = connection.cursor()  

        for table in tables:  
            # Execute PRAGMA query to get column info for each table  
            cursor.execute(f"PRAGMA table_info('{table}');")  
            column_info = cursor.fetchall()  

            # Extract column names and add them to the set  
            for column in column_info:  
                columns.add(column[1])  # assuming index 1 is for column names  

    except sqlite3.Error as e:  
        print(f"An error occurred: {e}")  

    finally:  
        # Ensure the connection is closed  
        if connection:  
            connection.close()  

    return columns  

# 2. schema使用sql0、sql1的并集
# /root/Schema-Value/data/bird/dataset_new_new_new/deepseek_new_new
def get_skeketon_schema(bird_file_path,file2,bird_database):
    
    data=read_json_file(bird_file_path)

    for item in data:  
        sql0 = item['err_pred']
        sql1 = item['sql1']
        sql2 = item['sql2']  
        new_err_type = item['new_err_type'] 
        db_id = item['db_id']  

        print(sql1)
        print(sql2)
        print("\n")
        if new_err_type=='result':

            # sql0=

            '''schema使用sql0、sql1的并集''' 
            # 提取values
            values0 = extract_values(sql0)
            values1 = extract_values(sql1)

            # 合并并去重values
            values = list(set(values0 + values1))  # 去重后的values

            # 获取sql_schemas
            sql_schemas0 = get_sql_schema(sql0)
            sql_schemas1 = get_sql_schema(sql1)

            # 合并表、列和值，分别处理每个部分
            tables = set(sql_schemas0[0]).union(sql_schemas1[0])  # 合并表
            columns = set(sql_schemas0[1]).union(sql_schemas1[1])  # 合并列
            # values = set(sql_schemas0[2]).union(sql_schemas1[2])  # 合并值

            # 最终结果以元组形式返回，保持原始格式
            sql_schemas = (tables, columns, values)



            schema_mapping = get_table_column_value(bird_database, db_id, sql_schemas, values)  
            new_schema = format_database_schema(schema_mapping) 

            skeleton2 = get_sql_skeleton(sql2)


        else:
            new_schema=''
            skeleton2=''

        item['sql1_schema']=new_schema
        item['sql2_skeleton']=skeleton2
        
    save_json_file(file2,data)


# 3. schema使用sql0、sql1、sql2的并集
# /root/Schema-Value/data/bird/dataset_new_new_new/deepseek_new_new_new
# def get_skeketon_schema(bird_file_path,file2,bird_database):
    
#     data=read_json_file(bird_file_path)

#     for item in data:  
#         sql0 = item['err_pred']
#         sql1 = item['sql1']
#         sql2 = item['sql2']  
#         new_err_type = item['new_err_type'] 
#         db_id = item['db_id']  

#         print(sql1)
#         print(sql2)
#         print("\n")
#         if new_err_type=='result':

#             '''schema使用sql0、sql1的并集''' 
#             # 提取values
#             values0 = extract_values(sql0)
#             values1 = extract_values(sql1)
#             values2 = extract_values(sql2)

#             # 合并并去重values
#             values = list(set(values0 + values1 + values2))  # 去重后的values

#             # 获取sql_schemas
#             sql_schemas0 = get_sql_schema(sql0)
#             sql_schemas1 = get_sql_schema(sql1)
#             sql_schemas2 = get_sql_schema(sql2)

#             # 合并表、列和值，分别处理每个部分
#             tables = set(sql_schemas0[0]).union(sql_schemas1[0]).union(sql_schemas2[0])  # 合并表
#             columns = set(sql_schemas0[1]).union(sql_schemas1[1]).union(sql_schemas2[1])  # 合并列

#             # 最终结果以元组形式返回，保持原始格式
#             sql_schemas = (tables, columns, values)



#             schema_mapping = get_table_column_value(bird_database, db_id, sql_schemas, values)  
#             new_schema = format_database_schema(schema_mapping) 

#             skeleton2 = get_sql_skeleton(sql2)


#         else:
#             new_schema=''
#             skeleton2=''

#         item['sql1_schema']=new_schema
#         item['sql2_skeleton']=skeleton2
        
#     save_json_file(file2,data)


# # 4. 对于SQL1选择的table，列出其所有的列（schema）
# def get_skeketon_schema(bird_file_path,file2,bird_database):
    
#     data=read_json_file(bird_file_path)

#     for item in data:  
#         sql1 = item['sql1']
#         sql2 = item['sql2']  
#         new_err_type = item['new_err_type'] 
#         db_id = item['db_id']  

#         print(sql1)
#         print(sql2)
#         print("\n")
#         if new_err_type=='result':

#             # 提取values
#             values = extract_values(sql1)


#             # 获取sql_schemas
#             sql_schemas1 = get_sql_schema(sql1)

#             # 表
#             tables = set(sql_schemas1[0])
#             # 查找表所有的列
#             columns = get_all_columns_for_db(bird_database, db_id, tables) 

#             # 最终结果以元组形式返回，保持原始格式
#             sql_schemas = (tables, columns, values)



#             schema_mapping = get_table_column_value(bird_database, db_id, sql_schemas, values)  
#             new_schema = format_database_schema(schema_mapping) 

#             skeleton2 = get_sql_skeleton(sql2)


#         else:
#             new_schema=''
#             skeleton2=''

#         item['sql1_schema']=new_schema
#         item['sql2_skeleton']=skeleton2
        
#     save_json_file(file2,data)