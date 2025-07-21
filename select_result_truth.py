import json

# 加载第一个 JSON 文件
with open('/home/NingyuanXiao/Vanna_test/queries_result2_processed.json', 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

# 加载第二个 JSON 文件
with open('/home/NingyuanXiao/Vanna_test/qa_output.json', 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)

# 构建第二个文件的问题到答案的映射，便于查找
question_to_answer = {entry['question']: entry['answer'] for entry in data2}

# 存储匹配结果
matched_results = []

# 匹配并提取所需字段
for entry in data1:
    user_query = entry.get('User Query')
    if user_query in question_to_answer:
        matched_results.append({
            'Question': user_query,
            'Summary Result': entry.get('Summary Result'),
            'answer': question_to_answer[user_query]
        })

# 将结果写入新 JSON 文件
with open('/home/NingyuanXiao/Vanna_test/select_results_truth.json', 'w', encoding='utf-8') as fout:
    json.dump(matched_results, fout, ensure_ascii=False, indent=2)

print(f"完成匹配，共写入 {len(matched_results)} 条数据到 /home/NingyuanXiao/Vanna_test/select_results_truth.json。")
