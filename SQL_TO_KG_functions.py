import requests
import re
import json

def query_ollama_for_user_name(model='qwen2', host='http://localhost:11434', user_query=None):
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

def query_ollama_for_date(model='qwen2', host='http://localhost:11434', user_query=None):
    """
    Query the Ollama model to extract the date from the user query.
    
    Args:
        model (str): The model name to use for querying.
        host (str): The host URL for the Ollama API.
        user_query (str): The user query containing the date.
        
    Returns:
        str: The extracted date.
    """
    prompt = f'''
    I will give you the user query, you will return the date in YYYY-MM-DD format

    ***Example***
    [User Query]:I return a product on 2025-05-02. How do I use the flashlight on the Watch Pro?
    [Date]: 2025-05-02
    '''
    full_prompt = (f'''{prompt} \n\n'''
                   f''' Now, do this for user_query: {user_query}''' 
                   f''' Please return the date in YYYY-MM-DD format. Do not include any other information.''' )

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

# print(query_ollama_for_date(user_query='I return a product on 2025-07-15. Will my phone lose data when getting repaired?'))

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

def generate_sql_query_date(date):
    sql_template="Get the product name in return form where return date is {date}"
    return sql_template.format(date=date)

print(generate_sql_query_date(query_ollama_for_date(user_query='I return a product on 2024-05-17. How do I operate the control functions on the Buds?')))

kg_query_prompt = '''
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

def generate_kg_query(prompt=kg_query_prompt, model='qwen2', host='http://localhost:11434', user_query=None, sql_agent_response=None):


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