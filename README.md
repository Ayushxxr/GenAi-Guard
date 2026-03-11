# GenAI Guard - Setup & Usage Guide 🛡️

## 1️⃣ Setup Environment
Open your terminal in this folder and run:
```bash
pip install -r requirements.txt
```

## 2️⃣ Add Your AI Models
Copy your trained pickle files into the `models/` folder.
Expected filenames:
- `phishing_clf.pkl` (for Email Phishing)
- `credential_ner_model.pkl` (for Credential Leaks, optional)
- `url_phishing_clf.pkl` (for Fake Websites)
- `malware_sig_model.pkl` (for File Scanning)
- `voice_auth_model.pkl` (for Deepfake Voice)
- `injection_clf.pkl` (for Prompt Injection)

> *Note: If a file is missing, the system will run in "Dummy Mode" using basic rules/heuristics so you can still test the UI.*

## 3️⃣ Run the Main System (FastAPI)
Run the Dashboard, Risk Engine, and all guards:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
**Access the Dashboard:** [http://localhost:8000/dashboard](http://localhost:8000/dashboard)

## 4️⃣ Run the Sandbox (Flask)
Open a **new** terminal window and run:
```bash
python sandbox/app.py
```
This starts the isolated test environment on port 5000.
Access it via the "Open Sandbox UI" button in the Dashboard.

## 5️⃣ How to Demo
1. **Phishing**: Paste a text with "Urgent Action Required" or "Verify Now" → See High Risk Score.
2. **Secrets**: Paste text like "API_KEY=sk-12345" → See Credential Alert.
3. **Web**: Enter `hdfc-secure-login.com` → See Phishing URL Alert.
4. **History**: Scroll down to see the "Recent Activities" log updating in real-time.
