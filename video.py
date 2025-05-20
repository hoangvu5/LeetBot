from utils import chatgpt
import json
import os

def main():
    # Ctrl + F and search `cfg` to check variables
    with open("config.json", 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # Get data
    title_slug = input("Title slug of the problem: ")
    cache_path = f"cache/data/{title_slug}.json"
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    except FileNotFoundError:
        print("Cannot find problem file")
        exit(1)

    # Generate
    video_prompt = chatgpt.generate_video_prompt(
        cache["title"], 
        cache["description"], 
        cache["example"], 
        cache["script"], 
        cache["timestamps"]
    )
    
    response = chatgpt.complete_video_chat(video_prompt, cfg["gen_model"])
    start = response.find("```python") + len("```python")
    end = response.find("```", start)
    extracted_code = response[start:end].strip()

    os.makedirs("cache/code", exist_ok=True)
    with open(f"cache/code/{title_slug}.txt", 'w', encoding='utf-8') as f:
        f.write(extracted_code)
    print(f"\nCode saved as cache/code/{title_slug}.txt!")

if __name__ == "__main__":
    main()
    