import json
import os
from google.adk.agents import Agent

# Load problem data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data", "hard3.json")

with open(data_path, 'r') as f:
    problem_data = json.load(f)

root_agent = Agent(
    name="greeter",
    model="gemini-live-2.5-flash-preview",
    description="The initial agent that welcomes and greets the user to the tutoring session.",
    instruction=f"""You have to speak only in English. Welcome the student to the tutoring session. Tell them that they will be learning about {problem_data['topic']}: {problem_data['title']}. 
Be encouraging and supportive in your tone. Once you've provided a warm welcome, the session will automatically proceed to the next phase."""
)