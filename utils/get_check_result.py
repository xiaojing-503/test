import argparse  
import json  
from sklearn.metrics import classification_report  
import numpy as np


def join_error_types(file1_path, file2_path, enveroment, dataset):  
    # 读取JSON文件  
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:  
        data1 = json.load(file1)  
        data2 = json.load(file2)  

    # 假设两个文件的数据是一个列表，每个元素对应一个SQL记录  
    y_true = []  
    y_pred = []  
    true_err_count = 0  
    pred_err_count = 0  
    for item1, item2 in zip(data1, data2):  
        # 获取两个文件中的new_err_type  
        new_err_type1 = item1.get('new_err_type', '')  
        new_err_type2 = item2.get('new_err_type', '')  
        true_err_type = item1.get('err_type', '')  

        # 判断combine_err_type的值  
        if new_err_type1 != 'correct' and new_err_type2 != 'correct':  
            pred_err_count += 1  
            if true_err_type != 'correct':  
                true_err_count += 1  

        true_label = 0 if true_err_type != "correct" else 1  
        # 根据 new_err_type 确定 predicted label  
        pred_label = 0 if new_err_type1 != "correct" and new_err_type2 != "correct" else 1  

        # 仅在不是超时的情况下记录  
        y_true.append(true_label)  
        y_pred.append(pred_label)  

    # 不加入system和empty
    if enveroment == 1:
        pass
    # 加入system和empty
    elif enveroment == 2:
        if dataset=='bird':
            pred_labels = np.array([0]*109+[1]*7+[0]*6)
            true_labels = np.array([0]*109 + [1]*13)
            y_true += true_labels.tolist()
            y_pred += pred_labels.tolist()
            pred_err_count += 115
            true_err_count += 109
        elif dataset == 'spider':
            pred_labels = np.array([0]*103+[1]*42)
            true_labels = np.array([0]*103+[1]*42)
            y_true += true_labels.tolist()
            y_pred += pred_labels.tolist()
            pred_err_count += 103
            true_err_count += 103
    
        

    print("预测为错误的：", pred_err_count)  
    print("实际为错误的：", true_err_count)  
    print("precision:", true_err_count * 1.0 / pred_err_count if pred_err_count else 0)  

    if y_true and y_pred:  
        report = classification_report(y_true, y_pred, target_names=["incorrect", "correct"])  
        print("Classification Report:")  
        print(report)  
        report_dict = classification_report(y_true, y_pred, target_names=["incorrect", "correct"], output_dict=True)  

        # 格式化和打印报告  
        for label, metrics in report_dict.items():  
            if isinstance(metrics, dict):  # 表示这是类别级别的统计  
                print(f"{label}:")  
                for metric, value in metrics.items():  
                    print(f"  {metric}: {value:.3f}")  
            else:  # 针对"accuracy"这个单值指标  
                print(f"{label}: {metrics:.3f}")  


def union_error_types(file1_path, file2_path, enveroment, dataset):  
    # 读取JSON文件  
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:  
        data1 = json.load(file1)  
        data2 = json.load(file2)  

    # 假设两个文件的数据是一个列表，每个元素对应一个SQL记录  
    y_true = []  
    y_pred = []  
    true_err_count = 0  
    pred_err_count = 0  
    for item1, item2 in zip(data1, data2):  
        # 获取两个文件中的new_err_type  
        new_err_type1 = item1.get('new_err_type', '')  
        new_err_type2 = item2.get('new_err_type', '')  
        true_err_type = item1.get('err_type', '')  

        # 判断combine_err_type的值  
        if new_err_type1 != 'correct' or new_err_type2 != 'correct':  
            pred_err_count += 1  
            if true_err_type != 'correct':  
                true_err_count += 1  

        true_label = 0 if true_err_type != "correct" else 1  
        # 根据 new_err_type 确定 predicted label  
        pred_label = 0 if new_err_type1 != "correct" or new_err_type2 != "correct" else 1  

        # 仅在不是超时的情况下记录  
        y_true.append(true_label)  
        y_pred.append(pred_label)  

    # 不加入system和empty
    if enveroment == 1:
        pass
    # 加入system和empty
    elif enveroment == 2:
        if dataset=='bird':
            pred_labels = np.array([0]*109+[1]*7+[0]*6)
            true_labels = np.array([0]*109 + [1]*13)
            y_true += true_labels.tolist()
            y_pred += pred_labels.tolist()
            pred_err_count += 115
            true_err_count += 109
        elif dataset == 'spider':
            pred_labels = np.array([0]*103+[1]*42)
            true_labels = np.array([0]*103+[1]*42)
            y_true += true_labels.tolist()
            y_pred += pred_labels.tolist()
            pred_err_count += 103
            true_err_count += 103
    
        

    print("预测为错误的：", pred_err_count)  
    print("实际为错误的：", true_err_count)  
    print("precision:", true_err_count * 1.0 / pred_err_count if pred_err_count else 0)  

    if y_true and y_pred:  
        report = classification_report(y_true, y_pred, target_names=["incorrect", "correct"])  
        print("Classification Report:")  
        print(report)  
        report_dict = classification_report(y_true, y_pred, target_names=["incorrect", "correct"], output_dict=True)  

        # 格式化和打印报告  
        for label, metrics in report_dict.items():  
            if isinstance(metrics, dict):  # 表示这是类别级别的统计  
                print(f"{label}:")  
                for metric, value in metrics.items():  
                    print(f"  {metric}: {value:.3f}")  
            else:  # 针对"accuracy"这个单值指标  
                print(f"{label}: {metrics:.3f}")  


if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description="Check SQL results and classify errors.")  
    parser.add_argument('--file1_path', type=str, required=True, help='Path to the first JSON file.')  
    parser.add_argument('--file2_path', type=str, required=True, help='Path to the second JSON file.')  
    parser.add_argument('--enveroment', type=int, required=True, help='Path to the second JSON file.') 
    parser.add_argument('--dataset', type=str, required=True, help='Path to the second JSON file.')  
    args = parser.parse_args()  

    # 交集
    print("交集")
    join_error_types(args.file1_path, args.file2_path, args.enveroment, args.dataset)

    # 并集
    print("并集")
    union_error_types(args.file1_path, args.file2_path, args.enveroment, args.dataset)

