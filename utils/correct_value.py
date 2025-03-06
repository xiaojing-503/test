import sqlite3

def find_similar_values_in_all_tables(db_path, value, case_sensitive=False):
    """
    使用 LIKE 或 ILIKE 进行模糊匹配，查找与给定值相似的数据库记录，同时返回列名和对应的值
    遍历数据库中的所有表，检查每个表的所有列

    :param db_path: SQLite 数据库文件路径
    :param value: 错误的值
    :param case_sensitive: 是否区分大小写
    :return: 与给定值相似的值以及表名、列名
    """
    # 连接 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取数据库中的所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # 存储相似值
    similar_values = []

    # 将 value 转换为字符串
    value = str(value)
    value_length = len(value)

    # 最大匹配长度
    max_length = value_length * 2

    # 使用 ILIKE 进行不区分大小写匹配，或者使用 LIKE 进行区分大小写匹配
    like_operator = f"COLLATE NOCASE" if not case_sensitive else ""

    # 遍历每个表
    for table_tuple in tables:
        table_name = table_tuple[0]

        # 获取表的所有列名
        cursor.execute(f"PRAGMA table_info(`{table_name}`);")
        columns = cursor.fetchall()

        # 遍历表中的每一列
        for column in columns:
            column_name_in_table = column[1]

            # 使用 LIKE 或 ILIKE 查找与 value 相似的值
            # 在 SQLite 中，我们可以使用 '%value%' 来表示模糊匹配
            like_query = f"""
                SELECT DISTINCT `{column_name_in_table}` 
                FROM `{table_name}` 
                WHERE `{column_name_in_table}` LIKE ? 
                AND LENGTH(`{column_name_in_table}`) <= ?
                {like_operator}
            """

            cursor.execute(like_query, ('%' + value + '%', max_length))  # 使用 '%' 来表示模糊匹配
            db_values = cursor.fetchall()

            # 遍历数据库中的所有匹配值
            for db_value_tuple in db_values:
                db_value = db_value_tuple[0]  # 获取列值

                # 确保 db_value 不是 None
                if db_value is not None:
                    # 将 db_value 转换为字符串
                    db_value = str(db_value)

                    # 添加匹配的值到结果
                    similar_values.append((table_name, column_name_in_table, db_value))  # 返回表名、列名、值

    # 关闭数据库连接
    conn.close()

    return similar_values

# # 示例使用
# BIRD_DATABASE='/root/Text-to-SQL/hdd/BIRD/data/sft_data_collections/bird/dev/dev_databases/'
# db_path = BIRD_DATABASE+'california_schools/california_schools.sqlite'  # SQLite 数据库路径
# value = '613360'  # 错误值

# similar_values = find_similar_values_in_all_tables(db_path, value, case_sensitive=False)

# # 打印最相似的值和对应的表名及列名
# for table, col, val in similar_values:
#     print(f"Table: {table}, Column: {col}, Value: {val}")
