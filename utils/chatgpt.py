from openai import OpenAI
from dotenv import load_dotenv
import os
import ast

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

def complete_chat(messages, model, title_slug):
    template = [
        {
            "role": "system",
            "content": "You are a programmer proficient in competitive programming.",
        },
        {
            "role": "user",
            "content": messages,
        }
    ]
    response = client.chat.completions.create(
        model = model,
        messages = template,
        temperature = 0.01,
    )

    # save text
    text = response.choices[0].message.content
    directory = 'cache/generated-text'
    if not os.path.exists(directory):
        os.makedirs(directory)

    gen_path = f"cache/generated-text/{title_slug}.txt"
    with open(gen_path, 'w', encoding='utf-8') as f:
        f.write(text)

    return text
    

def postprocessing(response):
    response = response.replace("```json\n", "").replace("\n```", "")
    final_dict = ast.literal_eval(response)

    return final_dict
    
def generate_prompt(description, example, solution, language="Python"):
    prompt = f"""
    ### INSTRUCTION ###
    You have to write a script for a video that presents a coding exercise and its solution. Your script should contain the following sections:
    1. Statement: Define the problem. Leave out unnecessary specifics mentioned in the problem such as the time complexity, the constraints, how the output must be formatted, or how the input ensures something, etc. If you want to write arithmetic symbols such as +, -, *, or /, you should write it as plus, minus, multiply by, or divide by. Simplify the problem as much as possible to not confuse the listeners.
    2. Example: Start the section with "For this example, ..." Use the example testcase below for this section. If you want to write arithmetic symbols such as +, -, *, or /, you should write it as plus, minus, multiply by, or divide by.
    3. Thought process: Concisely explain your solution. Start the section with "Let's go over the thought process." If you want to write arithmetic symbols such as +, -, *, or /, you should write it as plus, minus, multiply by, or divide by. If a solution is provided, then your thought process should align with the given solution.
    4. Solution: This section only contains the solution in {language}. In the {language} code, do not write in-line or multiline comments above or next to sections of code. Do not explain the code after writing it. The newline character should be escaped like `\\n`. The code should only contain the class Solution which contains a function that solves the problem, like in LeetCode style.

    ### PROBLEM ###
    {description}

    ### EXAMPLE TESTCASE ###
    {example}

    ### SOLUTION ###
    {solution}

    ### OUTPUT FORMAT ###
    The output should be a markdown code snippet formatted in the following schema, including the leading and trailing ```json and ```. In the output, for statement, example, definition, and thought_process, do not use any punctuations except for comma and full stop. For example, don't use brackets when listing out the elements inside an array:
    ```json
    {{
        "statement": string, // state the problem
        "example": string, // present and explain the example testcase
        "thought_process": string, // explain the thought process
        "solution": string, // solution in {language} and formatted as a string
    }}
    ```
    """
    return prompt

def get_timestamps(directory, model):
    audio_file = open(directory, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model=model,
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )
    return transcript.words

