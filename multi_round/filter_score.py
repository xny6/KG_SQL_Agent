import json

# 输入和输出文件路径
input_file = "/home/NingyuanXiao/Vanna_test/enhanced_evaluation_results_answer.json_final.json"
output_file = "/home/NingyuanXiao/Vanna_test/multi_round/filtered_score_results_50.json"

def main():
    # 读取 JSON 文件
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 只保留 score = 0 或 25 的项
    filtered_data = [
        item for item in data
        if item.get("evaluation", {}).get("score") in [0, 25,50]
    ]

    # 保存结果到新文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"筛选完成，结果共 {len(filtered_data)} 条，已保存到 {output_file}")

if __name__ == "__main__":
    main()
