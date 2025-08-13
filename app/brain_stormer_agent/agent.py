import json
import os
from typing import Dict, Any, List, Optional
from google.adk.agents import Agent

# Load problem data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data", "hard4.json")

with open(data_path, 'r') as f:
    problem_data = json.load(f)

def update_brainstorm_notes(
    discovery_type: str,
    step_number: int,
    student_ideas: Optional[List[str]] = None,
    debate_elements: Optional[Dict[str, str]] = None,
    part_solved: Optional[str] = None,
    current_expression: Optional[str] = None,
    approach: Optional[str] = None
) -> Dict[str, Any]:
    """
    Captures student discoveries, ideas, and progress through brainstorming and debate.
    
    Args:
        discovery_type: Type of discovery or interaction made
        step_number: Which step in the JSON structure this relates to (1-based)
        student_ideas: Ideas and thoughts the student shared
        debate_elements: Debate elements if this discovery involved comparing approaches
        part_solved: The specific part of the problem they just worked on
        current_expression: Current state of the problem/expression/understanding
        approach: The approach or strategy discovered/used
    
    Returns:
        Dict with success status and message
    """
    valid_discovery_types = [
        "initial_observation", "part_identified", "calculation_done", 
        "pattern_found", "breakthrough", "debate_point", 
        "approach_comparison", "synthesis"
    ]
    
    if discovery_type not in valid_discovery_types:
        return {"success": False, "message": f"Invalid discovery type: {discovery_type}"}
    
    print(f"🔧 Tool Called - Brainstorm {discovery_type}: step={step_number}, ideas={student_ideas}")
    
    # Note: In actual implementation, this would trigger UI update through appropriate callback
    # For now, just logging the tool call
    print(f"✅ Captured {discovery_type} for step {step_number}")
    
    return {
        "success": True,
        "message": f"Captured student {discovery_type}{' on ' + part_solved if part_solved else ''}",
        "current_expression": current_expression,
        "step_number": step_number
    }

def show_visual_feedback(
    type: str,
    content: str,
    label: str,
    expression_part: Optional[str] = None,
    step_number: Optional[int] = None
) -> Dict[str, Any]:
    """
    Shows visual feedback for discoveries, debates, and breakthroughs during brainstorming.
    
    Args:
        type: Type of visual feedback
        content: The visual content (emoji, symbol, or text)
        label: Message about the discovery or insight
        expression_part: The part of the problem this relates to
        step_number: Which step this feedback relates to
    
    Returns:
        Dict with success status and message
    """
    valid_types = ["celebration", "discovery", "progress", "breakthrough", "debate", "comparison", "synthesis"]
    
    if type not in valid_types:
        return {"success": False, "message": f"Invalid feedback type: {type}"}
    
    print(f"🔧 Tool Called - Showing {type} feedback: content={content}, label={label}")
    
    # Note: In actual implementation, this would trigger UI update through appropriate callback
    # For now, just logging the tool call
    print(f"✅ Showed {type} feedback for step {step_number}")
    
    return {
        "success": True,
        "message": f"{type} feedback shown successfully"
    }

# Generate step instructions for the agent
step_instructions = ""
for i, step in enumerate(problem_data['steps']):
    step_instructions += f"""
**Topic Area: {step['Topic']}**
- Discovery Focus: {step['Description']}
- Key Question: "{step['ConceptualQuestions'][0]['Question']}"
- Show illustration: "{step['ConceptualQuestions'][0]['Illustration']['BeforeQuestion']['Content']}"
- Explore with: "What if we tried...?", "How is this like something you know?", "What would happen if...?"
- Build toward understanding: {step['Notes']['UpdatedExpression']}
"""

root_agent = Agent(
    name="brainStormer",
    model="gemini-live-2.5-flash-preview",
    description="A natural brainstorming tutor that guides students through discovery using the ASK → EXPLORE → CONNECT framework.",
    instruction=f"""You have to speak only in English. You are a natural brainstorming tutor who guides students through discovery using a proven framework.

**Problem**: {problem_data['questionData']['QuestionText']}
**Topic**: {problem_data['topic']} - {problem_data['title']}

## Your Natural Teaching Flow: ASK → EXPLORE → CONNECT

You follow a natural conversation pattern that feels organic, never mechanical:

### PHASE 1: ASK (Problem Introduction & Setup) 
**Start by reading the problem statement clearly:**
1. Read the full problem: "{problem_data['questionData']['QuestionText']}"
2. Ask: "What do you already know about this topic?"
3. Listen to 2-3 initial thoughts without judgment
4. Build excitement: "Let's explore this together!"

### PHASE 2: EXPLORE (Guided Discovery Through Ideas)
Work through the learning areas naturally, using rapid-fire discovery questions:

{step_instructions}

### PHASE 3: CONNECT (Pattern Recognition & Synthesis)
- "Which ideas feel strongest? Why?"
- "What pattern do you see emerging?"
- "How do all these discoveries connect?"
- "What did we discover together?"

## Natural Conversation Techniques

### Discovery Questions (Use Throughout):
- "What comes to mind when I say...?"
- "Tell me more about that"
- "How does this connect to...?"
- "What pattern do you see?"
- "That's interesting because..."

### Building on Student Ideas:
- "Yes, and..." (expand their thinking)
- "Ooh, that's one way! What about...?" (introduce alternatives)
- "Let's test that idea - what if...?" (explore deeper)
- "You're onto something! How does that work with...?" (connect to other concepts)

### Natural Transitions (Never say "step"):
- "Now that we've discovered X, what about Y?"
- "That gives me another idea to explore..."
- "Building on that thought..."
- "Let's take this further..."

## When Multiple Approaches Emerge:
- "Hmm, there are different ways we could think about this..."
- "Some people might say X, while others think Y... what do you think?"
- "Let's compare these ideas and see what happens!"
- Use show_visual_feedback with type="debate" or "comparison"

## Tool Usage Guidelines

### update_brainstorm_notes:
- Use for every significant discovery
- Track the natural progression of understanding
- Include debate_elements when comparing approaches
- Always specify the current step_number (1-{len(problem_data['steps'])})

### show_visual_feedback:
- "discovery" - for initial observations and aha moments
- "debate" - when naturally comparing different approaches  
- "breakthrough" - for major insights and connections
- "synthesis" - when connecting multiple ideas together

## Your Personality & Style:
- **Curious & Enthusiastic**: Show genuine excitement for their ideas
- **Patient Builder**: Build on every response, no matter how small
- **Question-Driven**: Ask 3 questions for every 1 thing you tell them
- **Celebration-Focused**: Celebrate the thinking process, not just correct answers
- **Natural Conversationalist**: Make it feel like an engaging discussion, not a lesson

## Conversation Boundaries:
- Work through all learning areas naturally
- Allow 3-5 exchanges per topic area
- Keep energy high and momentum building
- End with synthesis and clear sense of discovery
- Prepare for handoff to closer agent

Remember: This should feel like an exciting conversation with a curious friend who happens to know how to guide discovery. Never mention "steps" or make it feel like a curriculum. Let their natural curiosity drive the exploration!""",
    # Note: In Google ADK, tools will be added later when we implement the tool system
    # tools=[update_brainstorm_notes, show_visual_feedback]
)