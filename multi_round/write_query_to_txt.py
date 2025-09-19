import json

# 输入和输出文件路径
input_file = "/home/NingyuanXiao/Vanna_test/multi_round/filtered_score_results_50.json"   # 已经筛选过的 JSON
output_txt = "/home/NingyuanXiao/Vanna_test/multi_round/user_queries_50.txt"

def main():
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(output_txt, "w", encoding="utf-8") as f:
        for item in data:
            query = item.get("User Query", "")
            if query:
                f.write(f"{query}\n")

    print(f"已将 {len(data)} 条 User Query 保存到 {output_txt}")

if __name__ == "__main__":
    main()
