import requests
import json
import re

use_azure = True
if use_azure:
    url = "your-url"
    headers = {
        "Content-Type": "application/json",
        "api-key": "your-api-key"
    }
else:
    url = "https://api.openai.com/v1/chat/completions"
    # Replace 'your-api-key' with your actual OpenAI API key
    OPENAI_API_KEY = 'your-api-key'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }


def get_code(user_prompt, his):
    prompt = f"""Based on the given history:
    {his}
    
    write Python code to accomplish the following task:
    {user_prompt}

    Please write a step-by-step plan in English, outlining what you want to achieve, and provide the corresponding valid Python code in a triple backtick Markdown code block below. 
    Make sure all code is valid and can be run in a Jupyter Python 3 kernel environment. 
    Remember to define every variable before using it.
    The data file you will need can be found in the folder './files/xxxx'.
    Additionally, please use matplotlib to generate any required charts and save them locally in the './images/output.png' directory.
    Please note that you should provide a clear and well-structured implementation of the given task, ensuring that the code is readable and easy to understand."""

    system = """
    You are a Data Analysis Scientist, a specialist in analyzing and interpreting complex datasets. 
    You employ a variety of techniques, including machine learning and data mining, to identify patterns, trends, and relationships in data. 
    """

    messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]

    data = {
        "messages": messages,
        "temperature": 0.7,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        content = response.json()['choices'][0]['message']['content']
    except:
        print('error')


    def extract_code(text):
        # Match triple backtick blocks first
        triple_match = re.search(r'```(?:\w+\n)?(.+?)```', text, re.DOTALL)
        if triple_match:
            return triple_match.group(1).strip()
        else:
            # If no triple backtick blocks, match single backtick blocks
            single_match = re.search(r'`(.+?)`', text, re.DOTALL)
            if single_match:
                return single_match.group(1).strip()

    return extract_code(content), content.strip()