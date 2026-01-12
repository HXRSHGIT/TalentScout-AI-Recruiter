# 🚀 TalentScout: AI-Powered Hiring Assistant

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red) ![LLM](https://img.shields.io/badge/AI-GPT--4o%20%7C%20Llama3-green) ![Status](https://img.shields.io/badge/Status-Completed-success)

## 📄 Overview
**TalentScout** is an intelligent conversational agent designed to revolutionize the technical recruitment process. Unlike static forms, this AI-driven assistant engages candidates in a dynamic dialogue, parsing their technical stack in real-time and generating bespoke technical assessments on the fly. 

Developed as part of the **PG-AGI AI/ML Intern Assignment**, this project leverages Large Language Models (LLMs) to automate candidate screening, ensuring a seamless, context-aware interaction that evaluates both technical proficiency and behavioral cues.

---

## ✨ Key Features

### 🧠 Core Functionalities
* **Intelligent Information Extraction:** Utilizes NLP to extract entities (Name, Email, Experience, Location) from natural conversation flow rather than rigid input fields.
* **Dynamic Tech Stack Parsing:** Automatically identifies and categorizes programming languages, frameworks, and tools declared by the candidate.
* **Context-Aware Question Generation:** The core engine generates **3-5 tailored technical questions** based specifically on the candidate's declared stack, moving beyond generic question banks.
* **Conversation State Management:** Maintains context throughout the interaction to handle follow-up queries and ensure a coherent flow.

### 🚀 Advanced Modules ("What's New")
To elevate the platform beyond a basic screener, the following advanced modules were engineered:

* **Mock Interview Simulation Mode:**
    * **Logic:** Uses recursive prompting to engage candidates in a deep-dive technical dialogue.
    * **Benefit:** Simulates high-pressure scenarios and provides immediate feedback on answer quality.
    
* **Gap Analysis & Roadmap Mode:**
    * **Logic:** Performs a semantic comparison between the candidate's current skills and the ideal profile for the role.
    * **Benefit:** Generates a personalized learning roadmap, turning the screening process into a value-add upskilling opportunity for the candidate.

* **Human-in-the-Loop (HITL) Profile Update:**
    * **Logic:** A dedicated interface allowing candidates to manually mutate the JSON state of their parsed profile.
    * **Benefit:** Ensures data accuracy by giving users final sign-off on AI-parsed information.

* **Real-Time Sentiment Analysis:**
    * **Logic:** Specific background processes analyze the emotional tone of responses.
    * **Benefit:** Provides recruiters with "Soft Skill Metrics" regarding candidate confidence and attitude.

* **Multilingual Support:**
    * **Logic:** Auto-detects input language and responds in the candidate's native tongue while logging English translations for the recruiter.

---

## 🛠️ Technical Architecture

* **Frontend:** Built with **Streamlit** for a reactive, component-based UI.
* **Orchestration:** Python-based backend handling API calls, session state, and logic routing.
* **AI Engine:** Integration with **[Insert Model: e.g., OpenAI GPT-4 / Llama 3]** for NLU (Natural Language Understanding) and NLG (Natural Language Generation).
* **Prompt Engineering:** Utilizes **Few-Shot Prompting** and **Chain-of-Thought (CoT)** reasoning to ensure the model
