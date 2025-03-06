# '''
# 1. 读取完整的1534条数据 -
# 2. process处理数据 -
# 3. 如果是系统错误，pass，标识new_err_type为system -
# 4. 如果不是系统错误，首先进行值错误验证，标识new_err_type为empty -
# 5. 剩余的进行双重验证，对于每一个sql，跑sql1，sql2，并且执行，如果XXXX则判断为XXX，标识new_err_type为skeleton_schema
# 6. 获取accuracy report
# --------------------------------
# 纠正
# 1. 系统错误先不做处理
# 2. 值错误先不做处理
# 3. 提取sql1的schema，sql2的skeleton，给出提示纠正
# 4. 计算准确率EX
# '''

# from utils.save_json_file import save_json_file
# from utils.read_json_file import read_json_file
# from skeleton.sql_skeleton import get_sql_skeleton,get_sql_schema
# from skeleton.sql_value import extract_values, extract_column_and_value
# from skeleton.mapping import get_table_column_value
# from utils.get_sql_schema_prompt import format_database_schema
# from utils.get_full_schema_prompt import parse_schema_to_string
# from check.check_value import check_value_in_any_table
# from generate_sql import question_schema_full_skeletion_sql, question_schema_new_sql
# import json
# import os
# from utils.check_sql_result import compare_sql_results,compute_report, get_system_error_desc
# from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
# import transformers,torch
# from process.correct_process import get_skeketon_schema,replace_special_characters_in_sql
# from utils.prompt import result_correction_instruction,result_correction_inputs,empty_correction_instruction,empty_correction_inputs,system_correction_instruction,system_correction_inputs
# from utils.get_response import get_deepseek_response,get_codes_response,get_llm_response
# from utils.process_llm_output_sql import format_sql_to_single_line
# from transformers import AutoModelForCausalLM, AutoTokenizer

# def process_bird_data(bird_file_path,file2,bird_database):
    
#     data=read_json_file(bird_file_path)

#     new_data = []  

#     for item in data:  
#         full_schema = item['schema_sequence']  
#         question = item['question'] + " " + item['evidence'] 
#         err_gold = item['err_gold']
#         err_pred = item['err_pred']  
#         err_type = item['err_type'] 
#         difficulty = item['difficulty'] 
#         db_id = item['db_id']  
#         new_err_type = ''

#         print(err_pred)
#         # 这个sqlglot会产生解析错误
#         if err_type=='system':
#             new_schema=''
#             skeleton=''
#             new_err_type = 'system'
#         else:
#             # 检查是否是empty错误
#             values = extract_values(err_pred)
#             # values: ['directed_by = Ben Jones']
#             extracted_conditions = extract_column_and_value(values)  
#             print(extracted_conditions)  
            
#             # 默认假设没有满足条件的行  
#             res = 1  
      
#             # 检查每个条件  
#             for column, value in extracted_conditions:  
#                 # 如果其中任意一个条件不成立，则设置为0
#                 if value=='':
#                     continue  
#                 if column is not None:  
#                     res = check_value_in_any_table(column, value, db_id,  db_path = bird_database)  
#                     if res == 0:  
#                         break  
#             # print("check完毕！")
#             if res == 0:  
#                 new_err_type = "empty"  
            
#             # 假设get_sql_skeleton，get_sql_schema和extract_values是已定义的函数  
#             skeleton = get_sql_skeleton(err_pred)  
#             sql_schemas = get_sql_schema(err_pred)  
#             # values = extract_values(err_pred)  

#             # 假设get_table_column_value是已定义的函数，用来获取映射关系  
#             # print(pred_sql)
#             schema_mapping = get_table_column_value(bird_database, db_id, sql_schemas, values)  

#             # 假设format_database_schema是已定义的函数，用来格式化架构  
#             new_schema = format_database_schema(schema_mapping)  
#         schema=parse_schema_to_string(full_schema)

#         # 构建新的条目  
#         new_item = {  
#             'db_id': db_id,  
#             'difficulty': difficulty,
#             'question': question,  
#             'err_gold': err_gold,  
#             'err_pred': err_pred,  
#             'err_type': err_type,  
#             'full_schema': schema,  
#             'new_schema': new_schema,  
#             'skeleton': skeleton,
#             'new_err_type': new_err_type
#         }  

#         # 将新条目添加到新数据列表中  
#         new_data.append(new_item)  

#     save_json_file(file2,new_data)

# def generate_sql(processed_file,output_file, llm_mode, pipeline=None):
#     data = read_json_file(processed_file)
#     # 打开文件以追加模式写入
#     with open(output_file, 'w', encoding='utf-8') as f:
#         f.write("[")  # 写入 JSON 数组的起始符号
        
