import pandas as pd
import json
import io  # ✅ 正确的 StringIO 导入

# 读取 questions.txt
with open('/home/NingyuanXiao/Vanna_test/user_queries_kg_sql.txt', 'r', encoding='utf-8') as f:
    questions = [line.strip() for line in f if line.strip()]

all_data = []

for i, question in enumerate(questions, 1):
    print(f"\n【问题 {i}】：{question}")
    print("请输入该问题对应的答案 DataFrame（例如：name,price\\nApple,299\\nGoogle,399）")
    print("⚠️ 输入完成后，输入一行 END 结束：")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    if not lines:
        print("⚠️ 没有输入任何内容，跳过该问题")
        continue

    try:
        # ✅ 正确使用 io.StringIO
        df = pd.read_csv(io.StringIO('\n'.join(lines)))
        answer_data = df.to_dict(orient='records')
    except Exception as e:
        print(f"❌ 解析失败：{e}")
        continue

    all_data.append({
        'question': question,
        'answer': answer_data
    })

# 保存为 JSON 文件
with open('qa_output.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("✅ 所有问题与答案已成功保存到 qa_output.json")
