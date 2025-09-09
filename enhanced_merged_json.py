import json

# 手动输入 JSON 文件路径（可以改成你的实际路径）
json_files = ['/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_kg_sql_answer_processed.json',
              '/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_sql_kg_1_reference_summary.json',
              '/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_sql_kg_2_reference_summary.json'


]

output_file = "/home/NingyuanXiao/Vanna_test/enhanced_reference_all.json"

merged_data = []

for file_path in json_files:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
        if isinstance(data, list):
            merged_data.extend(data)  # 列表直接合并
        elif isinstance(data, dict):
            merged_data.append(data)  # 字典加入列表
        else:
            print(f"⚠ 文件 {file_path} 格式不支持，已跳过")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

print(f"✅ 合并完成，结果已保存到 {output_file}")
