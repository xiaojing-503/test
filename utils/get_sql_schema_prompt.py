def format_database_schema(data_dict):
    # 初始化存储表结构的字典
    tables = {}

    # 遍历输入字典，构建表结构
    for key in data_dict.keys():
        table, column = key.split(':')
        if table not in tables:
            tables[table] = []
        if column not in tables[table]:
            tables[table].append(column)

    # 开始格式化数据库模式字符串
    result_lines = []

    for table, columns in tables.items():
        formatted_columns = []

        for column in columns:
            # 获取当前列的值
            full_column_name = f"{table}:{column}"
            values = data_dict[full_column_name]

            if values:  # 如果有值
                # Step 1: Create a list of formatted strings for each value
                formatted_values = []
                for value in values:
                    # Format string-like values with quotes and numeric values without
                    if value.startswith('(') and value.endswith(')'):  # Consider values wrapped in parentheses as strings
                        formatted_values.append(f"{value[1:-1]}")  # Remove parentheses
                    else:
                        formatted_values.append(value)

                # Step 2: Join the formatted values into a single string, separated by commas
                formatted_values_str = ', '.join(formatted_values)

                # Step 3: Combine the column name with the formatted values string
                formatted_column = f"`{column}` (values: '{formatted_values_str}')"
            else:  # 如果没有值
                formatted_column = f"`{column}`"

            formatted_columns.append(formatted_column)

        # 合并表和列描述成最终描述
        result_lines.append(f"table {table.lower()}, columns = [{', '.join(formatted_columns)}]")

    return '; '.join(result_lines)
