import re

# 没有单引号时，字段名是一个单词（不包含空格）。
# 有单引号时，字段名包括单引号内的所有内容（可以包含空格）。
# def extract_values(sql_query):  
#     # 修改正则表达式模式以包括 != 运算符  
#     # pattern = r'\b(\w+)\s*(=|!=|)\s*[\'\"](.*?)[\'\"]'  
#     pattern = r"(?:\'([\w\s\(\)/]+)\'|(\w+))\s*(=|!=)?\s*[\'\"](.*?)[\'\"]"
#     matches = re.findall(pattern, sql_query)  
#     # 调整输出格式以包括运算符  
#     return ['{} {} {}'.format(match[0], match[1], match[2]) for match in matches]   

# def extract_values(pred_sql):
#     pattern = r"(?:\'([\w\s\(\)/]+)\'|(\w+))\s*(=|!=)?\s*[\'\"](.*?)[\'\"]"
#     matches = re.findall(pattern, pred_sql)

#     # 格式化输出
#     results = []
#     for match in matches:
#         field_name = match[0] if match[0] else match[1]  # 优先取单引号内的字段名
#         operator = match[2]
#         value = match[3]
#         results.append(f"{field_name} {operator} {value}")

#     return results
def extract_column_and_value(conditions):  
    # 用于存储结果的列表  
    extracted_conditions = []  
    
    # 如果条件列表为空，返回空列表  
    if not conditions:  
        return extracted_conditions  
    
    # 对每个条件进行解析  
    for condition in conditions:  
        # 检查是否包含 `=` 或 `!=` 运算符  
        if '=' in condition:  
            # 检测不等于符号  
            if '!=' in condition:  
                column, value = condition.split('!=', 1)  
            else:  
                column, value = condition.split('=', 1)  

            # 去掉两边不必要的空格  
            column = column.strip()  
            value = value.strip()  
            
            # 将结果添加到列表中  
            extracted_conditions.append((column, value))  
    
    return extracted_conditions  

def extract_values(pred_sql):
    # pattern = r"(?:\'([\w\s\(\)/]+)\'|(\w+))\s*(=|!=)\s*[\'\"](.*?)[\'\"]"
    pattern = r"(\w+)\s*(=|!=)\s*(?:\'([^\']*(?:\'\'[^\']*)*)\'|\"([^\"]*)\")"
    matches = re.findall(pattern, pred_sql)

    # 格式化输出
    results = []
    for match in matches:
        field_name = match[0]
        operator = match[1]
        value = match[2] if match[2] else match[3]  # 优先选择单引号内的值
        results.append(f"{field_name} {operator} {value}")

    return results
# # pred_sql="SELECT DISTINCT schools.school FROM schools INNER JOIN satscores ON schools.cdscode = satscores.cds WHERE satscores.numge1500 > 500 AND magnet = 1"
# # pred_sql="SELECT schools.phone FROM schools INNER JOIN frpm ON schools.cdscode = frpm.cdscode WHERE frpm.'charter school (y/n)' = 1 AND schools.opendate > '2000-01-01'"
# # schools.fundingtype = ' Directly funded' 可以处理
# # schools.fundingtype = 1 无法处理，也不需要处理
# # pred_sql="SELECT count(DISTINCT schools.school) FROM schools INNER JOIN satscores ON schools.cdscode = satscores.cds WHERE satscores.avgscrmath > 560 AND schools.fundingtype = 1"
# # pred_sql="SELECT schools.zip FROM schools INNER JOIN frpm ON schools.cdscode = frpm.cdscode WHERE frpm.'county name' = 'Fresno' AND frpm.'charter school (y/n)' = 1"
# # pred_sql="SELECT max(frpm.'free meal count (k-12)') / max(frpm.'enrollment (k-12)') FROM frpm INNER JOIN schools ON frpm.cdscode = schools.cdscode WHERE schools.county = 'Alameda'"
# pred_sql="SELECT count(cdscode) FROM frpm WHERE 'county name' = 'Amador' AND 'low grade' = 9 AND 'high grade' = 12"
# values = extract_values(pred_sql) 

# print(values)