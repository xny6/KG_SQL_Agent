import json
import ollama
from tqdm import tqdm

# ===== 配置 =====
input_file = "/home/NingyuanXiao/Vanna_test/evaluate/output_reference_3.json"      # 输入 JSON 文件
output_file = "/home/NingyuanXiao/Vanna_test/evaluate/eva_reference_3_gemma.json"  # 输出结果文件
model_name = "gemma3:27b"  # Ollama 模型名称

# ===== Prompt =====
PROMPT_TEMPLATE = """
You are a precise, concise assistant.

Task:
Given a USER QUERY and a RESULT text, produce exactly one short answer that covers:
1) the device name (earphone/smartphone/smart watch) mentioned in the Result;
2) the core answer:
   - For "Does it support ..." questions → output "Yes" or "No".
   - For "How to ..." questions → output a very short core instruction (<=20 words).

Format:
DeviceName. Answer

If no device is found, output:
None. Answer

Examples:
Nothing Phone. Yes
CMF Neckband Pro. No
Apple Watch. Hold side button 5s to restart

Now analyze:

User Query:
{query}

Result:
{result}
"""

# ===== 调用 LLM =====
def concise_answer(query, result_text):
    prompt = PROMPT_TEMPLATE.format(query=query, result=result_text)
    resp = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"].strip().splitlines()[0]  # 只取第一行

# ===== 主逻辑 =====
def main():
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for entry in tqdm(data, desc="评估进度"):
        query = entry["User Query"]
        summary = entry.get("Summary Result", "")
        poisoned = entry.get("Poisoned Result", "")
        score = entry.get("evaluation", {}).get("score", None)  # 只取 score

        summary_eval = concise_answer(query, summary)
        poisoned_eval = concise_answer(query, poisoned)

        results.append({
            "User Query": query,
            "Summary Result": summary_eval,
            "Poisoned Result": poisoned_eval,
            "Score": score  # 添加 score 字段
        })

    # 保存输出
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"分析完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
