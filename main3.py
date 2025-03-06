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
from utils.prompt import result_correction_instruction,result_correction_inputs,result_correction_instruction_skeleton,result_correction_inputs_skeleton
from utils.prompt import result_correction_instruction_schema,result_correction_inputs_schema
from utils.prompt import result_correction_instruction_simple,result_correction_inputs_simple
from utils.prompt import system_correction_instruction,system_correction_inputs,ablation_system_correction_instruction,ablation_system_correction_inputs
from utils.prompt import empty_correction_instruction,empty_correction_inputs,empty_correction_instruction_simple,empty_correction_inputs_simple
from utils.get_response import get_deepseek_response,get_codes_response,get_llm_response,get_gpt_response,get_baidu_response
from utils.process_llm_output_sql import format_sql_to_single_line
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.correct_value import find_similar_values_in_all_tables

import time
# deepseek
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

def correct(result_file,skeleton_schema_file,corrected_file,database_path):
    # get_skeketon_schema(result_file,skeleton_schema_file,database_path)
    data = read_json_file(skeleton_schema_file) 
    # 打开文件以追加模式写入
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write("[")  # 写入 JSON 数组的起始符号
        
        for i, item in enumerate(data):
            question = item.get('question','')
            # sql2_skeleton = item.get('sql2_skeleton','')
            sql1_schema = item.get('sql1_schema','')
            new_err_type = item['new_err_type'] 
            sql_pred=item.get('err_pred','')
            schema=item.get('full_schema','')
            
            if new_err_type=='result':
                # result_inputs = result_correction_inputs.format(question=question,schema_new=sql1_schema,skeleton_new=sql2_skeleton)

                # print('instruction:',result_correction_instruction)
                # print('inputs:',result_inputs)
                # while True:
                #     try:
                #         sql = get_gpt_response(result_correction_instruction, result_inputs)
                #         sql = format_sql_to_single_line(sql)
                #         item['sql_new'] = sql
                #         print('sql:', sql)
                #         break  # 成功获取 SQL，跳出循环
                #     except Exception as e:
                #         print(f"获取 SQL 失败，错误信息: {e}，等待 60 秒后重试...")
                #         time.sleep(60)

                # # 我的方法
                # # 存在schema+skeleton错误
                # if item['err_type1'] != "correct" and item['err_type2'] != "correct":
                #     result_inputs = result_correction_inputs.format(err_pred=sql_pred,question=question,schema_full=schema)

                #     print('instruction:',result_correction_instruction)
                #     print('inputs:',result_inputs)
                #     while True:
                #         try:
                #             sql = get_baidu_response(result_correction_instruction, result_inputs)
                #             sql = format_sql_to_single_line(sql)
                #             item['sql_new'] = sql
                #             print('sql:', sql)
                #             break  # 成功获取 SQL，跳出循环
                #         except Exception as e:
                #             print(f"获取 SQL 失败，错误信息: {e}，等待 60 秒后重试...")
                #             time.sleep(60)
                # # 存在skeleton错误
                # elif item['err_type1'] == "correct" and item['err_type2'] != "correct":
                #     result_inputs = result_correction_inputs_skeleton.format(err_pred=sql_pred,question=question,schema_new=sql1_schema)

                #     print('instruction:',result_correction_instruction_skeleton)
                #     print('inputs:',result_inputs)
                #     while True:
                #         try:
                #             sql = get_baidu_response(result_correction_instruction_skeleton, result_inputs)
                #             sql = format_sql_to_single_line(sql)
                #             item['sql_new'] = sql
                #             print('sql:', sql)
                #             break  # 成功获取 SQL，跳出循环
                #         except Exception as e:
                #             print(f"获取 SQL 失败，错误信息: {e}，等待 60 秒后重试...")
                #             time.sleep(60)
                # # 存在schema错误
                # else:
                    
                #     result_inputs = result_correction_inputs_schema.format(err_pred=sql_pred,question=question,schema_full=schema)
                #     print('instruction:',result_correction_instruction_schema)
                #     print('inputs:',result_inputs)
                #     while True:
                #         try:
                #             sql = get_baidu_response(result_correction_instruction, result_inputs)
                #             sql = format_sql_to_single_line(sql)
                #             item['sql_new'] = sql
                #             print('sql:', sql)
                #             break  # 成功获取 SQL，跳出循环
                #         except Exception as e:
                #             print(f"获取 SQL 失败，错误信息: {e}，等待 60 秒后重试...")
                #             time.sleep(60)




                result_inputs = result_correction_inputs_simple.format(question=question,schema_full=schema,err_pred=sql_pred)
                print('instruction:',result_correction_instruction_simple)
                print('inputs:',result_inputs)
                while True:
                    try:
                        sql = get_baidu_response(result_correction_instruction_simple, result_inputs)
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

                print("err_pred:",err_pred)
                print(db_id)

                vvalues=''
                values = extract_values(err_pred)
                # values: ['directed_by = Ben Jones']
                extracted_conditions = extract_column_and_value(values)  
                print(extracted_conditions)  
                # 检查每个value
                for column, value in extracted_conditions:  
                    if value=='':
                        continue  
                    if column is not None:  
                        print(value)
                        similar_values = find_similar_values_in_all_tables(db_path, value, case_sensitive=False)
                        for table, col, val in similar_values:
                          vvalues += f"[`{col}` = '{val}']; "
                print("vvalues:",vvalues)    
                empty_inputs = empty_correction_inputs.format(err_pred=err_pred,question=question,values=vvalues)
                # empty_inputs = empty_correction_inputs_simple.format(err_pred=err_pred,question=question)
                while True:
                    try:
                        # get_gpt_response, get_deepseek_response
                        sql = get_baidu_response(empty_correction_instruction, empty_inputs)
                        sql = format_sql_to_single_line(sql)
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
                
                # err_desc = item.get('err_desc','')
                # tips = item.get('tips','')
                # system_inputs = ablation_system_correction_inputs.format(question=question,schema_new=sql_schema,err_pred=err_pred,err_desc=err_desc,tips=tips)
                
                err_desc = get_system_error_desc(database_path, db_id, err_pred)
                system_inputs = system_correction_inputs.format(question=question,schema_new=sql_schema,err_pred=err_pred,err_desc=err_desc)
                print(system_inputs)
                while True:
                    try:
                        sql = get_baidu_response(system_correction_instruction, system_inputs)
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


