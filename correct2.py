import os
from main import correct2,correct3
BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
directory='/root/Schema-Value/data/bird/dataset_new_new_new/deepseek'
directory_new='/root/Schema-Value/data/bird/dataset_new_new_new/llama'

llm_path = '/root/hdd/codes-7b'
# 处理反引号
bird_process=os.path.join(directory, 'bird_dev_result_process.json')

# 取sql0和sql1的交集
bird_skeleton_schema_file=os.path.join(directory_new, 'bird_dev_result_skeleton_schema.json')
bird_corrected_file=os.path.join(directory_new, 'bird_corrected.json')
# correct2(bird_process,bird_skeleton_schema_file,bird_corrected_file,BIRD_DATABASE,llm_path)
# correct3(bird_process,bird_skeleton_schema_file,bird_corrected_file,BIRD_DATABASE)

evaluate_file=os.path.join(directory_new, 'bird_evaluated.json')
# evaluation
os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {bird_corrected_file} {evaluate_file}")