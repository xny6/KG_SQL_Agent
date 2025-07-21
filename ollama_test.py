import requests
import re
def query_ollama(prompt, model='qwen2', host='http://localhost:11434', user_query=None, sql_agent_response=None):

    full_prompt = (f'''{prompt} \n\n'''
                f''' user_query: {user_query}, sql_agent_response: {sql_agent_response}''' 
                f''' Please return the query in natural language, do not return any other information.''' )
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
    prompt ='''
    You are a helpful manager agent, who can divided the work between a SQL Agent and Knowledge Graph Agent to help the user. You will receive [User Query] and [SQL Agent Response] as input, generate [Query for Knowledge Graph Agent] as output.
    ****Example:****
    ***[User Query]: [My XPhone 15 Pro is randomly restarting. Is this a known issue for my specific phone, and what can I do?]
    ***[SQL Agent Response]: {[
    {
        "order_date":"2025-1-13",
        "product_name":"XPhone 15 Pro",
        "warranty_status":"In Warranty",
        "manufacturing_batch_id":"BATCH-X15P-2025-Q2-612"
    },
    {
        "order_date":"2025-1-13",
        "product_name":"XBook Air",
        "warranty_status":"In Warranty",
        "manufacturing_batch_id":"BATCH-X15P-2025-Q2-612"
    }
    ] }
    ***[Query for Knowledge Graph Agent]: [Find Restart Issues related to Product 'XPhone 15 Pro', and their associated Troubleshooting Steps.]

    Here is the thinking process:
    1. Find the key element and topic in [user query], which is "XPhone 15 Pro" and "randomly restarting".
    2. Find the key element and ignore the irrelevant elements in [SQL Agent response]. Key elements are "XPhone 15 Pro" and "In Warranty". Ignore irrelevant elements like "XBook Air".
    3. Combine the [user query] and [SQL Agent response] to form a query for the Knowledge Graph Agent. 
    
    Now, do this for the following input:
    '''

    user_query = "I am Jeremy Walsh. I bought a Phone from your company a few months ago, How can I maintain my phone and protect it?"
    sql_agent_response = '''{[
    {
        "order_date":"2022-10-14",
        "product_name":"CMF Buds",
        "warranty_status":"Out of Warranty",
        "manufacturing_batch_id":"BATCH-X15P-2024-Q2-612"
    },
    {
        "order_date":"2022-10-14",
        "product_name":"Nothing Phone 2A Plus",
        "warranty_status":"Out of Warranty",
        "manufacturing_batch_id":"BATCH-X15P-2024-Q2-612"
    }
] }'''
    model = "qwen2"  # 替换为你实际使用的模型名称
    response = query_ollama(prompt, model, user_query=user_query, sql_agent_response=sql_agent_response)
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    print(f"Ollama 回复: {response}")
