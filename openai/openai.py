import requests

# Replace YOUR_API_KEY with your actual API key
api_key = "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"


headers = {
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}


def getChatGPt_response(q):
  json_data={
    "model": "text-ada-001",
    "prompt": f"{q}",
    "max_tokens": 128,
    "temperature": 0.5
  }

  response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data)
  response=response.json()
  return response['choices'][0]['text'] 
  # print()

# quest=input("Enter Question\n")
# getChatGPt_response(quest)