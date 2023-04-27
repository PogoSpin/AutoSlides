import os
import openai

def generate(prompt, key):
    openai.api_key = key
    answer = openai.Completion.create(
        model='text-davinci-003',
        prompt = prompt,
        max_tokens=100,
        temperature=0
    )
    return answer.choices[0].text