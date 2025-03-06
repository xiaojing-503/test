question_schema_skeleton_instruction = (
    "Please generate the final SQL query by filling in the SQL skeleton based on the given question and database schema, without any explanation. Please try to follow the skeleton as much as possible. For column names containing spaces, please strictly escape them as quotation marks.\n"
)

question_schema_skeleton_inputs = (
    "Question: {question}\n"
    "Database schema: {schema_full}\n"
    "Skeleton: {skeleton}\n"
    "SQL:"
)


# question_schema_skeleton_instruction = (
#     "Please generate the final SQL query by filling in the SQL skeleton based on the given question and database schema, without any explanation.\n"
# )

# question_schema_skeleton_inputs = (
#     "Question: {question}\n"
#     "{schema_full}\n"
#     "Skeleton: {skeleton}\n"
#     "SQL:"
# )

question_schema_new_instruction = (
    "Please generate the final SQL query based on the given question and database schema, without any explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
)

question_schema_new_inputs = (
    "Question: {question}\n"
    "Database schema: {schema_new}\n"
    "SQL:"
)


# # result_correction_instruction=(
# #     "Answer the question using only an SQLite SQL query, combined with the database schema and SQL skeleton, with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
# # )

# # result_correction_inputs=(
# #     "Question: {question}\n"
# #     "Database schema: {schema_new}\n"
# #     "SQL skeleton: {skeleton_new}\n"
# #     "SQL:"
# # )


# # 都错了
# result_correction_instruction=(
#     "The following SQL contains some errors. Please correct them with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
# )

# # schema_full
# result_correction_inputs=(
#     "Old SQL: {err_pred}\n"
#     "Question: {question}\n"
#     "Database schema: {schema_new}\n"
#     "SQL:"
# )



# # skeleton错了
# result_correction_instruction_skeleton=(
#     "The following SQL has some errors. Please fix the SQL based on the question with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
# )

# # schema_new
# result_correction_inputs_skeleton=(
#     "Old SQL: {err_pred}\n"
#     "Question: {question}\n"
#     "SQL:"
# )


# # schema错了
# result_correction_instruction_schema=(
#     "The SQL skeleton is correct, but there are errors in the content. Please fix the SQL by selecting the correct tables, columns, and values based on the question and database schema with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
# )

# # schema_full
# result_correction_inputs_schema=(
#     "Old SQL: {err_pred}\n"
#     "Question: {question}\n"
#     "Database schema: {schema_new}\n"
#     "SQL:"
# )

# result_correction_instruction_simple=(
#     "The following SQL contains some errors. Please correct them with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
# )

# result_correction_inputs_simple=(
#     "Question: {question}\n"
#     "Database schema: {schema_new}\n"
#     "Old SQL: {err_pred}\n"
#     "SQL:"
# )


empty_correction_instruction=(
"The following SQL query contains errors in the database value references. Please modify the value references in the SQL based on the values mentioned in the question and the possibly correct values in the database. Note that no other parts need to be modified, simply output the modified SQL without any explanation. For column names containing spaces, please strictly escape them as quotation marks.\n")

empty_correction_inputs=(
    "Old SQL: {err_pred}\n"
    "Question: {question}\n"
    "Values: {values}\n"
    "Correct SQL:"
)

empty_correction_instruction_simple=(
"The following SQL query contains errors in the database value references. Please modify the value references in the SQL based on the values mentioned in the question. Note that no other parts need to be modified, simply output the modified SQL without any explanation.\n")

empty_correction_inputs_simple=(
    "Old SQL: {err_pred}\n"
    "Question: {question}\n"
    "Correct SQL:"
)

system_correction_instruction=(
    "When executing SQL below, some errors occurred, please fix up SQL based on question and database info. Solve the task step by step if you need to. Using SQL format in the code block, and indicate script type in the code block. When you find an answer, verify the answer carefully. For column names containing spaces, please strictly escape them as quotation marks.\n"
)

system_correction_inputs=(
    "Question: {question}\n"
    "Database schema: {schema_new}\n"
    "Old SQL: {err_pred}\n"
    "SQLite error: {err_desc}\n"
    "Now please fixup old SQL and generate new SQL again without any explanation.\n"
    "Correct SQL: ```sql```"
)


ablation_system_correction_instruction=(
    "When executing SQL below, some errors occurred, please fix up SQL based on question and database info and tips. Solve the task step by step if you need to. Using SQL format in the code block, and indicate script type in the code block. When you find an answer, verify the answer carefully.\n"
)

ablation_system_correction_inputs=(
    "Question: {question}\n"
    "Database schema: {schema_new}\n"
    "Old SQL: {err_pred}\n"
    "SQLite error: {err_desc}\n"
    "Tips: {tips}\n"
    "Now please fixup old SQL and generate new SQL again without any explanation.\n"
    "Correct SQL: ```sql```"
)

# 都错了
result_correction_instruction=(
    "The following SQL may contains some errors. Please correct them with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
)

# schema_full
result_correction_inputs=(
    "Old SQL: {err_pred}\n"
    "Question: {question}\n"
    "Database schema: {schema_full}\n"
    "SQL:"
)

# 只有skeleton错了
# 不给old sql 
# 给question+schema0+schema1
result_correction_instruction_skeleton=(
    "The following SQL may have skeleton errors. Please fix the SQL based on the question with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
)

# schema_new
result_correction_inputs_skeleton=(
    "Old SQL: {err_pred}\n"
    "Question: {question}\n"
    "Database schema: {schema_new}\n"
    "SQL:"
)

# schema错了
result_correction_instruction_schema=(
    "The SQL skeleton is correct, but there may be errors in the content. Please fix the SQL by selecting the correct tables, columns, and values based on the question and database schema with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
)

# schema_full
result_correction_inputs_schema=(
    "Old SQL: {err_pred}\n"
    "Question: {question}\n"
    "Database schema: {schema_full}\n"
    "SQL:"
)

result_correction_instruction_simple=(
    "The following SQL may contains some errors. Please correct them with no explanation. For column names containing spaces, please strictly escape them as quotation marks.\n"
)

result_correction_inputs_simple=(
    "Question: {question}\n"
    "Database schema: {schema_full}\n"
    "Old SQL: {err_pred}\n"
    "SQL:"
)