#         for i, item in enumerate(data):
#             if item['new_err_type']=='':
#                 sql1 = question_schema_full_skeletion_sql(item,llm_mode,pipeline)
#                 item['sql1'] = sql1
#                 sql2 = question_schema_new_sql(item,llm_mode,pipeline)
#                 item['sql2'] = sql2
#             else:
#                 item['sql1'] = ''
#                 item['sql2'] = ''
#             # 将当前处理的 item 追加写入文件
#             json.dump(item, f, ensure_ascii=False, indent=2)
            
#             # 如果不是最后一条，添加逗号
#             if i < len(data) - 1:
#                 f.write(",\n")

#         f.write("]")  # 写入 JSON 数组的结束符号
    
#     print(f"所有数据已保存到文件：{output_file}")


# def identify_error(sql_file,output_file,bird_database,timeout=10):
#     data = read_json_file(sql_file)
#     for item in data:
#         if item['new_err_type']=='':
#             sql_initial = item['err_pred']
#             sql1 = item['sql1']
#             sql2 = item['sql2']
#             db_id = item['db_id']
#             err_type = item['err_type']

#             # 比较 SQL 结果
#             comparison_result1 = compare_sql_results(bird_database, db_id, sql_initial, sql1, timeout)
#             comparison_result2 = compare_sql_results(bird_database, db_id, sql_initial, sql2, timeout)
#             item['err_type1'] = comparison_result1
#             item['err_type2'] = comparison_result2

#             if comparison_result1!='correct' and comparison_result2!='correct':
#                 # 根据比较结果更新 new_err_type
#                 item['new_err_type'] = 'result'
#             else:
#                 item['new_err_type'] = 'correct'
#         else:
#             item['err_type1'] = ''
#             item['err_type2'] = ''

#     save_json_file(output_file, data)

# def compute(file):

#     compute_report(file,'err_type1')
#     print("----------------------------------------------")
#     compute_report(file,'err_type2')
#     print("----------------------------------------------")
#     compute_report(file,'new_err_type')
#     print("----------------------------------------------")

# def compute_union(file):
#     data = read_json_file(file)
#     y_true=[]
#     y_pred=[]
#     pred_err_count=0
#     true_err_count=0
#     for item in data:
#         err_type=item['err_type']
#         # 根据 err_type 确定 true label
#         true_label = 1 if err_type == "correct" else 0
#         # 根据 new_err_type 确定 predicted label
#         pred_label = 0 if item['err_type1'] != "correct" or item['err_type2'] != "correct" else 1

#         y_true.append(true_label)
#         y_pred.append(pred_label)

#         if item['err_type1'] != "correct" or item['err_type2'] != "correct":
#             pred_err_count+=1
#             if err_type!='correct':
#                 true_err_count+=1


#     print("预测为错误的：",pred_err_count)
#     print("实际为错误的：",true_err_count)
#     print("precision:", true_err_count*1.0 / pred_err_count) 

    

#     # 如果没有有效的预测，则避免计算
#     if y_true and y_pred:

#         report = classification_report(y_true, y_pred, target_names=["incorrect", "correct"])
#         print(report)
#         report_dict = classification_report(y_true, y_pred, target_names=["incorrect", "correct"], output_dict=True)  

#         # 格式化和打印报告  
#         print("Classification Report:")  
#         for label, metrics in report_dict.items():  
#             if isinstance(metrics, dict):  # 表示这是类别级别的统计  
#                 print(f"{label}:")  
#                 for metric, value in metrics.items():  
#                     print(f"  {metric}: {value:.3f}")  
#             else:  # 针对"accuracy"这个单值指标  
#                 print(f"{label}: {metrics:.3f}")  
#         # 使用 scikit-learn 计算 precision, recall, F1
#         precision = precision_score(y_true, y_pred) * 100
#         recall = recall_score(y_true, y_pred) * 100
#         f1 = f1_score(y_true, y_pred) * 100

#         print("Precision: {:.2f}%".format(precision))
#         print("Recall: {:.2f}%".format(recall))
#         print("F1-score: {:.2f}%".format(f1))
#     else:
#         print("没有有效的预测数据，无法计算 Precision/Recall/F1-score")

# # -----------------------------纠正-------------------------------------
# # 
# import time
# def correct(result_file,skeleton_schema_file,corrected_file,database_path):
#     get_skeketon_schema(result_file,skeleton_schema_file,database_path)
#     data = read_json_file(skeleton_schema_file) 
#     # 打开文件以追加模式写入
#     with open(corrected_file, 'w', encoding='utf-8') as f:
#         f.write("[")  # 写入 JSON 数组的起始符号
        
#         for i, item in enumerate(data):
#             question = item.get('question','')
#             sql2_skeleton = item.get('sql2_skeleton','')
#             sql1_schema = item.get('sql1_schema','')
#             new_err_type = item['new_err_type'] 
            
