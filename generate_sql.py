import argparse
from utils.get_response import get_gpt_response,get_llm_response,get_deepseek_response,get_aliyun_deepseek,get_baidu_response
from utils.prompt import question_schema_skeleton_instruction, question_schema_skeleton_inputs, question_schema_new_instruction, question_schema_new_inputs
from utils.read_json_file import read_json_file
from utils.save_json_file import save_json_file
from utils.process_llm_output_sql import format_sql_to_single_line
import json
import transformers,torch
import time


def question_schema_full_skeletion_sql(item,llm_mode,pipeline=None):
    question = item['question']
    full_schema = item['full_schema']
    skeleton = item['skeleton']
    inputs = question_schema_skeleton_inputs.format(
        question=question,
        schema_full=full_schema,
        skeleton=skeleton
    )
    print(inputs)
    if llm_mode ==1 :
        while True:
            try:
                sql = get_gpt_response(question_schema_skeleton_instruction, inputs)
                break  # 成功获取 SQL，跳出循环
            except Exception as e:
                print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                time.sleep(3)
        
        
    elif llm_mode ==2 :
        sql=get_llm_response(question_schema_skeleton_instruction,inputs,pipeline)
    elif llm_mode ==3:
        while True:
            try:
                sql = get_baidu_response(question_schema_skeleton_instruction, inputs)
                break  # 成功获取 SQL，跳出循环
            except Exception as e:
                print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                time.sleep(3)
        
    sql = format_sql_to_single_line(sql)
    print(sql)
    print("\n")
    return sql

def generate_sql1(input_file, output_file,llm_mode,pipeline=None):
    data = read_json_file(input_file)
    # 打开文件以追加模式写入
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("[")  # 写入 JSON 数组的起始符号
        
        for i, item in enumerate(data):
            sql = question_schema_full_skeletion_sql(item,llm_mode,pipeline)
            item['sql1'] = sql
            
            # 将当前处理的 item 追加写入文件
            json.dump(item, f, ensure_ascii=False, indent=2)
            
            # 如果不是最后一条，添加逗号
            if i < len(data) - 1:
                f.write(",\n")

        f.write("]")  # 写入 JSON 数组的结束符号
    
    print(f"所有数据已保存到文件：{output_file}")

def question_schema_new_sql(item,llm_mode,pipeline=None):
    question = item['question']
    new_schema = item['new_schema']
    inputs = question_schema_new_inputs.format(
        question=question,
        schema_new=new_schema
    )
    print(inputs)
    if llm_mode ==1 :
        while True:
            try:
                sql = get_gpt_response(question_schema_new_instruction, inputs)
                break  # 成功获取 SQL，跳出循环
            except Exception as e:
                print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                time.sleep(3)
        
    elif llm_mode ==2 :
        sql=get_llm_response(question_schema_new_instruction,inputs,pipeline)
    elif llm_mode ==3:
        while True:
            try:
                sql = get_baidu_response(question_schema_new_instruction, inputs)
                break  # 成功获取 SQL，跳出循环
            except Exception as e:
                print(f"获取 SQL 失败，错误信息: {e}，等待 3 秒后重试...")
                time.sleep(3)
        
    sql = format_sql_to_single_line(sql)
    print(sql)
    print("\n")
    return sql

def generate_sql2(input_file, output_file,llm_mode,pipeline=None):
    data = read_json_file(input_file)
    
    # 打开文件以追加模式写入
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("[")  # 写入 JSON 数组的起始符号
        
        for i, item in enumerate(data):
            sql = question_schema_new_sql(item,llm_mode,pipeline)
            item['sql2'] = sql
            
            # 将当前处理的 item 追加写入文件
            json.dump(item, f, ensure_ascii=False, indent=2)
            
            # 如果不是最后一条，添加逗号
            if i < len(data) - 1:
                f.write(",\n")

        f.write("]")  # 写入 JSON 数组的结束符号
    
    print(f"所有数据已保存到文件：{output_file}")

if __name__ == "__main__":
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Generate SQL queries from JSON files.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("--output_file", type=str, required=True, help="Path to the output JSON file.")
    parser.add_argument("--sql_mode", type=int, required=True, choices=[1, 2], help="Choose the mode: 1 for generate_sql1, 2 for generate_sql2.")
    parser.add_argument("--llm_mode", type=int, required=True, choices=[1, 2, 3], help="Choose the mode: 1 for gpt, 2 for llm.")
    parser.add_argument("--model_id", type=str, required=True, help="Choose the mode: 1 for gpt, 2 for llm.")
    parser.add_argument("--cuda", type=str, required=True, help="Choose the mode: 1 for gpt, 2 for llm.")


    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file

    if args.llm_mode == 2:
        pipeline = transformers.pipeline(
            "text-generation",
            model=args.model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device=args.cuda,
        )
    else:
        pipeline = None

    if args.sql_mode == 1:
        generate_sql1(input_file, output_file,args.llm_mode,pipeline)
    elif args.sql_mode == 2:
        generate_sql2(input_file, output_file,args.llm_mode,pipeline)
