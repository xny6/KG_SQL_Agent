import json

# 支持多个输入文件
input_files = [
    '/home/NingyuanXiao/Vanna_test/enhanced_evaluation_results_reference_final.json',
    "/home/NingyuanXiao/Vanna_test/enhanced_evaluation_results_answer.json_final.json"
    
    
]

def main():
    all_scores = []
    total_samples = 0
    score_count = {0: 0, 25: 0, 50: 0, 75: 0, 100: 0}

    for input_file in input_files:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            scores = [item["evaluation"]["score"] for item in data if "evaluation" in item and "score" in item["evaluation"]]
            print(f"{input_file} 样本数: {len(scores)}")
            all_scores.extend(scores)
            total_samples += len(scores)
            # 统计各分数段数量
            for s in scores:
                if s in score_count:
                    score_count[s] += 1
        except Exception as e:
            print(f"读取文件 {input_file} 时出错: {e}")

    if all_scores:
        avg_score = sum(all_scores) / len(all_scores)
        print(f"总样本数: {total_samples}")
        print(f"总体平均得分: {avg_score:.2f}")
        print("各分数段数量：")
        for k in [0, 25, 50, 75, 100]:
            print(f"分数为 {k} 的数量: {score_count[k]}")
    else:
        print("未找到任何分数！")

if __name__ == "__main__":
    main()