#             if new_err_type=='result':
#                 result_inputs = result_correction_inputs.format(question=question,schema_new=sql1_schema,skeleton_new=sql2_skeleton)

#                 print('instruction:',result_correction_instruction)
#                 print('inputs:',result_inputs)
#                 while True:
#                     try:
#                         sql = get_deepseek_response(result_correction_instruction, result_inputs)
#                         sql = format_sql_to_single_line(sql)
#                         item['sql_new'] = sql
#                         print('sql:', sql)
#                         break  # 成功获取 SQL，跳出循环
#                     except Exception as e:
#                         print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
#                         time.sleep(3)
                
#                 print("\n")
                
#             elif new_err_type=='empty':
#                 empty_inputs = ''
                
#                 while True:
#                     try:
#                         sql = get_deepseek_response(empty_correction_instruction, empty_inputs)
#                         sql = format_sql_to_single_line(sql)
#                         item['sql_new'] = sql
#                         print('sql:', sql)
#                         break  # 成功获取 SQL，跳出循环
#                     except Exception as e:
#                         print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
#                         time.sleep(3)
                
#                 print("\n")

#             elif new_err_type=='system':
#                 sql_schema = item.get('full_schema','')
#                 err_pred = item.get('err_pred','')
#                 db_id = item.get('db_id','')
#                 err_desc = get_system_error_desc(database_path, db_id, err_pred)
#                 sql_schema = item.get('full_schema','')
#                 system_inputs = system_correction_inputs.format(question=question,schema_new=sql_schema,err_pred=err_pred,err_desc=err_desc)
#                 while True:
#                     try:
#                         sql = get_deepseek_response(system_correction_instruction, system_inputs)
#                         sql = format_sql_to_single_line(sql)
#                         item['sql_new'] = sql
#                         print('sql:', sql)
#                         break  # 成功获取 SQL，跳出循环
#                     except Exception as e:
#                         print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
#                         time.sleep(3)
                
#                 print("\n")
        
#             else:
#                 item['sql_new'] = item['err_pred']
                
#             # 将当前处理的 item 追加写入文件
#             json.dump(item, f, ensure_ascii=False, indent=2)
            
#             # 如果不是最后一条，添加逗号
#             if i < len(data) - 1:
#                 f.write(",\n")
#         f.write("]")  # 写入 JSON 数组的结束符号

# # # codes第一遍生成结果
# # bird_path='/root/Schema-Value/data/bird/dataset/bird_dev_copy2.json'
# BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
# # directory='/root/Schema-Value/data/bird/dataset_new_new_new/deepseek'
# # bird_output='/root/Schema-Value/data/bird/dataset_new_new_new/bird_dev.json'
# # # # 会验证empty错误
# # # process_bird_data(bird_path,bird_output,BIRD_DATABASE)
# # # bird_sql= os.path.join(directory, 'bird_dev_sql.json')
# # # MODEL_ID="/root/hdd/Llama-3-8B-Instruct"
# # # CUDA_ID="cuda:1"
# # # pipeline = transformers.pipeline(
# # #     "text-generation",
# # #     model=MODEL_ID,
# # #     model_kwargs={"torch_dtype": torch.bfloat16},
# # #     device=CUDA_ID,
# # # )
# # # generate_sql(bird_output,bird_sql,2,pipeline)

# # bird_result = os.path.join(directory, 'bird_dev_result.json')
# # bird_sql = '/root/Schema-Value/data/bird/dataset_new_new_new/deepseek/bird_dev_sql_updated.json'
# # # bird_sql = '/root/Schema-Value/data/bird/dataset_new_new_new/llama/bird_dev_sql_updated.json'
# # # bird_result = '/root/Schema-Value/data/bird/dataset_new_new_new/llama/bird_dev_result_upadted.json'
# # # identify_error(bird_sql,bird_result,BIRD_DATABASE)
# # compute(bird_result)
# # compute_union(bird_result)
# # # # 处理反引号， 已修改为\"
# # # bird_process=os.path.join(directory, 'bird_dev_result_process.json')
# # # # replace_special_characters_in_sql(bird_result,bird_process)

# # # bird_skeleton_schema_file=os.path.join(directory, 'bird_dev_result_skeleton_schema.json')
# # # bird_corrected_file=os.path.join(directory, 'bird_corrected.json')
# # # correct(bird_process,bird_skeleton_schema_file,bird_corrected_file,BIRD_DATABASE)
# # # evaluate_file=os.path.join(directory, 'bird_evaluated.json')
# # # # evaluation

# # # os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {bird_corrected_file} {evaluate_file}")


# # get_system_error_desc(BIRD_DATABASE, 'card_games', "SELECT cards.name FROM cards INNER JOIN set_translations ON cards.uuid = set_translations.uuid INNER JOIN sets ON set_translations.setcode = sets.code WHERE sets.name = 'Coldsnap' AND set_translations.language = 'Italian' ORDER BY cards.convertedmanacost DESC LIMIT 1")



