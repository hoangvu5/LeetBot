# LeetBot

Code that helps create [3Blue1Brown](https://www.youtube.com/@3blue1brown)'s level LeetCode shorts.

Example result video: [Link](https://www.youtube.com/shorts/EHdnbe0g_uY)

[![Link](https://img.youtube.com/vi/EHdnbe0g_uY/0.jpg)](https://www.youtube.com/watch?v=EHdnbe0g_uY)

(Auto-subtitle & background music added using CapCut)

### Description
- Selenium will scrape the LeetCode problem statement from the title slug.
- OpenAI's API will generate the script for the video.
- ElevenLabs will generate the voice for the video and the timestamps for each word.
- Manim library is used to render the video. Common data structures have been declared such as array, map,...
- User will have to manually copy and paste all the information needed into an LLM for it to generate Manim code for rendering the video.

### Prerequisites

1. Create a virtual environment named with `python -m venv <env-name>`.
2. Download all libraries necessary with `pip install -r requirements.txt`.
3. Make sure you have already installed Chrome or Firefox, depending what browser you choose to scrape with in `utils/selenium.py`
4. Set `OPENAI_API_KEY` and `XI_API_KEY` in environment file `.env`.
5. Install [ffmpeg](https://www.hostinger.com/tutorials/how-to-install-ffmpeg)
6. Install [Computer Modern](https://www.fontsquirrel.com/fonts/computer-modern) font and choose to install:
    - cmunbi
    - cmunrm
    - cmunti
7. Run `main.py` and then run `video.py`


### Video editing tutorial
1. Font: The Bold Font, Size: 16
2. Music: -10dB
