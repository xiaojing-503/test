import json
# 其中difficulty和schema_sequence从/root/Schema-Value/data/bird/dataset/bird_dev.json获得，err_type ：如果res为1，为correct，如果res为0，且"error": null，则为result，否则为system


import json

def process_results(results_file, bird_file, output_file):
    # Load the results file
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Load the bird dataset file to get difficulty and schema_sequence
    with open(bird_file, 'r', encoding='utf-8') as f:
        bird_data = json.load(f)
    
    # Assuming the lengths of results and bird_data are the same, we zip them
    processed_results = []
    
    for result, bird_entry in zip(results, bird_data):
        # Extract necessary fields
        db_id = result['db_id']
        res = result['res']
        error = result['error']
        
        # Determine err_type
        if res == 1:
            err_type = "correct"
        elif res == 0 and error is None:
            err_type = "result"
        else:
            err_type = "system"
        
        # Get difficulty and schema_sequence from bird_entry
        difficulty = bird_entry.get('difficulty', 'moderate')  # Default to 'moderate' if not found
        schema_sequence = bird_entry.get('schema_sequence', '')  # Default to empty string if not found
        
        # Create the new formatted dictionary
        processed_result = {
            "db_id": db_id,
            "question": bird_entry['question'],  # Assuming we don't have a question field in the results file
            "evidence":  bird_entry['evidence'],  # Assuming we don't have evidence field in the results file
            "difficulty": difficulty,
            "schema_sequence": schema_sequence,
            "id": result['sql_idx'],  # Using sql_idx as id
            "err_gold": result['gold'],  # Assuming there's no "gold" error field provided
            "err_pred": result['pred'],  # The predicted SQL query
            "err_type": err_type,
            "new_err_type": ""  # Placeholder for future categorization if needed
        }
        
        # Add processed result to the list
        processed_results.append(processed_result)
    
    # Write the processed data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_results, f, ensure_ascii=False, indent=4)

# File paths (you can adjust the file paths as needed)
results_file = '/root/Schema-Value/codes/results/results2.json'
bird_file = '/root/Schema-Value/data/bird/dataset/bird_dev.json'
output_file = '/root/Schema-Value/data/bird/dataset_new_new_new_new/bird_dev.json'

# Process the results
process_results(results_file, bird_file, output_file)

