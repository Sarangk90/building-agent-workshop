# LangGraph Studio Configuration

This directory contains the LangGraph Studio configuration for the travel agents from the workshop notebooks.

## Agents Available

### 1. Travel Agent (`travel_agent.py`)
- **Graph ID**: `travel_agent`
- **Description**: Advanced travel agent using LangGraph with tool calling
- **Features**: 
  - Flight information lookup
  - Weather information
  - Cost calculations
  - Automatic tool binding and execution

### 2. Simple ReAct Agent (`simple_react_agent.py`)
- **Graph ID**: `simple_react_agent`
- **Description**: Simple ReAct pattern implementation converted from scratch
- **Features**:
  - Manual ReAct loop implementation
  - Action parsing with regex
  - Same travel tools as the advanced agent

## Setup Instructions

### 1. Install Dependencies
```bash
cd langgraph_studio
pip install -r requirements.txt
```

### 2. Environment Variables
Make sure you have a `.env` file in the parent directory with:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional
```

### 3. Launch LangGraph Studio
```bash
# From the langgraph_studio directory
# First, make sure you have the virtual environment activated
source ../venv/bin/activate  # or source venv/bin/activate if venv is in this directory

# Install the requirements (includes langgraph-cli)
pip install -r requirements.txt

# Launch LangGraph Studio
langgraph up
```

**Alternative Installation Method:**
If you encounter issues with `langgraph-cli`, you can install it directly:
```bash
pip install langgraph-cli
```

This will start LangGraph Studio and you can access it at `http://localhost:8123`

## Configuration Details

- **Configuration File**: `langgraph.json`
- **Environment File**: `../env` (points to the parent directory's .env file)
- **Dependencies**: Current directory (`.`) for local imports

## Available Tools

Both agents have access to these tools:

1. **get_flight_info**: Get flight duration and cost between cities
2. **get_weather**: Get current weather for a destination  
3. **calculate**: Perform mathematical calculations

## Example Queries

Try these example queries in LangGraph Studio:

1. "What's the weather like in Paris?"
2. "I want to travel from New York to London. Can you tell me the flight duration and cost, plus what's the weather like in London?"
3. "If flights from New York to Paris cost $750 each, what's the total for 2 travelers?"

## Differences Between Agents

- **Travel Agent**: Uses LangChain's built-in tool calling and automatic execution
- **Simple ReAct Agent**: Implements the ReAct pattern manually with regex parsing and explicit action loops

Both agents provide the same functionality but demonstrate different implementation approaches.