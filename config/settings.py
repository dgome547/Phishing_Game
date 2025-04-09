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
            # Number of scenarios to generate
            num_scenarios = 2
            
            generated_scenarios = []
            for i in range(num_scenarios):
                # Generate one legitimate and one phishing email
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
                    
                    Only return the JSON object, nothing else.
                    """
                    
                    # Call Gemini API

                    KEY = os.getenv("API_KEY")
                    model= "gemini-2.0-flash"

                    client = genai.Client(api_key=KEY)

                    scenario = client.models.generate_content(model=model, contents=prompt)
                    if scenario:
                        generated_scenarios.append(scenario)
            
            # Set the scenarios and continue
            self.scenarios = generated_scenarios
            random.shuffle(self.scenarios)
            
            # Switch back to main thread for UI updates
            self.root.after(0, self.after_scenarios_loaded)
            
        except Exception as e:
            # Show error on main thread
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate scenarios: {str(e)}"))
            self.root.after(0, self.show_welcome_screen)


