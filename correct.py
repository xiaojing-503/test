# from utils.save_json_file import save_json_file
# from utils.read_json_file import read_json_file
# from skeleton.sql_skeleton import get_sql_skeleton,get_sql_schema
# from skeleton.sql_value import extract_values
# from skeleton.mapping import get_table_column_value
# from utils.get_sql_schema_prompt import format_database_schema
# from utils.get_full_schema_prompt import parse_schema_to_string
# import json
# import re
# import numpy as np
# from utils.prompt import correction_instruction,correction_inputs
# from utils.get_response import get_deepseek_response
# from utils.process_llm_output_sql import format_sql_to_single_line


# BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'

# def join_error_types_out_file(file1_path, file2_path, output_file):  
#     # 读取JSON文件  
#     with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:  
#         data1 = json.load(file1)  
#         data2 = json.load(file2)  

#     new_data=[]
#     for item1, item2 in zip(data1, data2):  
#         # 获取两个文件中的new_err_type  
#         new_err_type1 = item1.get('new_err_type', '')  
#         new_err_type2 = item2.get('new_err_type', '')  
#         true_err_type = item1.get('err_type', '')  
#         db_id=item1.get('db_id','')
#         question=item1.get('question','')
#         pred_sql=item1.get('pred_sql','')
#         sql1=item1.get('sql1','')
#         sql2=item2.get('sql2','')


#         # 判断combine_err_type的值  
#         # 都判断为错误
#         if new_err_type1 != 'correct' and new_err_type2 != 'correct':  

#             # sql1的schema
#             skeleton = get_sql_skeleton(sql1)  
#             sql_schemas = get_sql_schema(sql1)  
#             values = extract_values(sql1)  
#             schema_mapping = get_table_column_value(BIRD_DATABASE, db_id, sql_schemas, values)  
#             new_schema = format_database_schema(schema_mapping)  


#             # sql2的skeleton
#             new_skeleton = skeleton = get_sql_skeleton(sql2)  

#             new_item = {  
#                 'db_id': db_id,  
#                 'question': question,  
#                 'pred_sql': pred_sql,  
#                 'err_type': true_err_type,  
#                 'sql1': sql1,  
#                 'sql2': sql2,  
#                 'sql1_schema': new_schema,
#                 'sql2_skeleton': new_skeleton
#             }  

#             new_data.append(new_item)

#     save_json_file(output_file,new_data)

# def correct_skeleton_schema(input_file, output_file):
#     data = read_json_file(input_file)
    
#     # 打开文件以追加模式写入
#     with open(output_file, 'w', encoding='utf-8') as f:
#         f.write("[")  # 写入 JSON 数组的起始符号
        
#         for i, item in enumerate(data):
#             question = item.get('question','')
#             sql2_skeleton = item.get('sql2_skeleton','')
#             sql1_schema = item.get('sql1_schema','')

#             inputs = correction_inputs.format(question=question,schema_new=sql1_schema,skeleton_new=sql2_skeleton)

#             print('instruction:',correction_instruction)
#             print('inputs:',inputs)

#             sql = get_deepseek_response(correction_instruction, inputs)
#             sql = format_sql_to_single_line(sql)
#             item['sql_new'] = sql

#             print('sql:',sql)

#             print("\n")
            
#             # 将当前处理的 item 追加写入文件
#             json.dump(item, f, ensure_ascii=False, indent=2)
            
#             # 如果不是最后一条，添加逗号
#             if i < len(data) - 1:
#                 f.write(",\n")

#         f.write("]")  # 写入 JSON 数组的结束符号
    
#     print(f"所有数据已保存到文件：{output_file}")

# file1='/root/Schema-Value/data/bird/dataset_new_new/foreign/merge1_gpt_result_deepseek_foreign.json'
# file2='/root/Schema-Value/data/bird/dataset_new_new/foreign/merge2_deepseek_result_deepseek_foreign.json'

# output_file='/root/Schema-Value/data/bird/dataset_new_new/error.json'

# # join_error_types_out_file(file1, file2, output_file)

# correct_file='/root/Schema-Value/data/bird/dataset_new_new/correct/corrected.json'

# correct_skeleton_schema(output_file,correct_file)


import os
# from main import correct
# BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
# directory='/root/Schema-Value/data/bird/dataset_new_new_new/deepseek'
# directory_new='/root/Schema-Value/data/bird/dataset_new_new_new/deepseek_new_new_new'

# # 处理反引号
# bird_process=os.path.join(directory, 'bird_dev_result_process.json')

# # 取sql0和sql1的交集
# bird_skeleton_schema_file=os.path.join(directory_new, 'bird_dev_result_skeleton_schema.json')
# bird_corrected_file=os.path.join(directory_new, 'bird_corrected.json')
# correct(bird_process,bird_skeleton_schema_file,bird_corrected_file,BIRD_DATABASE)
# evaluate_file=os.path.join(directory_new, 'bird_evaluated.json')
# evaluation
bird_corrected_file='/root/Schema-Value/data/bird/dataset_new_new_new/deepseek/bird_dev_result.json'
evaluate_file='/root/Schema-Value/data/bird/dataset_new_new_new/deepseek/evaluated_test.json'
os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {bird_corrected_file} {evaluate_file}")