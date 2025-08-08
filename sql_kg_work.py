# from SQL_TO_KG_functions import generate_sql_query, generate_kg_query, query_ollama_for_user_name
# from test import run_sql_query
# import re
# import json

# results = []

# with open('/home/NingyuanXiao/Vanna_test/user_queries_sql_kg.txt', 'r') as file:
#     user_queries = [line.strip() for line in file if line.strip()]

# for user_query in user_queries:
#     user_name = query_ollama_for_user_name(user_query=user_query)
#     SQL_Query = generate_sql_query(user_name)
#     SQL_Result = run_sql_query(question=SQL_Query)

#     kg_query_prompt = '''
#         You are a helpful manager agent, who can divided the work between a SQL Agent and Knowledge Graph Agent to help the user. You will receive [User Query] and [SQL Agent Response] as input, generate [Query for Knowledge Graph Agent] as output.
#         ****Example:****
#         ***[User Query]: [My XPhone 15 Pro is randomly restarting. Is this a known issue for my specific phone, and what can I do?]
#         ***[SQL Agent Response]: {[
#         {
#             "order_date":"2025-1-13",
#             "product_name":"XPhone 15 Pro",
#             "warranty_status":"In Warranty",
#             "manufacturing_batch_id":"BATCH-X15P-2025-Q2-612"
#         },
#         {
#             "order_date":"2025-1-13",
#             "product_name":"XBook Air",
#             "warranty_status":"In Warranty",
#             "manufacturing_batch_id":"BATCH-X15P-2025-Q2-612"
#         }
#         ] }
#         ***[Query for Knowledge Graph Agent]: [Find Restart Issues related to Product 'XPhone 15 Pro', and their associated Troubleshooting Steps.]

#         Here is the thinking process:
#         1. Find the key element and topic in [user query], which is "XPhone 15 Pro" and "randomly restarting".
#         2. Find the key element and ignore the irrelevant elements in [SQL Agent response]. Key elements are "XPhone 15 Pro" and "In Warranty". Ignore irrelevant elements like "XBook Air".
#         3. Combine the [user query] and [SQL Agent response] to form a query for the Knowledge Graph Agent. 
        
#         Now, do this for the following input:
#         '''
#     KG_Query = generate_kg_query(prompt=kg_query_prompt, model='deepseek-r1:32b', user_query=user_query, sql_agent_response=SQL_Result)
#     KG_Query = re.sub(r'<think>.*?</think>', '', KG_Query, flags=re.DOTALL)

#     results.append({
#         "User Query": user_query,
#         "SQL Query": SQL_Query,
#         "SQL Result": SQL_Result,
#         "KG Query": KG_Query,
#         "KG Result": '',
#         "Summary Result": ''
#     })

# with open('skq_kg_1.json', 'w') as f:
#     json.dump(results, f, ensure_ascii=False, indent=4)


import json
import os
import re
from tqdm import tqdm
from SQL_TO_KG_functions import generate_sql_query, generate_kg_query, query_ollama_for_user_name
from test import run_sql_query

# 文件路径
input_file = '/home/NingyuanXiao/Vanna_test/user_queries_sql_kg2.txt'
output_file = 'sql_kg_2.json'

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
            user_name = query_ollama_for_user_name(user_query=user_query)
            SQL_Query = generate_sql_query(user_name)
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

