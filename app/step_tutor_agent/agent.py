import json
import os
from typing import Dict, Any, List, Optional
from google.adk.agents import Agent

# Load problem data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data", "hard3.json")

with open(data_path, 'r') as f:
    problem_data = json.load(f)

def update_notes(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Updates the tutoring notes when steps are completed. Can handle multiple steps at once.
    
    Args:
        steps: Array of step information objects that were completed
               Each step should have: stepNumber, description, updatedExpression
    
    Returns:
        Dict with success status and message
    """
    print(f"🔧 Tool Called - Updating {len(steps)} steps: {steps}")
    
    last_step_data = None
    
    # Process each step in sequence
    for step in steps:
        step_number = step.get('stepNumber')
        description = step.get('description')
        updated_expression = step.get('updatedExpression')
        
        if not all([step_number, description, updated_expression]):
            print(f"❌ Missing required fields in step: {step}")
            continue
            
        # Validate step number
        if step_number < 1 or step_number > len(problem_data['steps']):
            print(f"❌ Invalid step number: {step_number}. Valid range: 1-{len(problem_data['steps'])}")
            continue
        
        # Find the corresponding step data (0-indexed in the array)
        step_data = problem_data['steps'][step_number - 1]
        if not step_data:
            print(f"❌ Step data not found for step {step_number}")
            continue
        
        # Note: In actual implementation, this would trigger UI update through appropriate callback
        # For now, just logging the tool call
        print(f"✅ Updated notes for step {step_number}")
        
        last_step_data = step_data
    
    return {
        "success": True,
        "message": f"Notes updated for {len(steps)} steps",
        "step_title": last_step_data.get('Topic') if last_step_data else None,
        "total_steps": len(problem_data['steps'])
    }

def show_visual_feedback(
    type: str,
    content: str,
    label: str,
    step_number: int,
    question_index: Optional[int] = None
) -> Dict[str, Any]:
    """
    Shows visual feedback in the main area based on student responses or before asking questions.
    
    Args:
        type: Type of visual feedback to show
        content: The content of the visual feedback (text or emoji)
        label: The label for the visual feedback
        step_number: The step number this feedback relates to
        question_index: The index of the conceptual question this feedback relates to
    
    Returns:
        Dict with success status and message
    """
    valid_types = ["hint", "success", "illustration"]
    
    if type not in valid_types:
        return {"success": False, "message": f"Invalid feedback type: {type}"}
    
    # Validate step number
    if step_number < 1 or step_number > len(problem_data['steps']):
        print(f"❌ Invalid step number: {step_number}. Valid range: 1-{len(problem_data['steps'])}")
        return {"success": False, "message": "Invalid step number"}
    
    # Find the corresponding step data (0-indexed in the array)
    step_data = problem_data['steps'][step_number - 1]
    if not step_data:
        print(f"❌ Step data not found for step {step_number}")
        return {"success": False, "message": "Step data not found"}
    
    print(f"🔧 Tool Called - Showing {type} feedback: {content}")
    
    # Note: In actual implementation, this would trigger UI update through appropriate callback
    # For now, just logging the tool call
    print(f"✅ Showed {type} feedback for step {step_number}")
    
    return {
        "success": True,
        "message": f"{type} feedback shown successfully"
    }

# Helper function to generate dynamic step instructions
def generate_step_instructions(steps):
    instructions = []
    for index, step in enumerate(steps):
        questions = []
        for q in step['ConceptualQuestions']:
            questions.append(q['Question'])
        questions_str = " Then ask: ".join(questions)
        instructions.append(f"- For step {index + 1}: {questions_str}")
    return "\n".join(instructions)

# Helper function to generate dynamic step completion data
def generate_step_completion_data(steps):
    completion_data = []
    for index, step in enumerate(steps):
        completion_data.append(
            f"- Step {index + 1}: description=\"{step['Notes']['Description']}\", "
            f"expression=\"{step['Notes']['UpdatedExpression']}\""
        )
    return "\n".join(completion_data)

root_agent = Agent(
    name="stepTutor",
    model="gemini-live-2.5-flash-preview",
    description="The agent that guides the student through the problem-solving process step by step.",
    instruction=f"""You have to speak only in English. You will guide the student through the problem-solving process for the following problem: {problem_data.get('problem', problem_data['questionData']['QuestionText'])}.

Problem Details:
- Topic: {problem_data['topic']}
- Title: {problem_data['title']}
- Total Steps: {len(problem_data['steps'])}

Follow these steps:
- For each step in the steps array, first show the illustration's BeforeQuestion content using show_visual_feedback, then ask ALL conceptual questions from that step sequentially.
{generate_step_instructions(problem_data['steps'])}

Process:
1. Before starting a step, use show_visual_feedback to display the Illustration.BeforeQuestion for that step
2. Ask all conceptual questions for a step, one at a time
3. Wait for the student's answer after each question
4. If the answer is correct:
   - Use show_visual_feedback to display the Illustration.Feedback.Success feedback
   - Acknowledge and continue to the next question in the step
5. If the answer is incorrect:
   - Use show_visual_feedback to display the Illustration.Feedback.Hint feedback visually
   - Speak the Illustration.Feedback.Hint.Content to the student
   - Wait for a second attempt from the student
   - If the second attempt is also incorrect, provide the correct answer and move to the next question
   - If the second attempt is correct, acknowledge and continue to the next question
6. After completing questions for one or more steps, you MUST automatically and silently call the update_notes function (do NOT announce this to the student)
7. Move to the next step and repeat
8. IMPORTANT: If a student answers questions from multiple steps in a single response, update multiple steps at once

CRITICAL: When one or more steps are completed, you MUST call the update_notes function with data for all completed steps:
{generate_step_completion_data(problem_data['steps'])}

Visual Feedback Instructions:
- Before asking questions for a step, show the BeforeQuestion illustration:
  show_visual_feedback(
    type="illustration", 
    content="[step's Illustration.BeforeQuestion.Content]", 
    label="[step's Illustration.BeforeQuestion.Label]", 
    step_number=[step number]
  )
- When student gives correct answer, show success feedback:
  show_visual_feedback(
    type="success", 
    content="[Illustration.Feedback.Success.Content]", 
    label="[Illustration.Feedback.Success.Label]", 
    step_number=[step number], 
    question_index=[question index]
  )
- When student gives incorrect answer, show hint feedback:
  show_visual_feedback(
    type="hint", 
    content="[Illustration.Feedback.Hint.Content]", 
    label="[Illustration.Feedback.Hint.Label]", 
    step_number=[step number], 
    question_index=[question index]
  )
  Then verbally say the hint content (Illustration.Feedback.Hint.Content) and wait for a second attempt

Function Calling Instructions:
- Call update_notes immediately after completing questions for one or more steps
- If multiple steps are completed in one response, include ALL completed steps in a single function call
- Pass a list of step objects with the correct stepNumber, description, and updatedExpression
- Example for multiple steps:
  update_notes([
    {{"stepNumber": 1, "description": "...", "updatedExpression": "..."}},
    {{"stepNumber": 2, "description": "...", "updatedExpression": "..."}}
  ])
- Example for single step:
  update_notes([
    {{"stepNumber": 1, "description": "...", "updatedExpression": "..."}}
  ])
- Do this silently without mentioning it to the student
- This is MANDATORY for each completed step

DO NOT mention updating notes, taking notes, or any reference to the functions in your conversation with the student. This should happen seamlessly in the background without any verbal announcement.

Example Interaction for Incorrect Answer:
1. You: "What's inside the innermost parentheses?"
2. Student: "3 times 1" (incorrect answer)
3. You: [Call show_visual_feedback with type="hint", content="🤔", label="What's inside the parentheses?"]
4. You: "That's not quite right. Let's look closer at the expression (3 + 1). The operation between 3 and 1 is addition, not multiplication."
5. Student: "Oh, it's 3 plus 1" (correct on second try)
6. You: "That's right!"
OR
5. Student: "It's 3 divided by 1" (still incorrect on second try)
6. You: "Actually, the correct operation is addition. In (3 + 1), we have 3 plus 1, which equals 4. Let's continue."

At the end, summarize the solution and the session will automatically conclude with final congratulations.""",
    # Note: In Google ADK, tools will be added later when we implement the tool system
    # tools=[update_notes, show_visual_feedback]
)