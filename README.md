# SaaS Migration AI Assistant

An AI-powered assistant designed to help with SaaS migration workflows. This project uses an agent-based architecture with memory, policies, and tools, and integrates with the Gemini API.

## Project Architecture

```
project/
├── main.py                # Entry point of the application
├── interface.py           # UI / interface logic
├── checkmodels.py         # Utility script to check available/running AI models (not used in final execution)
│
├── agent/
│   ├── agent.py           # Core agent logic
│   ├── tools.py           # API key and model configuration
│   ├── memory.py          # Agent memory handling
│   └── policies.py        # Decision-making policies
│
├── data/
│   ├── memory.json        # Persistent agent memory
│   └── tickets.json       # Sample / input ticket data
│
├── requirements.txt       # Python dependencies
└── README.md
```

---

## Important Notes

* **`checkmodels.py`** is **not required for final execution**. It is only used to verify the currently running AI model or API.
* You must **replace the API key and model name in ****`agent/tools.py`** before running the project.
* If you are unsure which model name to use, run `checkmodels.py`.

---

## Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

Additional required libraries (already included in `requirements.txt`, but listed here for clarity):

```bash
pip install google-generativeai
pip install streamlit
```

---

## Configuration

1. Open `agent/tools.py`.
2. Add your **Gemini API key**.
3. Specify the **model name**.

Example (illustrative only):

```python
API_KEY = "your_api_key_here"
MODEL_NAME = "gemini-1.5-pro"
```

If you are unsure about the model name, run:

```bash
python checkmodels.py
```

---

## How to Run the Project

### Step-by-step

1. Create a folder named `project` and place all files inside it following the architecture shown above.
2. Open **Command Prompt / Terminal** and navigate to the project directory.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Add your API key and model name in `agent/tools.py`.
5. (Optional) Run `checkmodels.py` to verify the model name.
6. Run the main application:

   ```bash
   python main.py
   ```

🎉 **YIPPEEE! The SaaS Migration AI Assistant is now running.**

---

## Summary

* Agent-based architecture
* Persistent memory using JSON
* Gemini API integration
* Modular and extensible design

This setup is ideal for experimenting with agentic AI workflows in SaaS migration scenarios.
