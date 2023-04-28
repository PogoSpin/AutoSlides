import os
import openai

def generate(prompt, key):
    openai.api_key = key
    completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': prompt}
    ]
    )

    return completion.choices[0].message.content