#!/bin/bash

# # 设置路径和文件变量（声明为只读变量，避免意外修改）
readonly BASE_DIR="/root/Schema-Value/data/spider/dataset_new_new"  
readonly LOGS="$BASE_DIR/logs"  


# # 不加入system和empty
# python utils/get_check_result.py \
#     --file1_path "${BASE_DIR}/merge1_gpt_result_deepseek_foreign.json" \
#     --file2_path "${BASE_DIR}/merge2_deepseek_result_deepseek_foreign.json" \
#     --enveroment 1 \
#     --dataset "bird" > "$LOGS/check_all.txt" 2>&1


# # 加入system和empty
# python utils/get_check_result.py \
#     --file1_path "${BASE_DIR}/merge1_gpt_result_deepseek_foreign.json" \
#     --file2_path "${BASE_DIR}/merge2_deepseek_result_deepseek_foreign.json" \
#     --enveroment 2 \
#     --dataset "bird" > "$LOGS/check_all_enveroment.txt" 2>&1



# # 不加入system和empty sql1
# python utils/get_check_result.py \
#     --file1_path "${BASE_DIR}/merge2_deepseek_result_deepseek_foreign.json" \
#     --file2_path "${BASE_DIR}/merge2_deepseek_result_deepseek_foreign.json" \
#     --enveroment 2 \
#     --dataset "bird" > "$LOGS/check_sql2.txt" 2>&1


# 不加入system和empty
python utils/get_check_result.py \
    --file1_path "/root/Schema-Value/data/spider/dataset_new_new/deepseek/sql1_merge.json" \
    --file2_path "/root/Schema-Value/data/spider/dataset_new_new/deepseek/sql1_merge.json" \
    --enveroment 2 \
    --dataset "spider" > "$LOGS/check_sql1_all.txt" 2>&1


# # 加入system和empty
# python utils/get_check_result.py \
#     --file1_path "/root/Schema-Value/data/spider/dataset_new_new/deepseek/sql2_result.json" \
#     --file2_path "/root/Schema-Value/data/spider/dataset_new_new/deepseek/sql1_merge.json" \
#     --enveroment 2 \
#     --dataset "spider" > "$LOGS/check_all_enveroment.txt" 2>&1