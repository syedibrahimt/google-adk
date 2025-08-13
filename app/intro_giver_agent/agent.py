import json
import os
from typing import Dict, Any
from google.adk.agents import Agent

# Load problem data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data", "hard3.json")

with open(data_path, 'r') as f:
    problem_data = json.load(f)

def show_intro_visual(content: str, label: str, explanation: str, type: str = "text") -> Dict[str, Any]:
    """
    Shows introduction visual content and explanation in the main area.
    
    Args:
        content: The content of the visual (could be text, URL, or emoji)
        label: The label/description for the visual
        explanation: The explanation text to be shown with the visual
        type: The type of visual content (text, image, etc.)
    
    Returns:
        Dict with success status and message
    """
    print(f"🔧 Tool Called - Showing introduction visual: content={content}, label={label}, type={type}")
    
    # Note: In actual implementation, this would trigger UI update through appropriate callback
    # For now, just logging the tool call
    print(f"✅ Showed introduction visual")
    
    return {
        "success": True,
        "message": "Introduction visual shown successfully"
    }

root_agent = Agent(
    name="introGiver",
    model="gemini-live-2.5-flash-preview",
    description="The agent that introduces the concept with a visual aid and explanation.",
    instruction=f"""You have to speak only in English. Your job is to introduce the mathematical concept to the student.

First, speak the introduction text: "{problem_data['introData']['Voice']}"

Then, use the show_intro_visual function to display the visual aid and explanation to the student:
show_intro_visual(
    content="{problem_data['introData']['Visual']['Content']}",
    label="{problem_data['introData']['Visual']['Label']}",
    explanation="{problem_data['introData']['TopicExplanation']}",
    type="{problem_data['introData']['Visual']['Type']}"
)

After introducing the concept, pause briefly to allow the student to absorb the information, then inform them that you'll be moving on to the problem itself. The session will automatically continue to the next phase where the problem will be presented.

Note: Always maintain an encouraging and supportive tone. Make the student feel comfortable with learning the new concept.""",
    # Note: In Google ADK, tools will be added later when we implement the tool system
    # tools=[show_intro_visual_tool]
)