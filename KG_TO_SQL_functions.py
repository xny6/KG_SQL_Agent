import requests


def generate_sql_query(model='qwen2', host='http://localhost:11434', user_query=None, kg_agent_response=None):

    prompt = f'''
    You are a helpful manager agent, who can divided the work between a SQL Agent and Knowledge Graph Agent to help the user. You will receive [User Query] and [Knowledge Graph Agent Response] as input, generate [Query for SQL Agent] as output.

    ****Example:****
    ***[User Query]: [I found that you have a new device which supports foldable screen, can you tell me how much is it?]
    ***[Knowledge Graph Agent Response]: [The device with a foldable screen is the XPhone 15 Pro, XPhone 15 Pro Max and XPhone 15 Pro Ultra. They are all new released in 2024, with lots of new features.]
    ***[Query for SQL Agent]: [Get the name and price of XPhone 15 Pro, XPhone 15 Pro Max and XPhone 15 Pro Ultra, or other devices with similar name.]

    Here is the thinking process:
    1. Find the key element and topic in [user query], which is 'foldable screen' and 'how much'.
    2. Find the key element and ignore the irrelevant elements in [Knowledge Graph Agent response]. Key elements are "XPhone 15 Pro", "XPhone 15 Pro Max" and "XPhone 15 Pro Ultra". Ignore irrelevant elements like "new released in 2024".
    3. Combine the [user query] and [Knowledge Graph Agent response] to form a query for the SQL Agent. For example, Get the [target elements, like name, price, weight, etc.] of [target products, like XPhone 15 Pro, XPhone 15 Pro Max and XPhone 15 Pro Ultra], or other devices with similar name.
    4. Note, the elements in [Knowledge Graph Agent response] may be wrong and not complete, so you may adding 'or other devices with similar name' in the query for SQL Agent.
    5. Follow this tempalte: Get the name and [target elements] of [target products], or other devices with similar name.
    Now, do this for the following input:
    '''
    full_prompt = (f'''{prompt} \n\n'''
                   f''' Now, do this for user_query: {user_query}''' 
                   f''' and kg_agent_response: {kg_agent_response}''' 
                   f''' Please Only return the SQL query in natural language with one sentence. Do not include any other information.''' )

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


# user_query = "I see you have a special earphone which supports ANC, I want to know how much is it?"
# kg_agent_response= """
# The following earphone devices support Active Noise Cancellation (ANC):\n\n1. **Ear (a)** - This model utilizes ANC technology to provide superior noise cancellation, enhancing audio quality in various environments.\n\n2. **CMF Buds Pro 2** - The CMF Buds Pro 2 incorporates Adaptive Noise Control (ANC) to dynamically adjust the noise-cancellation based on the environment, providing an enhanced listening experience.\n\n3. **Buds Pro earbuds** - These earbuds feature ANC technology which reduces background noise during use, enhancing audio quality by minimizing unwanted external sounds.\n\n4. **Ear (stick)** - The Ear (stick) device features Active Noise Cancellation to ensure clear voice transmission without disturbance from background noise.\n\n5. **Nothing Ear Stick earbuds** - This model employs ENC technology to reduce background noise during calls and improves call clarity.\n\n6. **CMF Buds 2** - These headphones support ANC up to a maximum depth of 48dB, which significantly enhances the listening experience by reducing ambient noise.\n\n7. **Ear (1) earbuds** - The Ear (1) earbuds include an Active Noise Cancellation feature that can be managed through the Nothing X app for customization based on user preference and environmental conditions.\n\nThese devices leverage ANC technology to provide users with a more immersive listening experience by eliminating or reducing unwanted background noise.
# """

# SQL_Query= generate_sql_query(model='deepseek-r1:32b', user_query=user_query, kg_agent_response=kg_agent_response)

# print(SQL_Query)

def generate_kg_query(model='qwen2', host='http://localhost:11434', user_query=None):

    prompt = f"""You are a helpful manager agent, who can divided the work between a SQL Agent and Knowledge Graph Agent to help the user. You will receive [User Query], and generate [Query for Knowledge Graph Agent] as output.
    The Knowleddge Graph Agent focus on product details, features, and solutions, which are detailed, continuous information. For example, product names, product descriptions, detailed features, use instruction and trouble solutions .
    The SQL Agent focus on product names, sizes, prices, and orders, which are some distinct, points information. For example, product names, prices, sizes, quantities, orders, reviews, ratings, and customers.
    Here is an example:
    ****Example 1:****
    ***[User Query]: [I found that you have a new device which supports foldable screen, can you tell me how much is it?]
    ***[Query for Knowledge Graph Agent]: [Which devices support foldable screen?]

    ****Example 2:****
    ***[User Query]: [I found that your company sells lots of smartphones. What are the ratings of them?]
    ***[Query for Knowledge Graph Agent]: [What are the names of the smartphones sold by your company?]

    Here is the thinking process of Example 1:
    1. Find the key element and topic in [user query], which is 'foldable screen'.
    2. Since the Knowledge Graph Agent foucs on product features, the query should foucs on What prodcuts have the feature of 'foldable screen'. Only ask the Knowledge Graph Agent about which product has the feature. The price part should leave to the SQL Agent.
    3. Combine the [user query] to form a query for the Knowledge Graph Agent  [Which devices support foldable screen?]
    """

    full_prompt = (f'''{prompt} \n\n'''
                   f''' Now, do this for user_query: {user_query}'''
                   f''' Please Only return the query for Knowledge Graph Agent in natural language. Do not include any other information.''' )

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


# print(generate_kg_query(model='deepseek-r1:32b', user_query="I see you have a special earphone which supports ANC, I want to know how much is it?"))

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