import json

# file2 = "/home/NingyuanXiao/Vanna_test/multi_round/eva1_final_50.json"   # 原始文件
# file1 = "/home/NingyuanXiao/Vanna_test/multi_round/filtered_score_results_50.json"   # 对比文件


file2 = "/home/NingyuanXiao/Vanna_test/multi_round/eva1_final.json"   # 原始文件
file1 = "/home/NingyuanXiao/Vanna_test/multi_round/filtered_score_results.json"   # 对比文件


def main():
    # 读取文件1
    with open(file1, "r", encoding="utf-8") as f:
        data1 = json.load(f)
    # 读取文件2
    with open(file2, "r", encoding="utf-8") as f:
        data2 = json.load(f)

    # 建立 file1 的 User Query -> score 映射
    scores1 = {item["User Query"]: item.get("evaluation", {}).get("score", -1) for item in data1}

    improved_count = 0
    total_compared = 0
    decreased_count = 0
    unchanged_count = 0

    # 遍历 file2，比较分数
    for item in data2:
        query = item.get("User Query")
        score2 = item.get("evaluation", {}).get("score", -1)
        score1 = scores1.get(query)

        if score1 is not None:  # file1 中也有这个 User Query
            total_compared += 1
            if score2 > score1:
                improved_count += 1
            elif score2 < score1:
                decreased_count += 1
            else:
                unchanged_count += 1

    print(f"共有 {total_compared} 个相同的 User Query 进行了对比")
    print(f"其中 {improved_count} 个分数在 file2 中有所提升")
    print(f"其中 {decreased_count} 个分数在 file2 中有所降低")
    print(f"其中 {unchanged_count} 个分数在 file2 中没有变化")

if __name__ == "__main__":
    main()