# # # codes第二遍生成结果
# # bird_path='/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/bird_dev_tmp.json'
# # BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
# # directory='/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/llama'
# # bird_output='/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/bird_dev.json'
# # # 会验证empty错误
# # # process_bird_data(bird_path,bird_output,BIRD_DATABASE)
# # bird_sql= os.path.join(directory, 'bird_dev_sql.json')
# # MODEL_ID="/root/hdd/Llama-3-8B-Instruct"
# # CUDA_ID="cuda:1"
# # pipeline = transformers.pipeline(
# #     "text-generation",
# #     model=MODEL_ID,
# #     model_kwargs={"torch_dtype": torch.bfloat16},
# #     device=CUDA_ID,
# # )
# # # pipeline=None
# # generate_sql(bird_output,bird_sql,2,pipeline)
# # bird_result = os.path.join(directory, 'bird_dev_result.json')

# # identify_error(bird_sql,bird_result,BIRD_DATABASE)
# # compute(bird_result)
# # compute_union(bird_result)
# # # 处理反引号
# # # bird_process=os.path.join(directory, 'bird_dev_result_process.json')
# # # # replace_special_characters_in_sql(bird_result,bird_process)

# # # bird_skeleton_schema_file=os.path.join(directory, 'bird_dev_result_skeleton_schema.json')
# # # bird_corrected_file=os.path.join(directory, 'bird_corrected.json')
# # # # correct(bird_process,bird_skeleton_schema_file,bird_corrected_file,BIRD_DATABASE)
# # # evaluate_file=os.path.join(directory, 'bird_evaluated.json')
# # # # evaluation

# # # os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {bird_corrected_file} {evaluate_file}")




'''
1. 读取完整的1534条数据 -
2. process处理数据 -
3. 如果是系统错误，pass，标识new_err_type为system -
4. 如果不是系统错误，首先进行值错误验证，标识new_err_type为empty -
5. 剩余的进行双重验证，对于每一个sql，跑sql1，sql2，并且执行，如果XXXX则判断为XXX，标识new_err_type为skeleton_schema
6. 获取accuracy report
--------------------------------
纠正
1. 系统错误先不做处理
2. 值错误先不做处理
3. 提取sql1的schema，sql2的skeleton，给出提示纠正
4. 计算准确率EX
'''

from utils.save_json_file import save_json_file
from utils.read_json_file import read_json_file
from skeleton.sql_skeleton import get_sql_skeleton,get_sql_schema
from skeleton.sql_value import extract_values, extract_column_and_value
from skeleton.mapping import get_table_column_value
from utils.get_sql_schema_prompt import format_database_schema
from utils.get_full_schema_prompt import parse_schema_to_string
from check.check_value import check_value_in_any_table
from generate_sql import question_schema_full_skeletion_sql, question_schema_new_sql
import json
import os
from utils.check_sql_result import compare_sql_results,compute_report,get_system_error_desc
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
import transformers,torch
from process.correct_process import get_skeketon_schema,replace_special_characters_in_sql
from utils.prompt import result_correction_instruction,result_correction_inputs,empty_correction_instruction,empty_correction_inputs,system_correction_instruction,system_correction_inputs
from utils.get_response import get_deepseek_response,get_codes_response,get_llm_response
from utils.process_llm_output_sql import format_sql_to_single_line
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.correct_value import find_similar_values_in_all_tables

def process_bird_data(bird_file_path,file2,bird_database):
    
    data=read_json_file(bird_file_path)

    new_data = []  

    for item in data:  
        full_schema = item['schema_sequence']  
        question = item['question'] + " " + item['evidence'] 
        err_gold = item['err_gold']
        err_pred = item['err_pred']  
        err_type = item['err_type'] 
        difficulty = item['difficulty'] 
        db_id = item['db_id']  
        new_err_type = ''

        print(err_pred)
        # 这个sqlglot会产生解析错误
        if err_type=='system':
            new_schema=''
            skeleton=''
            new_err_type = 'system'
        else:
            # 检查是否是empty错误
            values = extract_values(err_pred)
            # values: ['directed_by = Ben Jones']
            extracted_conditions = extract_column_and_value(values)  
            print(extracted_conditions)  
            
            # 默认假设没有满足条件的行  
            res = 1  
      
            # 检查每个条件  
            for column, value in extracted_conditions:  
                # 如果其中任意一个条件不成立，则设置为0
                if value=='':
                    continue  
                if column is not None:  
                    res = check_value_in_any_table(column, value, db_id,  db_path = bird_database)  
                    if res == 0:  
                        break  
            # print("check完毕！")
            if res == 0:  
                new_err_type = "empty"  
            
            # 假设get_sql_skeleton，get_sql_schema和extract_values是已定义的函数  
            skeleton = get_sql_skeleton(err_pred)  
            sql_schemas = get_sql_schema(err_pred)  
            # values = extract_values(err_pred)  

            # 假设get_table_column_value是已定义的函数，用来获取映射关系  
            # print(pred_sql)
            schema_mapping = get_table_column_value(bird_database, db_id, sql_schemas, values)  

            # 假设format_database_schema是已定义的函数，用来格式化架构  
            new_schema = format_database_schema(schema_mapping)  
        schema=parse_schema_to_string(full_schema)

        # 构建新的条目  
        new_item = {  
            'db_id': db_id,  
            'difficulty': difficulty,
            'question': question,  
            'err_gold': err_gold,  
            'err_pred': err_pred,  
            'err_type': err_type,  
            'full_schema': schema,  
            'new_schema': new_schema,  
            'skeleton': skeleton,
            'new_err_type': new_err_type
        }  

        # 将新条目添加到新数据列表中  
        new_data.append(new_item)  

    save_json_file(file2,new_data)

