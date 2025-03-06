import sqlite3
import os

# 获取数据库中所有表的列名映射
def get_column_table_mapping(database_name):
    # 连接SQLite数据库
    connection = sqlite3.connect(database_name)
    
    column_to_table_mapping = {}

    try:
        cursor = connection.cursor()

        # 获取所有表的名字
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            # 获取当前表的列信息
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns = cursor.fetchall()

            # 将列名映射到表
            for col in columns:
                column_name = col[1].lower()  # 使用小写列名以便大小写不敏感
                if column_name not in column_to_table_mapping:
                    column_to_table_mapping[column_name] = []
                column_to_table_mapping[column_name].append(table_name)

    finally:
        connection.close()

    return column_to_table_mapping

# def map_columns_to_tables_and_values(sql_schema, extracted_values, column_to_table_mapping):
#     tables, columns, _ = sql_schema  # Unpack data returned by get_sql_schema
#     column_to_value = {}

#     # 先处理没有 extracted_values 的情况，直接映射列名到表
#     if len(extracted_values) == 0:
#         for col in columns:  # Case insensitive match
#             col = col.lower().strip()  # 转换为小写，保证不区分大小写
#             # 查找该列对应的表
#             if col in column_to_table_mapping:
#                 for table in column_to_table_mapping[col]:
#                     table_column_key = f'{table}:{col}'
#                     if table_column_key not in column_to_value:
#                         column_to_value[table_column_key] = []

#     else:
#         # 处理带有 extracted_values 的情况
#         for condition in extracted_values:
#             operator = None
#             # 处理等式条件
#             if ' = ' in condition:
#                 column, value = condition.split(' = ', 1)  # 只处理第一个 '=' 号
#                 operator = '='
#             elif ' != ' in condition:
#                 column, value = condition.split(' != ', 1)
#                 operator = '!='
#             else:
#                 # 如果既没有 '=' 也没有 '!=', 跳过这个条件
#                 continue

#             column = column.strip().lower()  # 忽略大小写
#             value = value.strip()

#             # 只映射在列名列表中的列
#             if column in [col.lower() for col in columns]:  # 忽略大小写匹配
#                 # 找到该列对应的表
#                 if column in column_to_table_mapping:
#                     for table in column_to_table_mapping[column]:
#                         table_column_key = f'{table}:{column}'
#                         if table_column_key not in column_to_value:
#                             column_to_value[table_column_key] = []

#                         # 将值映射到表和列中，考虑到操作符
#                         if operator == '=':
#                             column_to_value[table_column_key].append(f'({value})')
#                         elif operator == '!=':
#                             column_to_value[table_column_key].append(f'(!={value})')

#     # 如果值为空，则仅根据列名映射表，确保不会漏掉没有值的列
#     for col in columns:  # 如果 extracted_values 中没有提取到值，也需要检查列名
#         col = col.lower().strip()
#         if col in column_to_table_mapping:
#             for table in column_to_table_mapping[col]:
#                 table_column_key = f'{table}:{col}'
#                 if table_column_key not in column_to_value:
#                     column_to_value[table_column_key] = []

#     return column_to_value
def map_columns_to_tables_and_values(sql_schema, extracted_values, column_to_table_mapping):
    tables, columns, _ = sql_schema  # Unpack data returned by get_sql_schema
    # print("tables:",tables)
    column_to_value = {}

    # 如果列名和 extracted_values 都为空，返回所有的表并映射空列
    if len(columns) == 0 and len(extracted_values) == 0:
        for table in tables:  # 遍历所有表
            table_column_key = f'{table}:*'  # 使用 '*' 表示所有列
            column_to_value[table_column_key] = []  # 为每个表设置空的列映射
        return column_to_value

    # 先处理没有 extracted_values 的情况，直接映射列名到表
    if len(extracted_values) == 0:
        for col in columns:  # Case insensitive match
            col = col.lower().strip()  # 转换为小写，保证不区分大小写
            # 查找该列对应的表
            if col in column_to_table_mapping:
                for table in column_to_table_mapping[col]:
                    # print(table)
                    table_column_key = f'{table}:{col}'
                    if table_column_key not in column_to_value:
                        column_to_value[table_column_key] = []

    else:
        # 处理带有 extracted_values 的情况
        for condition in extracted_values:
            operator = None
            # 处理等式条件
            if ' = ' in condition:
                column, value = condition.split(' = ', 1)  # 只处理第一个 '=' 号
                operator = '='
            elif ' != ' in condition:
                column, value = condition.split(' != ', 1)
                operator = '!='
            else:
                # 如果既没有 '=' 也没有 '!=', 跳过这个条件
                continue

            column = column.strip().lower()  # 忽略大小写
            value = value.strip()

            # print("column:",column)
            # print("value:",value)
            # print("columns:",columns)
            # print("column_to_table_mapping:",column_to_table_mapping)
            # print("tables:",tables)

            # 只映射在列名列表中的列
            if column in [col.lower() for col in columns]:  # 忽略大小写匹配
                # 找到该列对应的表
                if column in column_to_table_mapping:
                    for table in column_to_table_mapping[column]:
                        if table.lower() in tables:
                            table_column_key = f'{table}:{column}'
                            if table_column_key not in column_to_value:
                                column_to_value[table_column_key] = []

                            # 将值映射到表和列中，考虑到操作符
                            if operator == '=':
                                column_to_value[table_column_key].append(f'({value})')
                            elif operator == '!=':
                                column_to_value[table_column_key].append(f'(!={value})')

    # 如果值为空，则仅根据列名映射表，确保不会漏掉没有值的列
    for col in columns:  # 如果 extracted_values 中没有提取到值，也需要检查列名
        col = col.lower().strip()
        if col in column_to_table_mapping:
            for table in column_to_table_mapping[col]:
                if table.lower() in tables:
                    table_column_key = f'{table}:{col}'
                    if table_column_key not in column_to_value:
                        column_to_value[table_column_key] = []

    return column_to_value

# 使用示例
def get_table_column_value(database_path, db_id, sql_schema, extracted_values):
    database_name = os.path.join(database_path, db_id + f"/{db_id}.sqlite")  
    table_column_mapping = get_column_table_mapping(database_name)
    # print("table_column_mapping:",table_column_mapping)

    formatted_result = map_columns_to_tables_and_values(sql_schema, extracted_values, table_column_mapping)
    return formatted_result