def check(file,output):
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
        if item['new_err_type'] == 'system' or item['new_err_type'] == 'empty':
            pred_label = 0
            pred_err_count+=1
            if err_type!='correct':
                true_err_count+=1
        elif item['new_err_type'] != 'system' and item['new_err_type'] != 'empty' and (item['err_type1'] != "correct" or item['err_type2']) != "correct":
            pred_label=0
            pred_err_count+=1
            item['new_err_type'] = "result"
            if err_type!='correct':
                true_err_count+=1
        else:
            pred_label=1
            item['new_err_type'] = "correct"
                    
        y_true.append(true_label)
        y_pred.append(pred_label)

        
    save_json_file(output,data)
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


BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
directory='/root/Schema-Value/DIN-SQL/result/new/'

# # pipeline=None
# # # 1: gpt
# # # 2: llm
# # # 3: deepseek
bird_result = '/root/Schema-Value/DIN-SQL/result/predict_dev_deepseek_updated.json'
# 会验证empty错误
# process_bird_data(bird_path,bird_output,BIRD_DATABASE)
bird_sql= os.path.join(directory, 'bird_dev_sql.json')

# # # compute(bird_result)
# # # 重构new_err_type
# output_file = '/root/Schema-Value/data_new/xiaorong/bird_dev_result2.json'
# check(bird_result,output_file)






# # # # 处理反引号
bird_process=os.path.join(directory, 'bird_dev_result2.json')
# # # replace_special_characters_in_sql(bird_result,bird_process)

# # bird_skeleton_schema_file=os.path.join(directory, 'bird_dev_result_skeleton_schema.json')
# # # # # /root/Schema-Value/data/bird/dataset_new_new_new/deepseek_new_new_new/bird_corrected_updated2.json
# # # # # bird_skeleton_schema_file = os.path.join(directory, 'bird_corrected_updated.json')
# # bird_corrected_file=os.path.join(directory, 'bird_corrected_updated_system_empty.json')

# # input_path = '/root/Schema-Value/data_new/system/tips.json'
# # output_path = '/root/Schema-Value/data_new/system/corrected2.json'

input_path = '/root/Schema-Value/RSL-SQL/ours/bird_dev_resultt.json'
output_path = '//root/Schema-Value/RSL-SQL/ours/bird_dev_correct.json'
correct(bird_process,input_path,output_path,BIRD_DATABASE)

# # evaluate_file=os.path.join(directory, 'bird_evaluated_system_empty.json')
# # # # evaluation

# # os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {bird_corrected_file} {evaluate_file}")