def generate_sql(processed_file,output_file, llm_mode, pipeline=None):
    data = read_json_file(processed_file)
    # 打开文件以追加模式写入
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("[")  # 写入 JSON 数组的起始符号
        
        for i, item in enumerate(data):
            if item['new_err_type']=='':
                sql1 = question_schema_full_skeletion_sql(item,llm_mode,pipeline)
                item['sql1'] = sql1
                sql2 = question_schema_new_sql(item,llm_mode,pipeline)
                item['sql2'] = sql2
            else:
                item['sql1'] = ''
                item['sql2'] = ''
            # 将当前处理的 item 追加写入文件
            json.dump(item, f, ensure_ascii=False, indent=2)
            
            # 如果不是最后一条，添加逗号
            if i < len(data) - 1:
                f.write(",\n")

        f.write("]")  # 写入 JSON 数组的结束符号
    
    print(f"所有数据已保存到文件：{output_file}")


def identify_error(sql_file,output_file,bird_database,timeout=10):
    data = read_json_file(sql_file)
    for item in data:
        if item['new_err_type']=='':
            sql_initial = item['err_pred']
            sql1 = item['sql1']
            sql2 = item['sql2']
            db_id = item['db_id']
            err_type = item['err_type']

            # 比较 SQL 结果
            comparison_result1 = compare_sql_results(bird_database, db_id, sql_initial, sql1, timeout)
            comparison_result2 = compare_sql_results(bird_database, db_id, sql_initial, sql2, timeout)
            item['err_type1'] = comparison_result1
            item['err_type2'] = comparison_result2

            if comparison_result1!='correct' and comparison_result2!='correct':
                # 根据比较结果更新 new_err_type
                item['new_err_type'] = 'result'
            else:
                item['new_err_type'] = 'correct'
        else:
            item['err_type1'] = ''
            item['err_type2'] = ''

    save_json_file(output_file, data)

def compute(file):

    compute_report(file,'err_type1')
    print("----------------------------------------------")
    compute_report(file,'err_type2')
    print("----------------------------------------------")
    compute_report(file,'new_err_type')
    print("----------------------------------------------")

def compute_union(file):
    data = read_json_file(file)
    y_true=[]
    y_pred=[]
    pred_err_count=0
    true_err_count=0
    for item in data:
        err_type=item['err_type']
        # 根据 err_type 确定 true label
        true_label = 1 if err_type == "correct" else 0
        # 根据 new_err_type 确定 predicted label
        pred_label = 0 if item['err_type1'] != "correct" or item['err_type2'] != "correct" else 1

        y_true.append(true_label)
        y_pred.append(pred_label)

        if item['err_type1'] != "correct" or item['err_type2'] != "correct":
            pred_err_count+=1
            if err_type!='correct':
                true_err_count+=1


    print("预测为错误的：",pred_err_count)
    print("实际为错误的：",true_err_count)
    print("precision:", true_err_count*1.0 / pred_err_count) 

    

    # 如果没有有效的预测，则避免计算
    if y_true and y_pred:

        report = classification_report(y_true, y_pred, target_names=["incorrect", "correct"])
        print(report)
        report_dict = classification_report(y_true, y_pred, target_names=["incorrect", "correct"], output_dict=True)  

        # 格式化和打印报告  
        print("Classification Report:")  
        for label, metrics in report_dict.items():  
            if isinstance(metrics, dict):  # 表示这是类别级别的统计  
                print(f"{label}:")  
                for metric, value in metrics.items():  
                    print(f"  {metric}: {value:.3f}")  
            else:  # 针对"accuracy"这个单值指标  
                print(f"{label}: {metrics:.3f}")  
        # 使用 scikit-learn 计算 precision, recall, F1
        precision = precision_score(y_true, y_pred) * 100
        recall = recall_score(y_true, y_pred) * 100
        f1 = f1_score(y_true, y_pred) * 100

        print("Precision: {:.2f}%".format(precision))
        print("Recall: {:.2f}%".format(recall))
        print("F1-score: {:.2f}%".format(f1))
    else:
        print("没有有效的预测数据，无法计算 Precision/Recall/F1-score")