def generate_video_prompt(title, description, example, script, timestamps):
    prompt = f"""
    Currently we have a LeetCode problem, along with the example variables of one testcase. \
    Your task right now is to generate Python code to create animation from the example variables \
    that fits the timestamp of the prompt spoken in the video.

    The problem is {title}. Here's the description of the problem:
    {description}

    This is one example of the given variables and the expected answer in JSON format:
    {example}

    These are the Python classes and their functions you are already provided for creating the \
    animation. You don't have to implement it. You may not have to use all of it, depending on if \
    the prompt mentions it or not, or the problem or the solution needs it or not. You are not \
    allowed to use manim's self.play() function, and all the animation function needed are all \
    provided below:
    class MTitle
        - def __init__(title, difficulty, scene=self): Create an MTitle with title `title` and subtitle `difficulty`. When setting the title, only use the problem's title (e.g. Two Sum) and not the whole LeetCode problem number.
        - def run(run_time=1): Display the title. Can change default run_time (1 second).
        - .mobject: Get the manim object of the MTitle

    class MArray
        - def __init__(name, array, scene=self, center=coor): Create an MArray with name `name` and Python list `array`
        - def run(run_time=1): Display the array. Can change default run_time (1 second).
        - def highlight_element(idx, color=BLUE, run_time=1): Highlight element at index `idx` (index starts from 0), can change `color` to WHITE to unhighlight and can change default run_time (1 second). Before highlight element again, please unhighlight the element first and unhighlight the element for a while before highlight immediately.
        - def highlight_elements(indices, color=BLUE, run_time=1): Highlight elements with index inside `indices, can change `color` to WHITE to unhighlight and can change default run_time (1 second). Use this when you need to highlight multiple indices all at once.
        - def highlight_range(start, end, color=BLUE, run_time=1): Highlight elements from `start` to `end` inclusive, can change `color` to WHITE to unhighlight and can change default run_time (1 second). Use this when you need to highlight range all at once.
        - .array: Get the Python array of the MArray
        - .mobject: Get the manim object of the MArray

    class MVariable
        - def __init__(name, variable, scene=self, center=coor): Create an MVariable with name `name` and Python integer `variable`
        - def run(run_time=1): Display the variable. Can change default run_time (1 second).
        - def highlight_variable(color=BLUE, run_time=1): Highlight the variable, can change `color` to WHITE to unhighlight and can change default run_time (1 second).
        - def disappear(run_time=1): Make the variable disappear. Can change default run_time (1 second).
        - .variable: Get the value of the MVariable
        - .mobject: Get the manim object of the MVariable

    class MMap
        - def __init__(name, map, scene=self, center=coor): Create an MMap with name `name` and Python dict `map`
        - def run(run_time=1): Display the map. Can change default run_time (1 second).
        - def insert_element(key, value, run_time=1): Insert a key, value pair into the map and render new map. Can change default run_time (1 second)
        - def remove_element(key, run_time=1): Delete a key from the map and render new map. Can change default run_time (1 second)
        - .map: Get the Python dict of the MMap
        - .mobject: Get the manim object of the MMap

    class MText
        - def __init__(text, scene=self, center=coor): Create an MText with text `text`. When creating this object, try to reduce the length of the text to fit in the screen.
        - def run(run_time=1): Display the text. Can change default run_time (1 second).
        - def edit(new_text, run_time=1): Morph into `new_text`. Can change default run_time (1 second).
        - def disappear(run_time=1): Make the text disappear. Can change default run_time (1 second).
        - .text: Get the value of the text
        - .mobject: Get the manim object of the MText

    class MStack
        - def __init__(name, stack, scene=self, center=coor): Create an MStack with name `name` and Python list `stack`
        - def run(run_time=1): Display the stack. Can change default run_time (1 second).
        - def highlight_top(color=BLUE, run_time=1): Highlight element at the top of the stack, can change `color` to WHITE to unhighlight and can change default run_time (1 second). Before highlight element again, please unhighlight the element first and unhighlight the element for a while before highlight immediately.
        - def push(value, run_time=1): Make the top element of the stack fade in. Can change default run_time (1 second).
        - def pop(run_time=1): Make the top element of the stack fade out. Can change default run_time (1 second). Return the value of the top element. Return -1 if the stack is empty.
        - def top(): Return the value of the top element. Return -1 if the stack is empty.
        - .stack: Get the Python list of the MStack
        - .mobject: Get the manim object of the MStack

    This is the prompt for today's animation:
    {script}
    
    There are timestamps for each word spoken in seconds in JSON format. Besides using the functions \
    above, you must remember to use manim's self.wait() function, in order to sync between the \
    animation and the prompt. You can calculate the time needed to wait between two specific animations \
    by subtracting the two timestamps. Remember to also take into account the time it takes for \
    the animation's run time (by default it is 1 second per animation function):
    {timestamps}

    All of your output code should be placed inside function `def construct(self):` only, and not a \
    class. Do not import any libraries or wrap a class outside `def construct(self):`. You may write \
    out your thought process step by step but finally, you have to write your output code at the end \
    of your response. In your thought process, you should plan out what animation should be played or what \
    data structures should be created and rendered at this timestamp when this word is spoken, \
    the time it takes for the animation to play, and the time needed to wait until the next animation is rendered. 
    If there's no time to wait between two animations, then don't need to use self.wait(). \
    When naming new variables or data structures to solve the problem, try to make \
    the name short but still understandable (e.g: ma for map, se for set, etc.). Carefully check \
    the logic of the code.

    Before calling any functions, you should declare this `coor = ORIGIN + UP * 2.05`. After creating \
    objects representing data structures or variables (except MTitle), you should write this `coor[1] -= 0.5`. \
    If you erase or make a data structure disappear, then after it you should write `coor[1] += 0.5`.
    """

    return prompt

def complete_video_chat(messages, model):
    template = [
        {
            "role": "system",
            "content": "You are a senior Python developer, specialized in creating math animations using manim Python library.",
        },
        {
            "role": "user",
            "content": messages,
        }
    ]
    response = client.chat.completions.create(
        model = model,
        messages = template,
        temperature = 0.01,
    )

    text = response.choices[0].message.content
    return text


