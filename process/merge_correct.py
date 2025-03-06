import json  

def merge_json_data(file_path1, file_path2, output_file_path):  
    # 读取第一个JSON文件  
    with open(file_path1, 'r', encoding='utf-8') as f1:  
        data1 = json.load(f1)  
    
    # 读取第二个JSON文件  
    with open(file_path2, 'r', encoding='utf-8') as f2:  
        data2 = json.load(f2)  

    # 创建一个 question + evidence 到 err_gold 和 difficulty 的映射  
    question_to_info = {item['question'] + ' ' + item['evidence']: (item['err_gold'], item['difficulty']) for item in data2}  
    # print(question_to_info)

    # 更新第一个文件中的数据  
    for item in data1:  
        question = item.get('question')  
        if question in question_to_info:  
            item['err_gold'], item['difficulty'] = question_to_info[question]  
        print(item['err_gold'], item['difficulty'])
    
    # 将更新后的数据保存到新的JSON文件  
    with open(output_file_path, 'w', encoding='utf-8') as f_out:  
        json.dump(data1, f_out, ensure_ascii=False, indent=2)  

# 文件路径  
file1 = '/root/Schema-Value/data/bird/dataset_new_new/corrected.json'  
file2 = '/root/Schema-Value/data/bird/dataset/bird_dev.json'  
output_file = '/root/Schema-Value/data/bird/dataset_new_new/merged_with_err_gold.json'  

# 执行合并操作  
merge_json_data(file1, file2, output_file)