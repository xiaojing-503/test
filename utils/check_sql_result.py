import sqlite3
import os
import argparse
import multiprocessing
from utils.read_json_file import read_json_file
from utils.save_json_file import save_json_file
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report


def execute_sql(database_name, sql):
    """
    在子进程中执行 SQL 查询并返回结果。
    
    参数:
    database_name (str): SQLite 数据库路径。
    sql (str): SQL 查询语句。
    
    返回:
    list: 查询结果。
    """
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        return f"SQLite 错误: {e}"


def compare_sql_results(database_path, db_id, sql1, sql2, timeout=5):
    """
    比较两个 SQL 查询在 SQLite 数据库中的结果是否一致。
    
    参数:
    database_path (str): SQLite 数据库文件路径。
    db_id (str): 数据库标识符。
    sql1 (str): 第一个 SQL 查询语句。
    sql2 (str): 第二个 SQL 查询语句。
    timeout (int): 单个 SQL 查询的最大超时时间（秒）。
    
    返回:
    str: "correct" 如果两个查询结果一致，"result" 如果结果不一致，"timeout" 如果查询超时。
    """
    database_name = os.path.join(database_path, db_id, f"{db_id}.sqlite")
    print(f"连接数据库: {database_name}")

    # 创建多进程池
    with multiprocessing.Pool(processes=1) as pool:
        try:
            # 异步执行 SQL1
            result1_async = pool.apply_async(execute_sql, (database_name, sql1))
            result1 = result1_async.get(timeout=timeout)

            # 异步执行 SQL2
            result2_async = pool.apply_async(execute_sql, (database_name, sql2))
            result2 = result2_async.get(timeout=timeout)

            print(f"结果1: {result1}, 结果2: {result2}")

            # 比较结果
            if isinstance(result1, str) or isinstance(result2, str):
                # 如果返回的是错误信息
                return "system"
            return "correct" if result1 == result2 else "result"

        except multiprocessing.TimeoutError:
            print("查询超时")
            pool.terminate()
            return "timeout"

        except Exception as e:
            print(f"未知错误: {e}")
            return "timeout"


import os

def check_system_error(database_path, db_id, sql, timeout=5):
    """
    执行单个 SQL 查询，并检查查询结果是否为错误信息。
    
    参数:
    database_path (str): SQLite 数据库文件路径。
    db_id (str): 数据库标识符。
    sql (str): SQL 查询语句。
    timeout (int): 单个 SQL 查询的最大超时时间（秒）。
    
    返回:
    str: "system" 如果查询返回错误信息，否则返回 ""。
    """
    database_name = os.path.join(database_path, db_id, f"{db_id}.sqlite")
    print(f"连接数据库: {database_name}")

    try:
        # 执行 SQL 查询
        result = execute_sql(database_name, sql)

        print(f"查询结果: {result}")

        # 检查是否为错误信息
        if isinstance(result, str):
            # 如果返回的是错误信息
            return "system"
        return ""  # 正常查询结果，返回空字符串

    except Exception as e:
        print(f"查询错误: {e}")
        return "timeout"
import re
   
def get_system_error_desc(database_path, db_id, sql, timeout=5):
    """
    执行单个 SQL 查询，并检查查询结果是否为错误信息。
    
    参数:
    database_path (str): SQLite 数据库文件路径。
    db_id (str): 数据库标识符。
    sql (str): SQL 查询语句。
    timeout (int): 单个 SQL 查询的最大超时时间（秒）。
    
    返回:
    str: "system" 如果查询返回错误信息，否则返回 ""。
    """
    database_name = os.path.join(database_path, db_id, f"{db_id}.sqlite")
    print(f"连接数据库: {database_name}")

    try:
        # 执行 SQL 查询
        result = execute_sql(database_name, sql)
        

        # 检查是否为错误信息
        if isinstance(result, str):
            # 如果返回的是错误信息
            match = re.search(r'SQLite 错误: (.+)', result)
            if match:
                result = match.group(1)
            print(f"{result}")
            return result
        return ""  # 正常查询结果，返回空字符串

    except Exception as e:
        print(f"查询错误: {e}")
        return "timeout"


