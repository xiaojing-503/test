def format_sql_to_single_line(sql):  
    # 去掉反引号并按行分割，然后将每行的内容去掉前后的空格并按单空格拼接  
    sql = sql.replace('```sql', '').strip() 
    sql = sql.replace('```\nsql', '').strip() 
    sql = sql.replace('```', '').strip()  
    sql = sql.replace('-- ', '').strip() 
     
    return ' '.join(line.strip() for line in sql.splitlines())  


# # 示例 SQL
# sql = """
# ```
# sql
# SELECT schools.phone 
# FROM satscores 
# INNER JOIN schools ON satscores.cds = schools.cdscode 
# ORDER BY CAST(satscores.numge1500 AS FLOAT) / satscores.numtsttakr DESC 
# LIMIT 3;
# ```
# """

# print(format_sql_to_single_line(sql))