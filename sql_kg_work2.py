import json
import os
import re
from tqdm import tqdm
from SQL_TO_KG_functions import generate_sql_query_date,query_ollama_for_date,generate_kg_query
from test import run_sql_query

# 文件路径
input_file = '/home/NingyuanXiao/Vanna_test/user_queries_sql_kg3.txt'
output_file = 'sql_kg_3.json'

# 加载原始 user_queries
with open(input_file, 'r', encoding='utf-8') as file:
    user_queries = [line.strip() for line in file if line.strip()]

# 加载已处理数据（如存在）
if os.path.exists(output_file):
    with open(output_file, 'r', encoding='utf-8') as f:
        processed_data = json.load(f)
else:
    processed_data = []

# 提取已处理的 user queries
processed_queries = set(item.get("User Query", "") for item in processed_data)

# 过滤未处理的 user queries
unprocessed_queries = [uq for uq in user_queries if uq not in processed_queries]

print(f"🔍 Total: {len(user_queries)} queries, {len(unprocessed_queries)} left to process.")

while True:
    # 过滤未处理的 user queries
    unprocessed_queries = [uq for uq in user_queries if uq not in set(item.get("User Query", "") for item in processed_data)]
    if not unprocessed_queries:
        print("✅ All queries processed!")
        break
    print(f"🔍 {len(unprocessed_queries)} queries left to process.")
    for user_query in tqdm(unprocessed_queries, desc="Processing queries", unit="query"):
        try:
            date = query_ollama_for_date(user_query=user_query)
            SQL_Query = generate_sql_query_date(date)
            SQL_Result = run_sql_query(question=SQL_Query)
            KG_Query = generate_kg_query(
                model='deepseek-r1:32b',
                user_query=user_query,
                sql_agent_response=SQL_Result
            )
            KG_Query = re.sub(r'<think>.*?</think>', '', KG_Query, flags=re.DOTALL)
            result = {
                "User Query": user_query,
                "SQL Query": SQL_Query,
                "SQL Result": SQL_Result,
                "KG Query": KG_Query,
                "KG Result": "",
                "Summary Result": ""
            }
            processed_data.append(result)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"❌ Error processing '{user_query}': {e}")
            print("🔁 Skipping to next...")
            continue