import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# -----------------------------
# DEVICE SETUP
# -----------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"


# -----------------------------
# MODEL PATHS
# -----------------------------

MODEL_PATHS = {
    "cicandmal": "models/cicandmal_model",
    "dynamic_api": "models/lora_dynamic_api",
    "static_lora": "models/lora_static_malware_dataset_malwares",
    "pdf_malware": "models/pdf_malware_lora",
    "ember_static": "models/step2_ember_part4_model",
    "obfuscated": "models/step2_obfuscated_model/final"
}


# -----------------------------
# LOAD MODELS
# -----------------------------

tokenizers = {}
models = {}

for name, path in MODEL_PATHS.items():

    print("Loading model:", name)

    tokenizers[name] = AutoTokenizer.from_pretrained(path)

    models[name] = AutoModelForSequenceClassification.from_pretrained(path)

    models[name].to(device)

    models[name].eval()

print("All models loaded successfully")


# -----------------------------
# FEATURE EXTRACTION
# -----------------------------

def extract_features(file_path):

    size = os.path.getsize(file_path)

    extension = os.path.splitext(file_path)[1]

    feature_text = f"file_size {size} extension {extension}"

    return feature_text


# -----------------------------
# SINGLE MODEL PREDICTION
# -----------------------------

def predict_with_model(model_name, text):

    tokenizer = tokenizers[model_name]

    model = models[model_name]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)

    prediction = torch.argmax(probs).item()

    confidence = torch.max(probs).item()

    return prediction, confidence


# -----------------------------
# RUN ALL MODELS
# -----------------------------

def run_all_models(text):

    results = {}

    for model_name in models:

        pred, conf = predict_with_model(model_name, text)

        results[model_name] = {
            "prediction": pred,
            "confidence": round(conf, 3)
        }

    return results


# -----------------------------
# FINAL DECISION (VOTING)
# -----------------------------

def final_decision(results):

    malware_votes = 0

    reasons = []

    for model, data in results.items():

        if data["prediction"] == 1:

            malware_votes += 1

            reasons.append(f"{model} detected suspicious behavior")

    verdict = "MALWARE" if malware_votes >= 2 else "BENIGN"

    return verdict, reasons


# -----------------------------
# MAIN FILE SCANNER
# -----------------------------

def scan_uploaded_file(file_path):

    features = extract_features(file_path)

    model_results = run_all_models(features)

    verdict, reasons = final_decision(model_results)

    return {
        "file": file_path,
        "verdict": verdict,
        "reasons": reasons,
        "model_results": model_results
    }