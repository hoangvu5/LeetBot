from openai import OpenAI
from dotenv import load_dotenv
from settings import CACHE_GEN_TEXT_DIR
import ast
import logging
import os

load_dotenv()

log = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def complete_chat(prompt: str, model: str, title_slug: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a programmer proficient in competitive programming.",
        },
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.01,
    )
    text = response.choices[0].message.content

    os.makedirs(CACHE_GEN_TEXT_DIR, exist_ok=True)
    gen_path = f"{CACHE_GEN_TEXT_DIR}/{title_slug}.txt"
    with open(gen_path, "w", encoding="utf-8") as f:
        f.write(text)
    log.info("Script cached to %s", gen_path)

    return text


def postprocessing(response: str) -> dict:
    response = response.replace("```json\n", "").replace("\n```", "")
    return ast.literal_eval(response)


def generate_prompt(description: str, example: str, solution: str, language: str = "Python") -> str:
    return f"""
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
    The output should be a markdown code snippet formatted in the following schema, including the leading and trailing ```json and ```. In the output, for statement, example, definition, and thought_process, do not use any punctuations except for comma and full stop. Every sentence must end with a full stop. Keep each sentence short, no more than 20 words. Do not write run-on sentences. For example, don't use brackets when listing out the elements inside an array:
    ```json
    {{
        "statement": string, // state the problem
        "example": string, // present and explain the example testcase
        "thought_process": string, // explain the thought process
        "solution": string, // solution in {language} and formatted as a string
    }}
    ```
    """


def get_timestamps(audio_path: str, model: str, script: str = "") -> list:
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model=model,
            response_format="verbose_json",
            timestamp_granularities=["word"],
        )
    words = [{"word": w.word, "start": w.start, "end": w.end} for w in transcript.words]

    # Align transcribed timing to known script words to fix Whisper mis-recognitions.
    if script:
        script_words = script.split()
        if abs(len(script_words) - len(words)) <= max(5, int(len(words) * 0.15)):
            # Counts are close enough — replace recognized words with script words.
            for i, entry in enumerate(words):
                if i < len(script_words):
                    entry["word"] = script_words[i]

    return words


def _condense_timestamps(timestamps: list[dict], max_group: int = 10) -> list[dict]:
    """Group word-level timestamps into sentence/phrase markers for the video prompt.

    Returns a compact list of {"t": float, "text": str} — one entry per sentence
    (split on terminal punctuation) or per max_group words.
    """
    sentences: list[dict] = []
    current_words: list[str] = []
    current_start: float | None = None

    for entry in timestamps:
        word = entry["word"].strip()
        start = entry["start"]

        if current_start is None:
            current_start = start

        current_words.append(word)
        ends_sentence = word.endswith((".", "!", "?"))

        if ends_sentence or len(current_words) >= max_group:
            sentences.append({"t": round(current_start, 2), "text": " ".join(current_words)})
            current_words = []
            current_start = None

    if current_words and current_start is not None:
        sentences.append({"t": round(current_start, 2), "text": " ".join(current_words)})

    return sentences


