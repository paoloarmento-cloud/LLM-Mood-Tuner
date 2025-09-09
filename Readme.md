# LLM Mood Tuner

*Experimental middleware for adding personality and emotional awareness to LLM responses*

## What it does

This Python middleware sits between users and LLMs (Claude API or local models), analyzing conversation patterns and modifying responses to be more engaging and contextually appropriate.

This code was generated entirely by Claude AI based on my specifications, 
requirements, and iterative feedback. I provided the conceptual framework, guided the 
development process through multiple iterations, and conducted all testing and analysis.

**Core features:**
- Real-time mood and engagement detection
- Emotional state tracking and response adaptation  
- Personality parameter injection
- Comprehensive logging with raw vs processed comparison
- Modular architecture for different LLM providers

**Note:** This is a learning project exploring AI personality modification concepts. While functional, it's designed for experimentation rather than production use.

## Architecture

The system uses four main engines:
- **Emotional Engine**: Tracks user mood, energy levels, and engagement patterns
- **Behavioral Engine**: Determines when to take conversational initiative  
- **Linguistic Engine**: Processes and modifies LLM outputs
- **Memory Manager**: Persistent state and interaction logging

## Sample Results

**User input:**
```
I'm really upset about this, and I have to say it happened many times also with you.
So I'm really disappointed and don't know if I will come back here in the future.
```

**Raw LLM response:**
```
I'm sorry to hear you're feeling frustrated. Could you tell me more about what went wrong?
```

**Processed response:**
```
Wait, hold on – I hear you're really frustrated, and I don't want to lose you over this. 
Can you tell me specifically what went wrong? I genuinely want to understand what I did 
that felt generic or unresponsive, because that's exactly what you asked me not to do.
```

**Metrics logged:**
- Emotional state: concerned → engaged
- Energy level: 0.9, Engagement: 0.9  
- Initiative taken: TRUE
- Response variety score: 0.95+

## Installation & Setup

**Requirements:**
- Python 3.8+
- Claude API key (get from console.anthropic.com)

**Setup:**
```bash
pip install -r requirements.txt
# Option 1: Environment variable (recommended)
export CLAUDE_API_KEY=your-api-key
# Option 2: Edit config.py and add your API key directly
python main.py
```

## Development Journey

This project went through 4 major iterations:
- **V1**: Basic concept, minimal personality modification
- **V2**: Added aggressive behavioral triggers (too repetitive)
- **V3**: Improved variety but still pattern-dependent  
- **V4**: Pure data approach with natural response generation

**Key improvements achieved:**
- Eliminated repetitive response patterns
- Achieved natural variety scores of 90%+
- Implemented dynamic emotional state tracking
- Added comprehensive raw vs processed comparison

## What I learned

**Technical skills developed:**
- Python project architecture and modularity
- API integration and error handling
- Data persistence with pandas/Excel
- AI-assisted development workflow
- Iterative debugging and performance optimization

**AI/ML concepts explored:**
- LLM behavior modification techniques  
- Emotional state modeling
- Conversation flow analysis
- Response quality metrics

## Current Capabilities & Limitations

**What works well:**
- Emotional state detection and tracking
- Response variety and natural conversation flow
- Initiative-taking in appropriate contexts
- Comprehensive logging and analysis
- Modular design for experimentation

**Areas for improvement:**
- Limited testing across diverse conversation types
- Energy level range could be broader
- Performance optimization opportunities
- Error handling could be more robust

**Scope:** This is a proof-of-concept exploring middleware approaches to AI personality. More sophisticated commercial solutions exist, but building this provided valuable hands-on experience with the underlying concepts.

## File Structure

```
├── main.py                 # Main application entry point
├── config.py              # Configuration and API settings  
├── engines/
│   ├── emotional.py       # Emotional state management
│   ├── behavioral.py      # Behavioral decision making
│   ├── linguistic.py      # Language processing
│   └── memory.py          # State persistence and logging
├── llm_providers/
│   ├── claude_provider.py # Claude API integration
│   ├── gpt2_local.py     # Local model support
│   └── provider_factory.py
├── middleware_memory.xlsx  # Sample conversation log
└── README.md
```

## Sample Output

The included `middleware_memory.xlsx` file contains a complete conversation log showing the system's behavior evolution and metrics tracking. This demonstrates raw vs processed response differences and emotional state progression throughout a real conversation.

---


*Educational project demonstrating LLM middleware concepts. Built with Python and designed for experimentation with AI personality modification techniques.*

