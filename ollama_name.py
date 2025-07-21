import requests

def query_ollama(model='qwen2', host='http://localhost:11434', user_query=''):


    prompt = f'''I will give you the user query, you will return the name of the user'''
    full_prompt = (f'''{prompt} \n\n'''
                f''' Now, do this for user_query: {user_query}''' 
                f''' Please return the user's name. Do not include any other information.''' )

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
    # user_query = " I am Jeremy Walsh. I bought a Phone from your company a few months ago, How can I maintain my phone and protect it?"
    # response = query_ollama(user_query=user_query)
    # print(f"Ollama 回复: {response}")
    # 预期输出: "Jeremy Walsh"
    user_name = "Jeremy Walsh"
    sql_template = '''Get purchase date, products, warranty status and manufacturing_batch_id for {user_name}\'s order'''
    sql = sql_template.format(user_name=user_name)
    print(f"SQL 查询: {sql}")