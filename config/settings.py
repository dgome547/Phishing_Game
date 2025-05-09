import random
from tkinter import messagebox
from google import genai
from dotenv import load_dotenv
import os
import json
import time
import re

load_dotenv()


def generate_scenarios(n=2):
    KEY = os.getenv("API_KEY")
    model = "gemini-2.0-flash"
    client = genai.Client(api_key=KEY)

    scenarios = []
    

    for i in range(n):
        is_phishing = (i % 2 == 0)
        scenario_type = "phishing" if is_phishing else "legitimate"

        prompt = f"""Generate a realistic {scenario_type} email scenario for a phishing awareness training game.

The email should {'have clear phishing indicators' if is_phishing else 'be completely legitimate'}.

Return your response in JSON format with the following structure:
{{
  "email": "The full email content with From, Subject, and Body",
  "is_phishing": {"true" if is_phishing else "false"},
  "explanation": "A detailed explanation of why this is {'a phishing attempt' if is_phishing else 'legitimate'}, pointing out specific elements."
}}

{'Include typical phishing red flags like suspicious sender address, urgent language, suspicious links, grammar errors, or requests for sensitive information.' if is_phishing else 'Make it look like a genuine email from a real company with proper formatting, no suspicious elements, and realistic content.'}


Do not use Markdown formatting in the output. Return plain JSON only.
"""

        try:
            response = client.models.generate_content(model=model, contents=prompt)
            print(f"Raw response for iteration {i+1}:\n{response.text}\n")
            try:
                raw = response.text.strip()
                json_str = re.search(r'\{.*\}', raw, re.DOTALL).group()
                parsed = json.loads(json_str)
            except Exception as e:
                print(f"Error parsing JSON in iteration {i+1}: {e}")
                continue

            # Flatten email field if it's a dictionary
            if isinstance(parsed.get("email"), dict):
                email_data = parsed["email"]
                parsed["email"] = f"From: {email_data.get('From', '')}\nSubject: {email_data.get('Subject', '')}\n\n{email_data.get('Body', '')}"

            scenarios.append(parsed)

        except Exception as e:
            print(f"Error on iteration {i+1}: {e}")

        # SLEEP PREVENTS TIMEOUT FROM GOOGLE THEY DONT LIKE SPAM
        time.sleep(2)

    return scenarios