def generate_video_prompt(cache: dict) -> str:
    """Build the Manim code-generation prompt from the full problem cache dict."""
    title       = cache["title"]
    difficulty  = cache["difficulty"]
    description = cache["description"]
    example     = cache["example"]
    script      = cache["script"]
    timestamps  = cache["timestamps"]

    condensed   = _condense_timestamps(timestamps)
    total_dur   = round(timestamps[-1]["end"], 2) if timestamps else 0

    return f"""
    Currently we have a LeetCode problem, along with the example variables of one testcase. \
    Your task right now is to generate Python code to create animation from the example variables \
    that fits the timing of the narration spoken in the video.

    The problem is {title} ({difficulty}). Here's the description of the problem:
    {description}

    This is one example of the given variables and the expected answer in JSON format:
    {example}

    These are the Python classes and their functions you are already provided for creating the \
    animation. You don't have to implement them. Choose only the classes relevant to the problem. \
    You are not allowed to use manim's self.play() function directly — all animation is done \
    through the methods listed below. All text uses CMU Serif font automatically:

    class MTitle
        - def __init__(title, difficulty, scene=self): Use only the problem title (e.g. "Two Sum"), not the full LeetCode number.
        - def run(run_time=1): Display the title card, then shrink it to the top of the screen.
        - .mobject

    class MArray
        - def __init__(name, array, scene=self, center=coor): Horizontal array display.
        - def run(run_time=1)
        - def highlight_element(idx, color=BLUE, run_time=1): Unhighlight (color=WHITE) before re-highlighting.
        - def highlight_elements(indices, color=BLUE, run_time=1): Highlight multiple indices at once.
        - def highlight_range(start, end, color=BLUE, run_time=1): Highlight a contiguous range inclusive.
        - def disappear(run_time=1)
        - .array, .mobject

    class MVariable
        - def __init__(name, variable, scene=self, center=coor)
        - def run(run_time=1)
        - def highlight_variable(color=BLUE, run_time=1)
        - def disappear(run_time=1)
        - .variable, .mobject

    class MMap
        - def __init__(name, map, scene=self, center=coor): Dict display rendered as text.
        - def run(run_time=1)
        - def insert_element(key, value, run_time=1)
        - def remove_element(key, run_time=1)
        - def highlight_element(key, color=BLUE, run_time=1): Highlight a specific key-value pair.
        - def highlight(color=BLUE, run_time=1): Highlight the entire map text.
        - def disappear(run_time=1)
        - .map, .mobject

    class MText
        - def __init__(text, scene=self, center=coor): Short text label. Keep text brief to fit the screen.
        - def run(run_time=1)
        - def edit(new_text, run_time=1): Morph to new text.
        - def disappear(run_time=1)
        - .text, .mobject

    class MStack
        - def __init__(name, stack, scene=self, center=coor): Horizontal stack with a bounding box.
        - def run(run_time=1)
        - def highlight_top(color=BLUE, run_time=1)
        - def push(value, run_time=1)
        - def pop(run_time=1): Returns popped value, or -1 if empty.
        - def top(): Returns top value, or -1 if empty.
        - def disappear(run_time=1)
        - .stack, .mobject

    class MLinkedList
        - def __init__(name, values, scene=self, center=coor): Singly-linked list rendered as boxes with arrows.
        - def run(run_time=1)
        - def highlight_node(index, color=BLUE, run_time=1): Highlight box + value at position index.
        - def highlight_next(index, color=BLUE, run_time=1): Highlight the arrow out of node at index.
        - def disappear(run_time=1)
        - .values, .mobject

    class MBinaryTree
        - def __init__(name, array, scene=self, center=coor): Binary tree from LeetCode-style level-order list (None = absent node).
        - def run(run_time=1)
        - def highlight_node(index, color=BLUE, run_time=1): index is the array index.
        - def highlight_edge(parent_index, child_index, color=BLUE, run_time=1)
        - def disappear(run_time=1)
        - .array, .mobject

    class MGraph
        - def __init__(name, adj, scene=self, directed=False, center=coor): Graph from adjacency dict {{node: [neighbours]}}.
        - def run(run_time=1)
        - def highlight_node(node, color=BLUE, run_time=1)
        - def highlight_edge(u, v, color=BLUE, run_time=1): For undirected, order doesn't matter.
        - def disappear(run_time=1)
        - .adj, .mobject

    --- LAYOUT (IMPORTANT) ---
    This is a portrait video (YouTube Shorts). The Manim frame is 4.5 units wide (x: -2.2 to 2.2) \
    and 8 units tall (y: -4 to 4). After MTitle.run(), the title bar sits at y ≈ 2.9–3.25. \
    Place all other content objects below y = 2.0 to avoid overlap with the title bar.

    Approximate rendered heights of objects (after their internal scaling):
      MText / MVariable / MMap  →  ~0.7 units tall
      MArray / MStack           →  ~1.0 units tall (taller with index labels)
      MLinkedList               →  ~0.8 units tall
      MBinaryTree               →  ~2.5 units tall
      MGraph                    →  ~2.0 units tall

    Placement rules:
      1. Declare at the top:  coor = ORIGIN + UP * 1.5
      2. After MTitle.run(), do NOT adjust coor.
      3. After creating each data structure, decrement coor[1] by the object's height + 0.3 gap.
         e.g. after MArray:  coor[1] -= 1.3   (1.0 height + 0.3 gap)
              after MText:   coor[1] -= 1.0   (0.7 height + 0.3 gap)
      4. When a data structure disappears, add back the same amount.
      5. Keep at most 3 objects visible simultaneously to avoid crowding.
      6. For MBinaryTree or MGraph, disappear other objects first to free vertical space.

    --- TIMING ---
    This is the narration script for the video:
    {script}

    Sentence-level timing markers (each entry: time in seconds → phrase spoken at that time).
    Total audio duration: {total_dur}s — the video must last at least this long.
    Use self.wait() to sync animations: wait_time = marker_time - time_elapsed_so_far.
    Skip self.wait() if the result is zero or negative.
    {condensed}

    Output only the body of `def construct(self):` — no class wrapper, no imports. \
    You may reason step by step first, but place the final code block at the very end. \
    When naming variables, keep names short (e.g. mp=map, st=stack, ll=linked_list). \
    Verify timing carefully: the animation must cover the full {total_dur}s of narration.
    """


def complete_video_chat(prompt: str, model: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a senior Python developer, specialized in creating math animations using manim Python library.",
        },
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.01,
    )
    return response.choices[0].message.content
