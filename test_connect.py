import requests
import json

def extract_answer(model='deepseek-r1:32b', host='http://localhost:11434', answer=''):


    prompt = f'''You are a helpful agent who is good at extracting the answer from the given content.
    You will receieve a summarized content, you need to extract the product and its corresponding answer from the content.
    An example is given below:
    ****Example:****
    [Summarized Content]: [Certainly! Here's the organized and elegant presentation of the earphones that support ANC along with their respective prices:\n\n---\n\n**Active Noise Cancellation (ANC) Earphone Options**\n\n1. **Nothing Ear A**: Experience superior noise cancellation at $329.\n\n2. **CMF Buds Pro 2**: Enjoy dynamic ANC for enhanced listening, priced at $329.\n\n3. **Buds Pro earbuds (CMF Buds Pro)**: Immerse yourself in clear audio with ANC for $299.\n\n4. **Nothing Ear Stick**: Get exceptional call clarity with ANC at $349.\n\n5. **Ear (1) (Nothing Ear 1)**: Customize your ANC experience through the Nothing X app, priced at $299.\n\n6. **CMF Buds 2**: Enjoy ANC up to 48dB for a richer listening experience at $299.\n\n---\n\nEach of these earphones is designed to enhance your audio experience by effectively reducing background noise, ensuring clarity and immersion in various environments."]
    [Extract Content]: [1. Nothing Ear A: $329, 2. CMF Buds Pro 2: $329, 3. Buds Pro earbuds (CMF Buds Pro): $299, 4. Nothing Ear Stick: $349, 5. Ear (1) (Nothing Ear 1): $299, 6. CMF Buds 2: $299]
    ****End of Example****
    In short, you need to extract the [product] and its [corresponding answer] from the content. The [corresponding answer] may include price, weight, stock quantity, or other information.
    '''

    full_prompt = (f'''{prompt} \n\n'''
                f''' Now, do this for the [Summarized Content]: {answer}\n\n''' 
                f''' Please return the extracted content in natural language, do not return any other information.''' )

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
        
        
        
with open('/home/NingyuanXiao/Vanna_test/queries_result.json', 'r') as f:
    data = json.load(f)

for entry in data:
    summary_result = entry.get("Summary Result", "")
    answer = extract_answer(answer=summary_result)
    print('=================================================================')
    print(f"Extracted Answer: {answer}")

