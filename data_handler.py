import json
import os
import streamlit as st

PLANS_FILE = "plans.json"

def load_plans():
    if os.path.exists(PLANS_FILE):
        with open(PLANS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] # Dosya boş veya bozuksa
    return []

def save_plans(plans):
    with open(PLANS_FILE, 'w', encoding='utf-8') as f:
        json.dump(plans, f, ensure_ascii=False, indent=4)