import requests
import re
import json

def query_ollama_for_user_name(model='qwen2', host='http://localhost:11434', user_query=None, sql_agent_response=None):
    """
    Query the Ollama model to extract the user's name from the user query.
    
    Args:
        model (str): The model name to use for querying.
        host (str): The host URL for the Ollama API.
        user_query (str): The user query containing the user's name.
        
    Returns:
        str: The extracted user's name.
    """
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



def generate_sql_query(user_name):
    """
    Generate a SQL query to get purchase date, products, warranty status and manufacturing batch ID for the user's order.
    
    Args:
        user_name (str): The name of the user.
        
    Returns:
        str: The generated SQL query.
    """
    sql_template = '''Get purchase date, products, price and warranty status for {user_name}\'s order, check them in products, orders, order_items and customers tables.'''
    return sql_template.format(user_name=user_name)



def generate_kg_query(prompt, model='qwen2', host='http://localhost:11434', user_query=None, sql_agent_response=None):


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


def summary_response(model='deepseek-r1:32b', host='http://localhost:11434', user_query='', sql_answer='', kg_answer=''):


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