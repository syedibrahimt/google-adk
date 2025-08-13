import json
import os
from google.adk.agents import Agent

# Load problem data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data", "hard3.json")

with open(data_path, 'r') as f:
    problem_data = json.load(f)

root_agent = Agent(
    name="closer",
    model="gemini-live-2.5-flash-preview",
    description="The final agent that summarizes the session and provides closure to the user.",
    instruction=f"""You have to speak only in English. Congratulate the student for successfully completing all the steps of the problem. Inform them that the final answer to the problem "{problem_data.get('problem', problem_data['questionData']['QuestionText'])}" is: {problem_data['steps'][-1]['Notes']['UpdatedExpression']}. Encourage them to keep practicing and let them know they did a great job!"""
)