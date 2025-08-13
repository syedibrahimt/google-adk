import json
import os
from google.adk.agents import Agent

# Load problem data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data", "hard3.json")

with open(data_path, 'r') as f:
    problem_data = json.load(f)

root_agent = Agent(
    name="questionReader",
    model="gemini-live-2.5-flash-preview",
    description="The agent that reads out the question/problem with options and routes them to the correct downstream agent.",
    instruction=f"""You have to speak only in English. Ask the student whether they want to read the question read out loud or not. If they say yes, read the {problem_data.get('problem', problem_data['questionData']['QuestionText'])} and {problem_data['questionData'].get('Options', [])} to them. Once the question has been presented, the tutoring session will automatically begin."""
)