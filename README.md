# Building AI Agents Workshop 🤖

A comprehensive 2-hour workshop on building AI agents from scratch, covering fundamental concepts and practical implementations using both custom code and LangGraph.

## 🎯 Workshop Overview

This workshop teaches you how to build intelligent agents that can reason, plan, and take actions to solve complex problems. You'll learn two approaches:

1. **Building from Scratch**: Understand the ReAct (Reasoning + Acting) pattern by implementing a simple agent
2. **Using LangGraph**: Leverage powerful frameworks to build more sophisticated agents

## 📚 Learning Objectives

By the end of this workshop, you will:
- ✅ Understand the core concepts of AI agents and the ReAct pattern
- ✅ Build a simple agent from scratch using OpenAI's API
- ✅ Implement action loops and tool integration
- ✅ Use LangGraph to create more advanced agent architectures
- ✅ Handle real-world scenarios like web search and multi-step reasoning

## 🛠️ Prerequisites

- Basic Python programming knowledge
- Familiarity with APIs and HTTP requests
- Basic understanding of Large Language Models (LLMs)

## 📋 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd building-agent-workshop
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

### 5. Get Required API Keys

#### OpenAI API Key (Required)
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create an account and generate an API key
3. Add credits to your account (minimum $5 recommended)

#### Tavily API Key (Required for Lesson 2)
1. Visit [Tavily](https://tavily.com)
2. Sign up and get your free API key
3. Free tier includes 1000 searches/month

### 6. Start Jupyter Notebook
```bash
jupyter notebook
```

## 📖 Workshop Structure

### Lesson 1: Simple ReAct Agent from Scratch (60 minutes)
**File**: `notebooks/01_agent_from_scratch.ipynb`

Learn the fundamentals by building a ReAct agent from scratch:
- Understanding the ReAct pattern (Reasoning + Acting)
- Building a basic Agent class
- Implementing tool functions (calculator, dog weight lookup)
- Creating action loops and observation handling

### Lesson 2: Advanced Agents with LangGraph (60 minutes)
**File**: `notebooks/02_agent_using_langgraph.ipynb`

Build sophisticated agents using the LangGraph framework:
- Introduction to LangGraph components
- StateGraph and node management
- Tool binding and function calling
- Real-world web search integration

## 🎯 Workshop Timeline

| Time | Activity | Duration |
|------|----------|----------|
| 0:00-0:10 | Setup & Introduction | 10 min |
| 0:10-1:10 | Lesson 1: Agent from Scratch | 60 min |
| 1:10-1:20 | Break | 10 min |
| 1:20-2:20 | Lesson 2: LangGraph Agents | 60 min |

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your `.env` file is in the project root
   - Check that API keys are valid and have sufficient credits
   - Restart Jupyter after adding environment variables

2. **Package Installation Issues**
   - Use a fresh virtual environment
   - Upgrade pip: `pip install --upgrade pip`
   - Install packages one by one if bulk install fails

3. **Notebook Not Starting**
   - Ensure virtual environment is activated
   - Try: `python -m jupyter notebook`
   - Check if port 8888 is available

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

---

**Happy Building! 🚀**