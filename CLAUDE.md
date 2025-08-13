# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google ADK (Agent Development Kit) tutoring system that implements an interactive multi-agent educational platform. The system guides students through step-by-step problem-solving using specialized AI agents, each handling different phases of the tutoring experience.

## Architecture

### Multi-Agent System
The application follows a sequential agent handoff pattern where each agent handles a specific phase of the tutoring session:

1. **Greeter Agent** (`app/greeter_agent/`) - Welcomes students and introduces the topic
2. **Question Reader Agent** (`app/question_reader_agent/`) - Reads out problems with options and routes to appropriate agents
3. **Brain Stormer Agent** (`app/brain_stormer_agent/`) - Guides discovery using ASK → EXPLORE → CONNECT framework
4. **Step Tutor Agent** (`app/step_tutor_agent/`) - Provides detailed step-by-step problem solving
5. **Closer Agent** (`app/closer_agent/`) - Summarizes the session and provides final congratulations

### Agent Implementation Pattern
All agents follow a consistent structure:
- Import Google ADK's `Agent` class from `google.adk.agents`
- Load problem data from JSON files in the `data/` directory
- Define specialized tool functions (when applicable) with proper typing
- Create agent instances with specific models, descriptions, and detailed instructions

### Data Structure
- Problem data stored in `data/` directory as JSON files (hard3.json, hard4.json)
- Each problem contains: topic, title, questionData, steps array with ConceptualQuestions
- Steps include Topic, Description, ConceptualQuestions, and visual Illustrations

## Development Commands

### Python Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (pytest available)
python -m pytest

# Run specific test file
python -m pytest path/to/test_file.py
```

### Key Dependencies
- `google-adk==1.10.0` - Core agent framework
- `fastapi==0.116.1` - Web framework
- `uvicorn==0.35.0` - ASGI server
- `pydantic==2.11.7` - Data validation
- Google Cloud services (BigQuery, Storage, Speech, etc.)

## Agent Development Guidelines

### Tool Functions
When implementing agent tools, follow this pattern:
```python
def tool_function(param: str, optional_param: Optional[str] = None) -> Dict[str, Any]:
    """
    Description of the tool's purpose.
    
    Args:
        param: Description of required parameter
        optional_param: Description of optional parameter
    
    Returns:
        Dict with success status and message
    """
    # Validation logic
    if invalid_condition:
        return {"success": False, "message": "Error description"}
    
    # Tool implementation
    print(f"🔧 Tool Called - {tool_name}: {params}")
    
    # In actual implementation, this would trigger UI updates
    print(f"✅ Tool execution completed")
    
    return {"success": True, "message": "Success description"}
```

### Agent Instructions
Agent instructions should be comprehensive and include:
- Clear personality and teaching style guidelines
- Detailed conversation flow and transitions
- Tool usage guidelines with specific parameters
- Boundary conditions and handoff criteria
- Visual feedback patterns for UI integration

### Problem Data Integration
Agents dynamically generate instructions based on problem data structure:
- Load JSON data using relative paths from agent directory
- Generate step-by-step instructions from problem steps array
- Include validation for step numbers and data integrity

## Legacy Code
The `app/old_agents/` directory contains JavaScript implementations that have been migrated to Python. These files are kept for reference but should not be modified for new development.

## File Structure Navigation
- `/app/[agent_name]_agent/agent.py` - Main agent implementations
- `/data/*.json` - Problem and tutorial data files
- `/requirements.txt` - Python dependencies
- Legacy JS agents in `/app/old_agents/` (reference only)