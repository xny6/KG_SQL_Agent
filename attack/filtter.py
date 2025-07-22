import json

# 输入和输出文件路径
input_file = "/home/NingyuanXiao/Vanna_test/queries_result2_processed.json"  # 原始JSON文件
output_file = "/home/NingyuanXiao/Vanna_test/attack/kg_sql_without_summary.json"  # 修改后的JSON文件

# 读取原始JSON文件
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)  # 假设是JSON数组

# 遍历每个JSON对象，将"Summary Result"设置为空
for item in data:
    if "Summary Result" in item:
        item["Summary Result"] = ""

# 保存修改后的数据到新文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"已处理 {len(data)} 个JSON对象，结果保存到 {output_file}")