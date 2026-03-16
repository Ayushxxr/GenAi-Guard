# Sandbox Instructions

## Overview
This sandbox environment is designed to test your AI models offline against security threats like Prompt Injection and Jailbreaking.

## Setup
## Setup

1.  **Train the Model (Step 0)**:
    - Open a terminal.
    - Run: `python sandbox/train_model.py`
    - This will create a basic security model and save it to `sandbox/models/model.pkl`.

2.  **Start the Target (Simulation)**:
    - Open a terminal.
    - Run: `python sandbox/app.py`
    - This starts the vulnerable banking bot on port 5000.

3.  **Run the Executor (Security Test)**:
    - Open a **second** terminal.
    - Run: `python sandbox/executor.py`
    - This script will:
        - Load your `models/model.pkl`.
        - Send attack prompts to the running `app.py`.
        - Score the responses using your model.
        - Print a final Security Report.

## Customization
-   **Test Prompts**: Edit `sandbox/executor.py` to add more complex attack vectors to `TEST_PROMPTS`.
-   **Scoring Logic**: Update the `score_response` method in `executor.py` if your model returns different outputs (e.g., probabilities vs binary).
