# readme.md

python3 -m venv .venv && source .venv/bin/activate
pip install -U "smolagents[toolkit]" "smolagents[litellm]"  # toolkit = default tools (web search, etc.)


I installed 

ollama pull qwen2.5:3b
ollama run qwen2.5:3b


Discovery/Trends:
  python smolagent.py "Analyze all journal entries in [directory path]. Look for patterns, recurring themes, mood trends over time, and topics I
  write about most. Summarize key insights about my interests and emotional patterns."

  Personal Growth:
  python smolagent.py "Read through my journal entries in [directory] and identify signs of personal growth, challenges I'm working through, and
  goals or aspirations that keep coming up. What advice would you give based on what you see?"

  Mood & Wellbeing:
  python smolagent.py "Analyze the emotional tone and mood patterns in my journal entries from [directory]. Are there specific triggers, seasonal
  patterns, or activities that correlate with positive/negative moods?"

  Topic Analysis:
  python smolagent.py "Read my journal entries in [directory] and categorize them by main topics. What are my biggest concerns, interests, and
  focus areas? Create a summary of what matters most to me based on frequency and emotional weight."

  Timeline View:
  python smolagent.py "Look at my journal entries in [directory] chronologically and tell me how my thoughts, priorities, and concerns have
  evolved over time. What changes do you notice?"

