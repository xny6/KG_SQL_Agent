import json
from KG_TO_SQL_functions_refine import generate_sql_query, generate_kg_query, summary_response
import re
# from test import run_sql_query

results = []

with open('/home/NingyuanXiao/Vanna_test/user_queries_refine.txt', 'r') as f:
    user_queries = f.read().strip()  
    for user_query in user_queries.split('\n'):
        if not user_query.strip():
            continue
        print(f"Processing user query: {user_query}")
        user_query = user_query.strip()
        KG_Query=generate_kg_query(model='deepseek-r1:32b', user_query=user_query)
        KG_Query = re.sub(r'<think>.*?</think>', '', KG_Query, flags=re.DOTALL)

        result = {
            "User Query": user_query,
            "SQL Query": '',
            "SQL Result": '',
            "KG Query": KG_Query,
            "KG Result": '',
            "Summary Result": ''
        }
        results.append(result)
        
        print(KG_Query)
        print("===" * 20)
