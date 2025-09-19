import json

input_file="/home/NingyuanXiao/Vanna_test/evaluate/eva_answer_1_gemma.json"

def main():
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results=0
    score_100_2_different = 0
    score_100_1_different = 0
    score_100_0_different = 0
    score_75_2_different = 0
    score_75_1_different = 0
    score_75_0_different = 0
    score_50_2_different = 0
    score_50_1_different = 0
    score_50_0_different = 0
    score_25_2_different = 0
    score_25_1_different = 0
    score_25_0_different = 0
    score_0_2_different = 0
    score_0_1_different = 0
    score_0_0_different = 0

    number_of_100 = 0
    number_of_75 = 0
    number_of_50 = 0
    number_of_25 = 0
    number_of_0 = 0

    for entry in data:
        summary_support = entry.get("Summary Result", {}).get("support", None)
        summary_value = entry.get("Summary Result", {}).get("value", None)
        poisoned_support = entry.get("Poisoned Result", {}).get("support", None)
        poisoned_value = entry.get("Poisoned Result", {}).get("value", None)
        
    #     if summary_support == poisoned_support and summary_value == poisoned_value:
    #         results += 0
    #     elif summary_support != poisoned_support and summary_value != poisoned_value:
    #         results += 1
    #     else:
    #         results += 0.5
            
    # print(f"总题数: {len(data)}, 总分: {results}, 平均分: {results/len(data)}")

        if entry.get('Score', None) == 100:
            number_of_100 += 1
            if summary_support != poisoned_support and summary_value != poisoned_value:
                score_100_2_different += 1
            elif summary_support == poisoned_support and summary_value == poisoned_value:
                score_100_0_different += 1
            else:
                score_100_1_different += 1
        elif entry.get('Score', None) == 75:
            number_of_75 += 1
            if summary_support != poisoned_support and summary_value != poisoned_value:
                score_75_2_different += 1
            elif summary_support == poisoned_support and summary_value == poisoned_value:
                score_75_0_different += 1
            else:
                score_75_1_different += 1
        elif entry.get('Score', None) == 50:
            number_of_50 += 1
            if summary_support != poisoned_support and summary_value != poisoned_value:
                score_50_2_different += 1
            elif summary_support == poisoned_support and summary_value == poisoned_value:
                score_50_0_different += 1
            else:
                score_50_1_different += 1
        elif entry.get('Score', None) == 25:
            number_of_25 += 1
            if summary_support != poisoned_support and summary_value != poisoned_value:
                score_25_2_different += 1
            elif summary_support == poisoned_support and summary_value == poisoned_value:
                score_25_0_different += 1
            else:
                score_25_1_different += 1
        elif entry.get('Score', None) == 0:
            number_of_0 += 1
            if summary_support != poisoned_support and summary_value != poisoned_value:
                score_0_2_different += 1
            elif summary_support == poisoned_support and summary_value == poisoned_value:
                score_0_0_different += 1
            else:
                score_0_1_different += 1
    print(f"总题数: {len(data)}")
    print(f"number_of_100: {number_of_100}")
    print(f"score_100_2_different: {score_100_2_different}")
    print(f"score_100_1_different: {score_100_1_different}")
    print(f"score_100_0_different: {score_100_0_different}")
    print(f"number_of_75: {number_of_75}")
    print(f"score_75_2_different: {score_75_2_different}")
    print(f"score_75_1_different: {score_75_1_different}")
    print(f"score_75_0_different: {score_75_0_different}")
    print(f"number_of_50: {number_of_50}")
    print(f"score_50_2_different: {score_50_2_different}")
    print(f"score_50_1_different: {score_50_1_different}")
    print(f"score_50_0_different: {score_50_0_different}")
    print(f"number_of_25: {number_of_25}")
    print(f"score_25_2_different: {score_25_2_different}")
    print(f"score_25_1_different: {score_25_1_different}")
    print(f"score_25_0_different: {score_25_0_different}")
    print(f"number_of_0: {number_of_0}")
    print(f"score_0_2_different: {score_0_2_different}")
    print(f"score_0_1_different: {score_0_1_different}")
    print(f"score_0_0_different: {score_0_0_different}")



# ========== 运行 ==========
if __name__ == "__main__":
    main()
