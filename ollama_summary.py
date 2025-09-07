import requests
import json
import re
from KG_TO_SQL_functions_refine import summary_response

def query_ollama(model='deepseek-r1:32b', host='http://localhost:11434', user_query='', sql_answer='', kg_answer=''):


    prompt = f'''You are a helpful agent who is good at summarizing contents and providing final answer. 
    Now, you will receive TWO pieces of contents, one from a SQL Agent and another from a Knowledge Graph Agent. 
    The SQL agent's response focus on the products, orders, customers, product features, which are some distinct, points information. 
    The Knowledge Graph Agent's response focus on the solution, idea and description, which are detailed, continuous information.  
    Under a customer service scenario, please act as a customer server, combine [User query], [SQL Agent response], and [Knowledge Graph Agent response], to generate a final response to answer the user's query. The answer should be rich in content, with proper tone.
    Note, there may be conflicts between the SQL Agent response and the Knowledge Graph Agent response, such as different names. you should resolve these conflicts and provide a coherent final response.
    '''

    full_prompt = (f'''{prompt} \n\n'''
                f''' Now, do this for user_query: {user_query}, sql_answer: {sql_answer}, kg_answer: {kg_answer}''' 
                f''' Please return the final response in natural language, do not return any other information.''' )

    url = f'{host}/api/generate'
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ 出错：{e}"

if __name__ == "__main__":
    # 示例用法
    with open('/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_sql_kg_1.json', 'r') as f:
        data = json.load(f)
    model = "deepseek-r1:32b"  # 替换为你实际使用的模型名称
    result = []
    for item in data:
        user_query = item.get("User Query", "")
        sql_answer = item.get("SQL Result", "")
        kg_answer = item.get("KG Result", "")
        response = summary_response(model=model, user_query=user_query, sql_answer=sql_answer, kg_answer=kg_answer)
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        print(f"Response: {response}")
        item["Summary Result"] = response
        result.append(item)
    with open('/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_sql_kg_1_summary.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
        

    with open('/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_sql_kg_2.json', 'r') as f:
        data = json.load(f)
    model = "deepseek-r1:32b"  # 替换为你实际使用的模型名称
    result = []
    for item in data:
        user_query = item.get("User Query", "")
        sql_answer = item.get("SQL Result", "")
        kg_answer = item.get("KG Result", "")
        response = summary_response(model=model, user_query=user_query, sql_answer=sql_answer, kg_answer=kg_answer)
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        print(f"Response: {response}")
        item["Summary Result"] = response
        result.append(item)
    with open('/home/NingyuanXiao/Vanna_test/enhanced_prompt_injection_sql_kg_2_summary.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)