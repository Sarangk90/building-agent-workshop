"""
LangGraph Travel Agent for LangGraph Studio
Converted from notebooks/02_agent_using_langgraph.ipynb
"""

from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain.tools import Tool


def calculate(what: str) -> str:
    """Run a calculation"""
    try:
        result = eval(what)
        return str(result)
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


# Create LangChain tools
tools = [
    Tool(
        name="calculate",
        func=calculate,
        description="Run a calculation and return the number - useful for travel budgets, costs, etc."
    ),
    Tool(
        name="get_flight_info",
        func=get_flight_info,
        description="Get flight duration and typical cost between two cities"
    ),
    Tool(
        name="get_weather",
        func=get_weather,
        description="Get current weather information for a destination"
    )
]


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class TravelAgent:
    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}


# System prompt for the travel agent
SYSTEM_PROMPT = """
You are a helpful travel assistant that runs in a loop of Thought, Action, PAUSE, Observation.

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
""".strip()


# Create the agent instance
def create_travel_agent():
    """Factory function to create a travel agent instance"""
    model = ChatOpenAI(model="gpt-4o")
    return TravelAgent(model, tools, system=SYSTEM_PROMPT)


# For LangGraph Studio compatibility
def get_graph():
    """Return the compiled graph for LangGraph Studio"""
    agent = create_travel_agent()
    return agent.graph


# Main graph instance for LangGraph Studio
graph = get_graph()