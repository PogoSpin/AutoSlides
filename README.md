# AutoSlides
Automatically creates a google slide presentation from a given topic with Chat GPT 3.5-turbo. 

### How it works

It uses pyautogui to move your mouse cursor to the positions of elements on google slides.
ChatGPT generates a list of slide titles for the topic you chose and then creates each slide and generates the body for each.

## Features

- Generate slides for any topic
- Choose the amount of slides and the amount of words per slide
- It saves your api key and position information locally for later use

## Cons

It does the job but there is no GUI and it doesn't give a lot of options when it comes to customizing the end result.

## Installation
Clone the project and install the requirements.
1. `git clone https://github.com/PogoSpin/AutoSlides`
2. `pip install -r requirements.txt`

## Usage

1. Run the code with `python main.py` and follow the intructions. 
2. The first time you run the program you need to input you openai key from https://platform.openai.com/account/api-keys. It will also prompt you to record the positions of each element on google slides.
3. Then you input the presentation topic, slide amount, word limit and then run.

Everything is explained in the program in case of any confusion.
