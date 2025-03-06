from sqlglot import parse_one, exp

sql = "SELECT DISTINCT s.\"school\", CONCAT(s.\"street\", ', ', s.\"city\", ', ', s.\"state\", ' ', s.\"zip\") AS \"full_communication_address\" FROM frpm f INNER JOIN schools s ON f.\"cdscode\" = s.\"cdscode\" WHERE s.\"city\" = 'Monterey' AND f.\"frpm count (ages 5-17)\" > 800"

# print all column references (a and b)
for column in parse_one(sql).find_all(exp.Column):
    print(column.alias_or_name)

# find all projections in select statements (a and c)
for select in parse_one(sql).find_all(exp.Literal):
    for projection in select.expressions:
        print(projection.this)

# find all tables (x, y, z)
for table in parse_one(sql).find_all(exp.Table):
    print(table.name)