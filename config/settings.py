import random
from tkinter import messagebox
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
# def get_response():
#     KEY = os.getenv("API_KEY")
#     model= "gemini-2.0-flash"
#     prompt = "Explain how AI works in a few words"

#     client = genai.Client(api_key=KEY)

#     response = client.models.generate_content(
#         model=model, contents=prompt
#     )
#     return response.text

def generate_scenarios_with_gemini(self):
    try:

        num_scenarios = 10
        generated_scenarios = []

        KEY = os.getenv("API_KEY")
        model_name = "gemini-2.0-flash"
        genai.configure(api_key=KEY)

        model = genai.GenerativeModel(model_name)

        for _ in range(num_scenarios):
            for is_phishing in [True, False]:
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

Only return the JSON object, nothing else."""

                response = model.generate_content(prompt)

                if response and response.text:
                    try:
                        parsed = json.loads(response.text)
                        generated_scenarios.append(parsed)
                    except json.JSONDecodeError:
                        print("Invalid JSON from Gemini:")
                        print(response.text)

        self.scenarios = generated_scenarios
        random.shuffle(self.scenarios)


        for idx, scenario in enumerate(generated_scenarios, start=1):
            print(f"\n--- Scenario {idx} ---")
            print("Email:\n", scenario.get("email", "N/A"))
            print("Is Phishing:", scenario.get("is_phishing", "N/A"))
            print("Explanation:\n", scenario.get("explanation", "N/A"))



        self.root.after(0, self.after_scenarios_loaded)

    except Exception as e:
        self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate scenarios: {str(e)}"))
        self.root.after(0, self.show_welcome_screen)