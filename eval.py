import os

output_path = '/root/Schema-Value/RSL-SQL/ours/bird_dev_correct.json'
evaluate_file = '/root/Schema-Value/RSL-SQL/ours/bird_dev_correct_eval.json'


os.system(f"sh /root/Schema-Value/code/process/run_evaluation.sh {output_path} {evaluate_file}")