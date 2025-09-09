import json
import os
import re
import time
from tqdm import tqdm
from KG_TO_SQL_functions import generate_sql_query, summary_response
from test import run_sql_query

# 文件路径
input_file = '/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_kg_sql_reference.json'
output_file = '/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_kg_sql_reference_processed.json'

# 读取原始输入
with open(input_file, 'r', encoding='utf-8') as f:
    all_data = json.load(f)

while True:
    # 如果已处理文件存在，加载；否则为空列表
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            processed_data = json.load(f)
    else:
        processed_data = []

    # 获取已处理的 "User Query" 集合
    processed_queries = set(item.get("User Query", "") for item in processed_data)

    # 筛选未处理的项
    unprocessed_items = [item for item in all_data if item.get("User Query", "") not in processed_queries]

    print(f"\n🔍 Still {len(unprocessed_items)} unprocessed items out of {len(all_data)} total.")

    # 如果全部处理完毕，退出循环
    if not unprocessed_items:
        print("\n✅ All items processed successfully!")
        break

    # 使用 tqdm 展示进度条
    for item in tqdm(unprocessed_items, desc="🚀 Processing", unit="item"):
        user_query = item.get("User Query", "")
        KG_Query = item.get("KG Query", "")
        KG_Result = item.get("KG Result", "")

        try:
            SQL_Query = generate_sql_query(model='qwen2', user_query=user_query, kg_agent_response=KG_Result)
            SQL_Query = re.sub(r'<think>.*?</think>', '', SQL_Query, flags=re.DOTALL)

            SQL_Result = run_sql_query(question=SQL_Query)

            Summary_Result = summary_response(
                model='deepseek-r1:32b',
                user_query=user_query,
                sql_answer=SQL_Result,
                kg_answer=KG_Result
            )
            Summary_Result = re.sub(r'<think>.*?</think>', '', Summary_Result, flags=re.DOTALL)

            # 添加处理结果
            processed_data.append({
                "User Query": user_query,
                "SQL Query": SQL_Query,
                "SQL Result": SQL_Result,
                "KG Query": KG_Query,
                "KG Result": KG_Result,
                "Summary Result": Summary_Result
            })

            # 写入文件（每个 item 后写一次，避免中断丢数据）
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"\n❌ Error processing query: {user_query}")
            print(f"   Reason: {e}")
            continue

    # 每轮处理后等待一小段时间，防止重复频繁触发
    time.sleep(1)
