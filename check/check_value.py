import sqlite3  
import os  
# from skeleton.sql_value import extract_values, extract_column_and_value

def check_value_in_any_table(column_name, value, db_id, db_path="/root/Text-to-SQL/dataset/spider/database"):  
    # 连接到SQLite数据库  
    database_path = os.path.join(db_path, f"{db_id}/{db_id}.sqlite")  
    conn = sqlite3.connect(database_path)  
    cursor = conn.cursor()  
    
    try:  
        # 查询数据库中的所有表名  
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
        tables = cursor.fetchall()  
        
        # 遍历每个表  
        # count=0
        for (table_name,) in tables:  
            # 检查该表中是否存在指定的列（列名大小写不敏感）  
            cursor.execute(f"PRAGMA table_info('{table_name}')")  
            columns = cursor.fetchall() 
            # print("table_name:",table_name) 
            # 使用小写比较，确保列名匹配时不区分大小写  
            # print(column[1].lower())
            if any(column[1].lower() == column_name.lower() for column in columns):  
                # 执行查询，这里对值的比较保持大小写敏感  
                # print("column_name")
                # print(column_name)
                # print(value)
                value = value.replace("''", "'")
                query = f"SELECT 1 FROM '{table_name}' WHERE \"{column_name}\"= ? LIMIT 1"  
                cursor.execute(query, (value,))
                # 如果存在，则返回结果  
                if cursor.fetchall(): 
                    # print("#####") 
                    print(f"The value '{value}' exists in column '{column_name}' in table '{table_name}'.") 
                    # 检查到了，这个表中的xx列有这个 
                    return 1  
            # print("\n")
        print(f"The value '{value}' does not exist in column '{column_name}' in any table.")    
        return 0  
    except Exception as e:  
        print(f"发生错误：{e}")
        return 0  

    finally:  
        # value="O''Gallagher"
        # value = value.replace("''", "'")
        # query = "SELECT * FROM member WHERE last_name = ?"
        # cursor.execute(query, (value,))
        # print(cursor.fetchall())
        # query = "SELECT 1 FROM 'member' WHERE \"last_name\"= ? LIMIT 1"  
        # value='O''Gallagher'
        # cursor.execute(query, (value,))
        # print(cursor.fetchall())
        cursor.close()  
        conn.close()  

# def check_empty(err_pred,db_id,bird_database):
#     # 检查是否是empty错误
#     values = extract_values(err_pred)
#     # values: ['directed_by = Ben Jones']
#     extracted_conditions = extract_column_and_value(values)  
#     print(extracted_conditions)  
    
#     # 默认假设没有满足条件的行  
#     res = 1  

#     # 检查每个条件  
#     for column, value in extracted_conditions:  
#         # 如果其中任意一个条件不成立，则设置为0
#         if value=='':
#             continue  
#         if column is not None:  
#             res = check_value_in_any_table(column, value, db_id,  db_path = bird_database)  
#             if res == 0:  
#                 break  
#     # print("check完毕！")
#     if res == 0:  
#         return "empty"
#     return ""         