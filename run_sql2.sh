# !/bin/bash

# # 设置路径和文件变量（声明为只读变量，避免意外修改）
# readonly MODEL_ID="/root/hdd/Llama-3-8B-Instruct"
# readonly CUDA_ID="cuda:1"
# readonly LOGS="/root/Schema-Value/data/bird/dataset_new_new/deepseek/logs"
# # readonly FILE_PATH="/root/Schema-Value/data/bird/datasets/"
# readonly FILE_PATH="/root/Schema-Value/data/bird/dataset_new_new/"
# readonly OUTPUT_PATH="/root/Schema-Value/data/bird/dataset_new_new/deepseek/"
# readonly BIRD_DATABASE="/root/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/"

# # 执行 Python 脚本
# python generate_sql.py \
#     --input_file "" \
#     --output_file "${OUTPUT_PATH}sql2.json" \
#     --sql_mode 2 \
#     --llm_mode 3 \
#     --model_id "$MODEL_ID" \
#     --cuda "$CUDA_ID" > "$LOGS/sql2_deepseek.txt" 2>&1

# python utils/check_sql_result.py \
#     --sql_file "${OUTPUT_PATH}sql2.json" \
#     --save_file "${OUTPUT_PATH}sql2_result.json" \
#     --bird_database "${BIRD_DATABASE}" \
#     --new_sql_name "sql2"\
#     --timeout 10 > "$LOGS/sql2_deepseek_check.txt" 2>&1


# file='/root/Schema-Value/data/bird/datasets/sql2.json'

# python utils/check_sql_result.py \
#     --sql_file "${file}" \
#     --save_file "${OUTPUT_PATH}sql2-result-gpt.json" \
#     --bird_database "${BIRD_DATABASE}" \
#     --new_sql "sql2"\
#     --timeout 10

readonly MODEL_ID="/root/hdd/Llama-3-8B-Instruct"
readonly CUDA_ID="cuda:1"
readonly LOGS="/root/Schema-Value/data/spider/dataset_new_new/logs"
readonly FILE_PATH="/root/Schema-Value/data/spider/dataset_new_new/"
readonly OUTPUT_PATH="/root/Schema-Value/data/spider/dataset_new_new/deepseek/"
readonly BIRD_DATABASE="/root/Text-to-SQL/dataset/spider/database/"


python generate_sql.py \
    --input_file "/root/Schema-Value/data/spider/dev_889_new_schema.json" \
    --output_file "${OUTPUT_PATH}sql2.json" \
    --sql_mode 2 \
    --llm_mode 3 \
    --model_id "$MODEL_ID" \
    --cuda "$CUDA_ID" > "$LOGS/sq12_deepseek_spider.txt" 2>&1


python utils/check_sql_result.py \
    --sql_file "${OUTPUT_PATH}sql2.json" \
    --save_file "${OUTPUT_PATH}sql2_result.json" \
    --bird_database "${BIRD_DATABASE}" \
    --new_sql "sql2"\
    --timeout 10 > "$LOGS/sq12_deepseek_check_spider.txt" 2>&1


    
# # python utils/check_sql_result.py \
# #     --sql_file "/root/Schema-Value/data/bird/dataset_new/DIN-SQL/merged_data_gpt.json" \
# #     --save_file "/root/Schema-Value/data/bird/dataset_new/DIN-SQL/merged_data_gpt_result.json" \
# #     --bird_database "${BIRD_DATABASE}" \
# #     --new_sql "final_query"\
# #     --timeout 10 > /root/Schema-Value/data/bird/dataset_new/DIN-SQL/merged_data_gpt_check.txt 2>&1