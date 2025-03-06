db_root_path='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
data_mode='dev'

num_cpus=16
meta_time_out=30.0
mode_gt='gt'
mode_predict='gpt'

# save_path='/root/Schema-Value/data/bird/dataset_new_new/result.json'

echo '''starting to compare with knowledge for ex'''
python3 -u /root/Schema-Value/code/process/evaluation.py --db_root_path ${db_root_path} --sql_path $1  \
    --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
    --meta_time_out ${meta_time_out} --save_path $2
