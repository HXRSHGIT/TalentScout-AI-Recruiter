🚀 TalentScout: AI-Powered Hiring Assistant
📄 Overview
TalentScout is an intelligent conversational agent designed to revolutionize the technical recruitment process. Unlike static forms, this AI-driven assistant engages candidates in a dynamic dialogue, parsing their technical stack in real-time and generating bespoke technical assessments on the fly.

Developed as part of the PG-AGI AI/ML Intern Assignment, this project leverages Large Language Models (LLMs) to automate candidate screening, ensuring a seamless, context-aware interaction that evaluates both technical proficiency and behavioral cues.

✨ Key Features
🧠 Core Functionalities

Intelligent Information Extraction: utilizes NLP to extract entities (Name, Email, Experience, Location) from natural conversation flow rather than rigid input fields.
+1


Dynamic Tech Stack Parsing: Automatically identifies and categorizes programming languages, frameworks, and tools declared by the candidate.


Context-Aware Question Generation: The core engine generates 3-5 tailored technical questions based specifically on the candidate's declared stack, moving beyond generic question banks.
+1


Conversation State Management: Maintains context throughout the interaction to handle follow-up queries and ensure a coherent flow.

🚀 Advanced Modules ("What's New")
To elevate the platform beyond a basic screener, the following advanced modules were engineered:

Mock Interview Simulation Mode:

Logic: Uses recursive prompting to engage candidates in a deep-dive technical dialogue.

Benefit: Simulates high-pressure scenarios and provides immediate feedback on answer quality.

Gap Analysis & Roadmap Mode:

Logic: Performs a semantic comparison between the candidate's current skills and the ideal profile for the role.

Benefit: Generates a personalized learning roadmap, turning the screening process into a value-add upskilling opportunity for the candidate.

Human-in-the-Loop (HITL) Profile Update:

Logic: A dedicated interface allowing candidates to manually mutate the JSON state of their parsed profile.

Benefit: Ensures data accuracy by giving users final sign-off on AI-parsed information.

Real-Time Sentiment Analysis:

Logic: specific background processes analyze the emotional tone of responses.

Benefit: Provides recruiters with "Soft Skill Metrics" regarding candidate confidence and attitude.

Multilingual Support:

Logic: Auto-detects input language and responds in the candidate's native tongue while logging English translations for the recruiter.

🛠️ Technical Architecture

Frontend: Built with Streamlit for a reactive, component-based UI.
+1


Orchestration: Python-based backend handling API calls, session state, and logic routing.


AI Engine: Integration with [Insert Model: e.g., OpenAI GPT-4 / Llama 3] for NLU (Natural Language Understanding) and NLG (Natural Language Generation).


Prompt Engineering: Utilizes Few-Shot Prompting and Chain-of-Thought (CoT) reasoning to ensure the model acts as a "Senior Technical Recruiter".


Data Privacy: Implements simulated data handling to mask PII (Personally Identifiable Information) in compliance with GDPR best practices.

💻 Installation & Local Execution Guide
Follow these steps to set up the project on your local machine.

Prerequisites
Python 3.8 or higher installed.

Git installed.

An API Key for the LLM provider (e.g., OpenAI API Key or Groq/Llama API Key).

Step 1: Clone the Repository
Open your terminal and run:

Bash

git clone <YOUR_REPOSITORY_LINK>
cd TalentScout-Hiring-Assistant
Step 2: Create a Virtual Environment (Recommended)
It is best practice to run Python projects in an isolated environment.

Bash

# For Windows
python -m venv venv
venv\Scripts\activate

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
Install the required libraries listed in requirements.txt:

Bash

pip install -r requirements.txt
Step 4: Configure Environment Variables
Create a file named .env in the root directory. Add your API key inside:

Ini, TOML

OPENAI_API_KEY="your_api_key_here"
# OR if using another model
GROQ_API_KEY="your_api_key_here"
Step 5: Run the Application
Launch the Streamlit server:

Bash

streamlit run src/app.py
Step 6: Access the Interface
Once the command runs, your default browser should open automatically to: http://localhost:8501

🛡️ Challenges & Solutions
Hallucinations: The LLM initially invented non-existent Python libraries. Solution: Implemented negative constraints in the system prompt to restrict knowledge to verifiable tech stacks.

Context Loss: Long conversations led to token limit issues. Solution: Implemented a rolling window buffer to keep only the most relevant recent interactions in the active prompt.

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements.


Submission for PG-AGI AI/ML Intern Assignment