# -----------------------------纠正-------------------------------------
# 
import time
# deepseek
def correct(result_file,skeleton_schema_file,corrected_file,database_path):
    get_skeketon_schema(result_file,skeleton_schema_file,database_path)
    data = read_json_file(skeleton_schema_file) 
    # 打开文件以追加模式写入
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write("[")  # 写入 JSON 数组的起始符号
        
        for i, item in enumerate(data):
            question = item.get('question','')
            sql2_skeleton = item.get('sql2_skeleton','')
            sql1_schema = item.get('sql1_schema','')
            new_err_type = item['new_err_type'] 
            
            if new_err_type=='result':
                result_inputs = result_correction_inputs.format(question=question,schema_new=sql1_schema,skeleton_new=sql2_skeleton)

                print('instruction:',result_correction_instruction)
                print('inputs:',result_inputs)
                while True:
                    try:
                        sql = get_deepseek_response(result_correction_instruction, result_inputs)
                        sql = format_sql_to_single_line(sql)
                        item['sql_new'] = sql
                        print('sql:', sql)
                        break  # 成功获取 SQL，跳出循环
                    except Exception as e:
                        print(f"获取 SQL 失败，错误信息: {e}，等待 60 秒后重试...")
                        time.sleep(60)
                
                print("\n")

            elif new_err_type=='empty':
                
                err_pred = item.get('err_pred','')
                db_id = item.get('db_id','')
                db_path = os.path.join(database_path, db_id, f"{db_id}.sqlite")

                vvalues=''
                values = extract_values(err_pred)
                # values: ['directed_by = Ben Jones']
                extracted_conditions = extract_column_and_value(values)  
                # print(extracted_conditions)  
                # 检查每个value
                for column, value in extracted_conditions:  
                    if value=='':
                        continue  
                    if column is not None:  
                        similar_values = find_similar_values_in_all_tables(db_path, value, case_sensitive=False)
                        for table, col, val in similar_values:
                          vvalues += f"Column: {col}, Value: {val}; "
                print("vvalues:",vvalues)    
                empty_inputs = empty_correction_inputs.format(err_pred=err_pred,values=vvalues)
                while True:
                    try:
                        sql = get_deepseek_response(empty_correction_instruction, empty_inputs)
                        sql = format_sql_to_single_line(sql)
                        item['sql_new'] = sql
                        print('sql:', sql)
                        break  # 成功获取 SQL，跳出循环
                    except Exception as e:
                        print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                        time.sleep(3)
                
                print("\n")

            elif new_err_type=='system':
                sql_schema = item.get('full_schema','')
                err_pred = item.get('err_pred','')
                db_id = item.get('db_id','')
                err_desc = get_system_error_desc(database_path, db_id, err_pred)
                sql_schema = item.get('full_schema','')
                system_inputs = system_correction_inputs.format(question=question,schema_new=sql_schema,err_pred=err_pred,err_desc=err_desc)
                while True:
                    try:
                        sql = get_deepseek_response(system_correction_instruction, system_inputs)
                        sql = format_sql_to_single_line(sql)
                        item['sql_new'] = sql
                        print('sql:', sql)
                        break  # 成功获取 SQL，跳出循环
                    except Exception as e:
                        print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                        time.sleep(3)
                
                print("\n")
        
            else:
                item['sql_new'] = item['err_pred']
                
            # 将当前处理的 item 追加写入文件
            json.dump(item, f, ensure_ascii=False, indent=2)
            
            # 如果不是最后一条，添加逗号
            if i < len(data) - 1:
                f.write(",\n")
        f.write("]")  # 写入 JSON 数组的结束符号

def prepare_inputs(prefix_seq, tokenizer, max_prefix_length):
    """
    对输入的 `prefix_seq` 进行 tokenization 处理，使其符合模型输入格式。
    """
    input_ids = [tokenizer.bos_token_id] + tokenizer(prefix_seq, truncation=False)["input_ids"]

    if len(input_ids) > max_prefix_length:
        print("The current input sequence exceeds max_tokens, truncating.")
        input_ids = [tokenizer.bos_token_id] + input_ids[-(max_prefix_length-1):]
    
    attention_mask = [1] * len(input_ids)
    
    return {
        "input_ids": torch.tensor([input_ids], dtype=torch.int64),  # batch_size=1
        "attention_mask": torch.tensor([attention_mask], dtype=torch.int64)
    }