def check_sql(sql_file, save_file, bird_database, new_sql, timeout=5):
    data = read_json_file(sql_file)

    y_true = []
    y_pred = []
    true_err_count=0
    pred_err_count=0
    for item in data:
        sql1 = item['pred_sql']
        sql2 = item[new_sql]
        db_id = item['db_id']
        err_type = item['err_type']

        # 比较 SQL 结果
        comparison_result = compare_sql_results(bird_database, db_id, sql1, sql2, timeout)

        # 根据比较结果更新 new_err_type
        item['new_err_type'] = comparison_result
  

        # 根据 err_type 确定 true label
        true_label = 1 if err_type == "correct" else 0
        # 根据 new_err_type 确定 predicted label
        pred_label = 1 if item['new_err_type'] == "correct" else 0

        # 仅在不是超时的情况下记录
        # if item['new_err_type'] != "timeout":
        y_true.append(true_label)
        y_pred.append(pred_label)

        if item['new_err_type']!='correct':
            pred_err_count+=1
            if err_type!='correct':
                true_err_count+=1

    
    print("预测为错误的：",pred_err_count)
    print("实际为错误的：",true_err_count)
    print("precision:", true_err_count*1.0 / pred_err_count) 

    save_json_file(save_file, data)

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

def compute_report(sql_file,new_err_key):
    data = read_json_file(sql_file)
    y_true=[]
    y_pred=[]
    pred_err_count=0
    true_err_count=0
    for item in data:
        err_type=item['err_type']
        # 根据 err_type 确定 true label
        true_label = 1 if err_type == "correct" else 0
        # 根据 new_err_type 确定 predicted label
        pred_label = 1 if item[new_err_key] == "correct" else 0

        y_true.append(true_label)
        y_pred.append(pred_label)

        if item[new_err_key]!='correct':
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check SQL results and classify errors.")
    parser.add_argument('--sql_file', required=True, type=str, help='Path to the input JSON file containing SQL data')
    parser.add_argument('--save_file', required=True, type=str, help='Path to the output JSON file to save results')
    parser.add_argument('--bird_database', required=True, type=str, help='Path to the SQLite databases')
    parser.add_argument('--new_sql_name', required=True, type=str, help='Key for the new SQL in the JSON data')
    parser.add_argument('--timeout', type=int, default=5, help='Maximum time (seconds) allowed for each SQL query')

    args = parser.parse_args()

    check_sql(
        sql_file=args.sql_file,
        save_file=args.save_file,
        bird_database=args.bird_database,
        new_sql=args.new_sql_name,
        timeout=args.timeout
    )




# # # # 示例用法
# BIRD_DATABASE = "/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases"
# # db_id = 'california_schools'
# # sql1 = "SELECT schools.zip FROM schools INNER JOIN frpm ON schools.cdscode = frpm.cdscode WHERE frpm.'county name' = 'Fresno' AND frpm.'charter school (y/n)' = 1"
# # sql2 = "SELECT schools.zip FROM schools INNER JOIN frpm ON schools.cdscode = frpm.cdscode WHERE frpm.[Charter School (Y/N)] = 1 AND frpm.[county name] = 'Fresno County Office of Education';"
# # is_equal = compare_sql_results(BIRD_DATABASE, db_id, sql1, sql2)
# # print("结果是否一致:", is_equal)

# folder_path = "Filtered data has been saved to /root/Schema-Value/data/bird/dataset_new/OURS-GPT/round2/filtered_results.json"
# sql_file = os.path.join(folder_path, "merged_sql1.json") 
# out_file = os.path.join(folder_path, "result_sql11.json") 
# check_sql(sql_file,out_file,BIRD_DATABASE,"sql1")
