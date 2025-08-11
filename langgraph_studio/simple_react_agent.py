"""
Simple ReAct Travel Agent for LangGraph Studio
Converted from notebooks/01_agent_from_scratch.ipynb
"""

from dotenv import load_dotenv
load_dotenv()

import re
from openai import OpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage

client = OpenAI()


def calculate(what: str) -> str:
    """Run a calculation"""
    try:
        return str(eval(what))
    except Exception as e:
        return f"Error in calculation: {str(e)}"


def get_flight_info(route: str) -> str:
    """Get flight information between two cities"""
    route = route.strip()
    
    # Simple mock data for common routes
    flight_data = {
        "New York to London": "Flight duration: 7 hours, Typical cost: $600-800",
        "London to Paris": "Flight duration: 1.5 hours, Typical cost: $150-250", 
        "New York to Paris": "Flight duration: 8 hours, Typical cost: $700-900",
        "Tokyo to London": "Flight duration: 12 hours, Typical cost: $800-1200",
        "Los Angeles to Tokyo": "Flight duration: 11 hours, Typical cost: $600-1000",
        "London to New York": "Flight duration: 8 hours, Typical cost: $600-800",
        "Paris to London": "Flight duration: 1.5 hours, Typical cost: $150-250",
        "Paris to New York": "Flight duration: 8.5 hours, Typical cost: $700-900"
    }
    
    return flight_data.get(route, f"Flight information not available for {route}. Typical international flights cost $500-1000 and take 6-12 hours.")


def get_weather(city: str) -> str:
    """Get weather information for a destination"""
    city = city.strip()
    
    # Simple mock weather data
    weather_data = {
        "Paris": "Currently 18°C, partly cloudy. Good weather for sightseeing!",
        "London": "Currently 15°C, light rain. Pack an umbrella!",
        "New York": "Currently 22°C, sunny. Perfect weather for walking around the city!",
        "Tokyo": "Currently 25°C, humid. Light clothing recommended.",
        "Los Angeles": "Currently 28°C, sunny. Great beach weather!",
        "Rome": "Currently 24°C, sunny. Perfect for exploring ancient sites!",
        "Barcelona": "Currently 26°C, clear skies. Ideal for beach and city tours!"
    }
    
    return weather_data.get(city, f"Weather information not available for {city}. Check local weather services for current conditions.")


# Available actions for the ReAct agent
known_actions = {
    "calculate": calculate,
    "get_flight_info": get_flight_info,
    "get_weather": get_weather
}


class SimpleAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    max_turns: int
    current_turn: int


class SimpleReActAgent:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.action_re = re.compile(r'^Action: (\w+): (.*)$')
        
        # Create the graph
        graph = StateGraph(SimpleAgentState)
        graph.add_node("think", self.think)
        graph.add_node("act", self.act)
        graph.add_conditional_edges(
            "think",
            self.should_continue,
            {True: "act", False: END}
        )
        graph.add_edge("act", "think")
        graph.set_entry_point("think")
        self.graph = graph.compile()

    def think(self, state: SimpleAgentState):
        """Generate thoughts and actions using the LLM"""
        messages = state['messages']
        
        # Add system message if this is the first turn
        if state['current_turn'] == 0:
            messages = [SystemMessage(content=self.system_prompt)] + messages
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[{"role": msg.type, "content": msg.content} for msg in messages]
        )
        
        response = completion.choices[0].message.content
        
        return {
            'messages': [AIMessage(content=response)],
            'current_turn': state['current_turn'] + 1
        }

    def act(self, state: SimpleAgentState):
        """Execute actions found in the last message"""
        last_message = state['messages'][-1].content
        
        # Find actions in the message
        actions = [
            self.action_re.match(line.strip()) 
            for line in last_message.split('\n') 
            if self.action_re.match(line.strip())
        ]
        
        if actions:
            # Execute the first action found
            action, action_input = actions[0].groups()
            
            if action not in known_actions:
                observation = f"Unknown action: {action}. Available actions: {list(known_actions.keys())}"
            else:
                print(f" -- running {action} {action_input}")
                observation = known_actions[action](action_input)
                print(f"Observation: {observation}")
            
            # Add observation as a human message
            return {
                'messages': [HumanMessage(content=f"Observation: {observation}")]
            }
        
        return {'messages': []}

    def should_continue(self, state: SimpleAgentState):
        """Determine if we should continue the loop"""
        if state['current_turn'] >= state['max_turns']:
            return False
        
        last_message = state['messages'][-1].content
        
        # Check if there are actions to execute
        actions = [
            self.action_re.match(line.strip()) 
            for line in last_message.split('\n') 
            if self.action_re.match(line.strip())
        ]
        
        return len(actions) > 0


# System prompt for the simple ReAct agent
SIMPLE_REACT_PROMPT = """
You are a helpful travel assistant that runs in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.

Use Thought to describe your reasoning about the travel question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

get_flight_info:
e.g. get_flight_info: New York to London
Returns flight duration and typical cost between two cities

get_weather:
e.g. get_weather: Paris
Returns current weather information for a destination

calculate:
e.g. calculate: 450 * 2 + 100
Runs a calculation and returns the number - useful for travel budgets, costs, etc.

Example session:

Question: What's the weather like in Paris and how much would a flight from New York cost?
Thought: I need to get weather information for Paris and flight information from New York to Paris
Action: get_weather: Paris
PAUSE

You will be called again with this:

Observation: Currently 18°C, partly cloudy. Good weather for sightseeing!

Then continue:
Thought: Now I need to get flight information from New York to Paris
Action: get_flight_info: New York to Paris
PAUSE

You will be called again with this:

Observation: Flight duration: 8 hours, Typical cost: $700-900

You then output:

Answer: The weather in Paris is currently 18°C and partly cloudy - great for sightseeing! A flight from New York to Paris typically takes 8 hours and costs between $700-900.
""".strip()


def create_simple_react_agent():
    """Factory function to create a simple ReAct agent instance"""
    return SimpleReActAgent(SIMPLE_REACT_PROMPT)


def get_simple_graph():
    """Return the compiled graph for the simple ReAct agent"""
    agent = create_simple_react_agent()
    return agent.graph


# For LangGraph Studio - this will be the main graph
simple_graph = get_simple_graph()