#!/bin/bash

# 设置路径和文件变量（声明为只读变量，避免意外修改）
# readonly BASE_DIR="/root/Schema-Value/data/bird/dataset_new_new/foreign/deepseek"  
# readonly LOGS="$BASE_DIR/logs"  
# readonly OUTPUT_PATH="$BASE_DIR/"  
# readonly MODEL_ID="/root/hdd/Llama-3-8B-Instruct"  
# readonly CUDA_ID="cuda:1"  
# readonly BIRD_DATABASE="/root/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/"  


# python generate_sql.py \
#     --input_file "/root/Schema-Value/data/bird/dataset_new_new/foreign_process.json" \
#     --output_file "${OUTPUT_PATH}foreign_sql1.json" \
#     --sql_mode 1 \
#     --llm_mode 3 \
#     --model_id "$MODEL_ID" \
#     --cuda "$CUDA_ID" > "$LOGS/foreign_sql1.txt" 2>&1


# python utils/check_sql_result.py \
#     --sql_file "${OUTPUT_PATH}foreign_sql1.json" \
#     --save_file "${OUTPUT_PATH}foreign_sql1_result.json" \
#     --bird_database "${BIRD_DATABASE}" \
#     --new_sql "sql1"\
#     --timeout 10 > "$LOGS/foreign_sql1_check.txt" 2>&1

# file='/root/Schema-Value/data/bird/datasets/sql1_unique.json'

# python utils/check_sql_result.py \
#     --sql_file "${file}" \
#     --save_file "${OUTPUT_PATH}sql1-result-gpt.json" \
#     --bird_database "${BIRD_DATABASE}" \
#     --new_sql "sql1"\
#     --timeout 10


readonly MODEL_ID="/root/hdd/Llama-3-8B-Instruct"
readonly CUDA_ID="cuda:0"
readonly LOGS="/root/Schema-Value/data/spider/dataset_new_new/logs"
readonly FILE_PATH="/root/Schema-Value/data/spider/dataset_new_new/"
readonly OUTPUT_PATH="/root/Schema-Value/data/spider/dataset_new_new/deepseek/"
readonly BIRD_DATABASE="/root/Text-to-SQL/dataset/spider/database/"


python generate_sql.py \
    --input_file "/root/Schema-Value/data/spider/dataset_new/foreign_processs.json" \
    --output_file "${OUTPUT_PATH}sql1_foreign.json" \
    --sql_mode 1 \
    --llm_mode 3 \
    --model_id "$MODEL_ID" \
    --cuda "$CUDA_ID" > "$LOGS/sql1_foreign_deepseek_spider.txt" 2>&1


python utils/check_sql_result.py \
    --sql_file "${OUTPUT_PATH}sql1_foreign.json" \
    --save_file "${OUTPUT_PATH}sql1_foreign_result.json" \
    --bird_database "${BIRD_DATABASE}" \
    --new_sql "sql1"\
    --timeout 10 > "$LOGS/sql1_foreign_check_deepseek_spider.txt" 2>&1
