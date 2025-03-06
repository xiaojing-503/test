#!/bin/bash

# 设置路径和文件变量（声明为只读变量，避免意外修改）
readonly BASE_DIR="/root/Schema-Value/data/bird/llama"  
readonly LOGS="$BASE_DIR/logs"  
readonly OUTPUT_PATH="$BASE_DIR/"  
readonly MODEL_ID="/root/hdd/Llama-3-8B-Instruct"  
readonly CUDA_ID="cuda:1"  
readonly BIRD_DATABASE="/root/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/"  


python generate_sql.py \
    --input_file "/root/Schema-Value/data/bird/dataset_new_new/process.json" \
    --output_file "${OUTPUT_PATH}sql1.json" \
    --sql_mode 1 \
    --llm_mode 2 \
    --model_id "$MODEL_ID" \
    --cuda "$CUDA_ID" > "$LOGS/sql1.txt" 2>&1


python utils/check_sql_result.py \
    --sql_file "${OUTPUT_PATH}sql1.json" \
    --save_file "${OUTPUT_PATH}sql1_result.json" \
    --bird_database "${BIRD_DATABASE}" \
    --new_sql "sql1"\
    --timeout 10 > "$LOGS/sql1_check.txt" 2>&1


python generate_sql.py \
    --input_file "/root/Schema-Value/data/bird/dataset_new_new/process.json" \
    --output_file "${OUTPUT_PATH}sql2.json" \
    --sql_mode 2 \
    --llm_mode 2 \
    --model_id "$MODEL_ID" \
    --cuda "$CUDA_ID" > "$LOGS/sql2.txt" 2>&1


python utils/check_sql_result.py \
    --sql_file "${OUTPUT_PATH}sql2.json" \
    --save_file "${OUTPUT_PATH}sql2_result.json" \
    --bird_database "${BIRD_DATABASE}" \
    --new_sql "sql2"\
    --timeout 10 > "$LOGS/sql2_check.txt" 2>&1