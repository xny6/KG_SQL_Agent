import json

# 输入和输出文件路径
input_file = "/home/NingyuanXiao/Vanna_test/enhanced_evaluation_results_reference_final.json"
output_file = "/home/NingyuanXiao/Vanna_test/evaluate/output_reference_4.json"

# 选择区间 [start, end) ，包含 start，不包含 end
start_index = 259
end_index = 319

def main():
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 切片选择
    filtered_data = data[start_index:end_index]

    # 保存到新文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"已保存 {len(filtered_data)} 条记录到 {output_file}")

if __name__ == "__main__":
    main()
