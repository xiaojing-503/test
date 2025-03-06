import json
import os
import subprocess

# 定义文件路径
file1_path = '/root/Schema-Value/data/bird/dataset_new_new_new/deepseek/bird_dev_result.json'
file2_path = '/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/deepseek/bird_dev_result.json'
output_path = '/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/deepseek/merged_result.json'
evaluate_file = '/root/Schema-Value/data/bird/dataset_new_new_new_codes_version/deepseek/evaluated.json'

# 检查文件是否存在
if os.path.exists(file1_path) and os.path.exists(file2_path):
    # # 读取两个 JSON 文件
    # with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
    #     data1 = json.load(f1)
    #     data2 = json.load(f2)

    # # 存储合并后的结果
    # merged_data = []

    # # 遍历两个文件的数据
    # for entry1, entry2 in zip(data1, data2):
    #     # 检查两个条目的 "new_err_type" 字段
    #     if entry1.get('new_err_type') == 'correct' or entry2.get('new_err_type') == 'correct':
    #         # 如果任何一个是 "correct"，则选择将第一条数据存入新文件
    #         merged_data.append(entry1 if entry1.get('new_err_type') == 'correct' else entry2)
    #     else:
    #         # 如果都不是 "correct"，则选择存入第一条数据
    #         merged_data.append(entry1)

    # # 将合并后的数据写入新文件
    # with open(output_path, 'w') as output_file:
    #     json.dump(merged_data, output_file, indent=4)

    # print(f"合并结果已保存到 {output_path}")

    # 调用外部 shell 脚本
    # subprocess.run(["sh", "bird_evaluation/run_evaluation.sh", output_path])
    os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {output_path} {evaluate_file}")

else:
    print(f"One or both files do not exist.")
