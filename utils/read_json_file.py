import json  

def read_json_file(file_path):  
    """  
    读取并解析指定路径的JSON文件。  

    参数:  
    file_path: str - JSON文件的路径  

    返回:  
    dict - 解析后的JSON内容  
    """  
    try:  
        with open(file_path, 'r', encoding='utf-8') as file:  
            data = json.load(file)  
        return data  
    except FileNotFoundError:  
        print(f"Error: The file {file_path} was not found.")  
    except json.JSONDecodeError:  
        print(f"Error: The file {file_path} is not a valid JSON file.")  
    except Exception as e:  
        print(f"An unexpected error occurred: {e}")  