# codes
def correct2(result_file,skeleton_schema_file,corrected_file,database_path,llm_path):
    data = read_json_file(skeleton_schema_file) 
    max_tokens = 4096 
    max_new_tokens = 256

    model = AutoModelForCausalLM.from_pretrained(llm_path, device_map = "auto", torch_dtype = torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(llm_path)

    model.eval()
    # 打开文件以追加模式写入
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write("[")  # 写入 JSON 数组的起始符号
        
        for i, item in enumerate(data):
            question = item.get('question','')
            sql2_skeleton = item.get('sql2_skeleton','')
            sql1_schema = item.get('sql1_schema','')
            new_err_type = item['new_err_type'] 
            
            if new_err_type=='result':
                result_inputs = result_correction_inputs.format(question=question,schema_new=sql1_schema,skeleton_new=sql2_skeleton)

                # print('instruction:',result_correction_instruction)
                # print('inputs:',result_inputs)
                # while True:
                #     try:
                #         sql = get_deepseek_response(result_correction_instruction, result_inputs)
                #         sql = format_sql_to_single_line(sql)
                #         item['sql_new'] = sql
                #         print('sql:', sql)
                #         break  # 成功获取 SQL，跳出循环
                #     except Exception as e:
                #         print(f"获取 SQL 失败，错误信息: {e}，等待 60 秒后重试...")
                #         time.sleep(60)
                
                # print("\n")

            elif new_err_type=='empty':
                
                err_pred = item.get('err_pred','')
                db_id = item.get('db_id','')
                db_path = os.path.join(database_path, db_id, f"{db_id}.sqlite")

                print("err_pred:",err_pred)
                print(db_id)

                vvalues=''
                values = extract_values(err_pred)
                # values: ['directed_by = Ben Jones']
                extracted_conditions = extract_column_and_value(values)  
                # print(extracted_conditions)  
                # 检查每个value
                for column, value in extracted_conditions:  
                    if value=='':
                        continue  
                    if column is not None:  
                        print(value)
                        similar_values = find_similar_values_in_all_tables(db_path, value, case_sensitive=False)
                        for table, col, val in similar_values:
                          vvalues += f"[{col} = '{val}']; "
                print("vvalues:",vvalues)    
                empty_inputs = empty_correction_inputs.format(err_pred=err_pred,question=question,values=vvalues)
                while True:
                    try:
                        # get_gpt_response, get_deepseek_response
                        tokenized_inputs = prepare_inputs(empty_correction_instruction+empty_inputs, tokenizer, max_tokens - max_new_tokens)
                        print('tokenized_inputs:', tokenized_inputs)

                        # 生成 SQL
                        sql = get_codes_response(model, tokenized_inputs, tokenizer, max_new_tokens)  # 可调整 max_new_tokens
                        sql = format_sql_to_single_line(sql[0])
                        item['sql_new'] = sql
                        print('sql:', sql)
                        break  # 成功获取 SQL，跳出循环
                    except Exception as e:
                        print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                        time.sleep(3)
                
                print("\n")

            elif new_err_type=='system':
                # continue
                sql_schema = item.get('full_schema','')
                err_pred = item.get('err_pred','')
                db_id = item.get('db_id','')
                err_desc = get_system_error_desc(database_path, db_id, err_pred)
                sql_schema = item.get('full_schema','')
                system_inputs = system_correction_inputs.format(question=question,schema_new=sql_schema,err_pred=err_pred,err_desc=err_desc)
                while True:
                    try:
                        tokenized_inputs = prepare_inputs(system_correction_instruction+system_inputs, tokenizer, max_tokens - max_new_tokens)
                        print('tokenized_inputs:', tokenized_inputs)

                        # 生成 SQL
                        sql = get_codes_response(model, tokenized_inputs, tokenizer, max_new_tokens)
                        sql = format_sql_to_single_line(sql[0])
                        item['sql_new'] = sql
                        print('sql:', sql)
                        break  # 成功获取 SQL，跳出循环
                    except Exception as e:
                        print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                        time.sleep(3)
                
                print("\n")
        
            else:
                item['sql_new'] = item['err_pred']
                
            # 将当前处理的 item 追加写入文件
            json.dump(item, f, ensure_ascii=False, indent=2)
            
            # 如果不是最后一条，添加逗号
            if i < len(data) - 1:
                f.write(",\n")
        f.write("]")  # 写入 JSON 数组的结束符号

# 
# llama
# def correct3(result_file,skeleton_schema_file,corrected_file,database_path):
#     # get_skeketon_schema(result_file,skeleton_schema_file,database_path)
#     data = read_json_file(skeleton_schema_file) 
#     model='/root/hdd/Llama-3-8B-Instruct'
#     pipeline = transformers.pipeline(
#         "text-generation",
#         model=model,
#         model_kwargs={"torch_dtype": torch.bfloat16},
#         device="cuda:1",
#     )
#     # 打开文件以追加模式写入
#     with open(corrected_file, 'w', encoding='utf-8') as f:
#         f.write("[")  # 写入 JSON 数组的起始符号
        
#         for i, item in enumerate(data):
#             question = item.get('question','')
#             sql2_skeleton = item.get('sql2_skeleton','')
#             sql1_schema = item.get('sql1_schema','')
#             new_err_type = item['new_err_type'] 
            
#             if new_err_type=='result':
#                 inputs = correction_inputs.format(question=question,schema_new=sql1_schema,skeleton_new=sql2_skeleton)

#                 print('instruction:',correction_instruction)
#                 print('inputs:',inputs)

#                 sql = get_llm_response(correction_instruction, inputs, pipeline)
#                 sql = format_sql_to_single_line(sql)
#                 item['sql_new'] = sql

#                 print('sql:',sql)

#                 print("\n")
#             else:
#                 item['sql_new'] = item['err_pred']
                
#             # 将当前处理的 item 追加写入文件
#             json.dump(item, f, ensure_ascii=False, indent=2)
            
#             # 如果不是最后一条，添加逗号
#             if i < len(data) - 1:
#                 f.write(",\n")
#         f.write("]")  # 写入 JSON 数组的结束符号

        
# bird_path='/root/Schema-Value/data/bird/dataset/bird_dev.json'
# BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
# directory='/root/Schema-Value/data/bird/dataset_new_new_new/deepseek'
# bird_output='/root/Schema-Value/data/bird/dataset_new_new_new/bird_dev.json'
# # 会验证empty错误
# process_bird_data(bird_path,bird_output,BIRD_DATABASE)
# bird_sql= os.path.join(directory, 'bird_dev_sql.json')
# MODEL_ID="/root/hdd/Llama-3-8B-Instruct"
# CUDA_ID="cuda:1"
# pipeline = transformers.pipeline(
#     "text-generation",
#     model=MODEL_ID,
#     model_kwargs={"torch_dtype": torch.bfloat16},
#     device=CUDA_ID,
# )
# generate_sql(bird_output,bird_sql,2,pipeline)
# bird_result = os.path.join(directory, 'bird_dev_result.json')

# identify_error(bird_sql,bird_result,BIRD_DATABASE)
# compute(bird_result)
# compute_union(bird_result)
# # 处理反引号
# bird_process=os.path.join(directory, 'bird_dev_result_process.json')
# # replace_special_characters_in_sql(bird_result,bird_process)

# bird_skeleton_schema_file=os.path.join(directory, 'bird_dev_result_skeleton_schema.json')
# bird_corrected_file=os.path.join(directory, 'bird_corrected.json')
# # correct(bird_process,bird_skeleton_schema_file,bird_corrected_file,BIRD_DATABASE)
# evaluate_file=os.path.join(directory, 'bird_evaluated.json')
# # evaluation

# os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {bird_corrected_file} {evaluate_file}")



# bird_path='/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/bird_dev_tmp.json'
BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
directory='/root/Schema-Value/data/bird/dataset_new_new_new/codes/'
# bird_output='/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/bird_dev.json'
# 会验证empty错误
# process_bird_data(bird_path,bird_output,BIRD_DATABASE)
# bird_sql= os.path.join(directory, 'bird_dev_sql.json')
# MODEL_ID="/root/hdd/Llama-3-8B-Instruct"
# CUDA_ID="cuda:1"
# pipeline = transformers.pipeline(
#     "text-generation",
#     model=MODEL_ID,
#     model_kwargs={"torch_dtype": torch.bfloat16},
#     device=CUDA_ID,
# )
# pipeline=None
# 1: gpt
# 2: llm
# 3: deepseek
# generate_sql(bird_output,bird_sql,3,pipeline)
# bird_result = os.path.join(directory, 'bird_dev_result.json')

# identify_error(bird_sql,bird_result,BIRD_DATABASE)
# compute(bird_result)
# compute_union(bird_result)
# 处理反引号
bird_process=os.path.join(directory, 'bird_dev_result_process.json')
# # replace_special_characters_in_sql(bird_result,bird_process)

# bird_skeleton_schema_file=os.path.join(directory, 'bird_dev_result_skeleton_schema.json')
bird_skeleton_schema_file = os.path.join(directory, 'bird_corrected_updated2.json')
bird_corrected_file=os.path.join(directory, 'bird_corrected_updated_system_empty.json')
llm_path = '/root/hdd/codes-7b'

correct2(bird_process,bird_skeleton_schema_file,bird_corrected_file,BIRD_DATABASE,llm_path)
evaluate_file=os.path.join(directory, 'bird_evaluated_updated_system_empty.json')
# evaluation

os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {bird_corrected_file} {evaluate_file}")