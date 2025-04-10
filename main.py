import os
import time
import random
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import threading
import re
import requests
from PIL import Image, ImageTk
import io
import base64


class PhishingGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Phishing Awareness Training Game")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Game state variables
        self.player_name = ""
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_time = 0
        self.leaderboard = []
        self.training_mode = False
        self.scenario_index = 0
        self.scenarios = []
        self.current_scenario = None
        self.start_time = 0
        self.timer_running = False
        self.timer_value = 0
        self.use_gemini = False
        self.gemini_api_key = ""
        
        # Create widgets
        self.create_widgets()
        self.load_leaderboard()
        self.show_welcome_screen()
    
    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Game content frame
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Timer label
        self.timer_label = ttk.Label(self.main_frame, text="Time: 0s", font=("Helvetica", 12))
        self.timer_label.pack(anchor=tk.NE, padx=10, pady=5)
        
        # Status frame for score and progress
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        # Score label
        self.score_label = ttk.Label(self.status_frame, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Progress label
        self.progress_label = ttk.Label(self.status_frame, text="Progress: 0/0", font=("Helvetica", 12))
        self.progress_label.pack(side=tk.RIGHT, padx=10)
    
    def load_leaderboard(self):
        try:
            if os.path.exists("data/leaderboard.json"):
                with open("data/leaderboard.json", "r") as file:
                    self.leaderboard = json.load(file)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            self.leaderboard = []
    
    def save_leaderboard(self):
        try:
            os.makedirs("data", exist_ok=True)  # Ensure 'data/' exists
            with open("data/leaderboard.json", "w") as file:
                json.dump(self.leaderboard, file)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
    
    def add_to_leaderboard(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            "name": self.player_name,
            "score": self.score,
            "correct": self.correct_answers,
            "incorrect": self.incorrect_answers,
            "avg_time": round(self.total_time / max(1, (self.correct_answers + self.incorrect_answers)), 2),
            "timestamp": timestamp
        }
        self.leaderboard.append(result)
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.save_leaderboard()
    
    def display_leaderboard(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        leaderboard_frame = ttk.Frame(self.content_frame)
        leaderboard_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Leaderboard header
        ttk.Label(leaderboard_frame, text="LEADERBOARD", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Create treeview for leaderboard display
        columns = ("Rank", "Name", "Score", "Correct", "Incorrect", "Avg Time", "Date")
        tree = ttk.Treeview(leaderboard_frame, columns=columns, show="headings", height=10)
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            width = 80 if col == "Name" else 60
            tree.column(col, width=width, anchor=tk.CENTER)
        
        # Insert leaderboard data
        if not self.leaderboard:
            tree.insert("", tk.END, values=("--", "No records yet", "--", "--", "--", "--", "--"))
        else:
            for i, entry in enumerate(self.leaderboard[:10], 1):
                tree.insert("", tk.END, values=(
                    i,
                    entry["name"],
                    entry["score"],
                    entry["correct"],
                    entry["incorrect"],
                    f"{entry['avg_time']}s",
                    entry.get("timestamp", "N/A")
                ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button to return to main menu
        ttk.Button(leaderboard_frame, text="Back to Main Menu", command=self.show_welcome_screen).pack(pady=10)
    
    def show_welcome_screen(self):
        # Reset game state
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_time = 0
        self.scenario_index = 0
        self.timer_running = False
        
        # Update labels
        self.score_label.config(text="Score: 0")
        self.progress_label.config(text="Progress: 0/0")
        self.timer_label.config(text="Time: 0s")
        
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Welcome frame
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Logo/Title
        title_label = ttk.Label(welcome_frame, text="PHISHING AWARENESS\nTRAINING GAME", 
                               font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(welcome_frame, 
                                  text="Test your skills at identifying phishing attempts!",
                                  font=("Helvetica", 12))
        subtitle_label.pack(pady=10)
        
        # Player name input
        name_frame = ttk.Frame(welcome_frame)
        name_frame.pack(pady=20)
        
        ttk.Label(name_frame, text="Enter your name:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(name_frame, width=30, font=("Helvetica", 12))
        self.name_entry.pack(side=tk.LEFT, padx=5)
        if self.player_name:
            self.name_entry.insert(0, self.player_name)
        
        # Scenario source options
        source_frame = ttk.Frame(welcome_frame)
        source_frame.pack(pady=10)
        
        self.scenario_source = tk.StringVar(value="premade")
        ttk.Label(source_frame, text="Scenario Source:", font=("Helvetica", 12)).pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(source_frame, text="Use Premade Scenarios", variable=self.scenario_source, 
                       value="premade").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(source_frame, text="Generate with Gemini API", variable=self.scenario_source, 
                       value="gemini").pack(anchor=tk.W, padx=20)
        
        # API Key input
        api_frame = ttk.Frame(welcome_frame)
        api_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(api_frame, text="Gemini API Key (if using Gemini):", font=("Helvetica", 12)).pack(anchor=tk.W, pady=5)
        self.api_entry = ttk.Entry(api_frame, width=40, font=("Helvetica", 12))
        self.api_entry.pack(anchor=tk.W, padx=20, fill=tk.X)
        if self.gemini_api_key:
            self.api_entry.insert(0, self.gemini_api_key)
        
        # Training mode option
        training_frame = ttk.Frame(welcome_frame)
        training_frame.pack(pady=10)
        
        self.training_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(training_frame, text="Enable Training Mode (with detailed explanations)", 
                       variable=self.training_var).pack(pady=5)
        
        # Button frame
        button_frame = ttk.Frame(welcome_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Start Game", command=self.start_game, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="View Leaderboard", command=self.display_leaderboard, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy, width=20).pack(side=tk.LEFT, padx=10)
    
    def start_game(self):
        # Validate name
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Missing Name", "Please enter your name to continue.")
            return
        
        # Check for API key if using Gemini
        self.use_gemini = (self.scenario_source.get() == "gemini")
        if self.use_gemini:
            self.gemini_api_key = self.api_entry.get().strip()
            if not self.gemini_api_key:
                messagebox.showwarning("Missing API Key", "Please enter a Gemini API key to use Gemini for scenarios.")
                return
        
        # Set training mode
        self.training_mode = self.training_var.get()
        
        # Initialize game
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_time = 0
        self.scenario_index = 0
        
        # Update labels
        self.score_label.config(text="Score: 0")
        
        # Load scenarios
        if self.use_gemini:
            # Show loading screen while generating scenarios
            self.show_loading_screen("Generating scenarios with Gemini API...")
            threading.Thread(target=self.generate_scenarios_with_gemini).start()
        else:
            self.scenarios = self.get_premade_scenarios()
            random.shuffle(self.scenarios)
            self.progress_label.config(text=f"Progress: 0/{len(self.scenarios)}")
            
            # If training mode is enabled, show training intro
            if self.training_mode:
                self.show_training_intro()
            else:
                self.display_next_scenario()
    
    def show_loading_screen(self, message):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        loading_frame = ttk.Frame(self.content_frame)
        loading_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        ttk.Label(loading_frame, text=message, font=("Helvetica", 14)).pack(pady=20)
        
        # Create a progress bar
        progress = ttk.Progressbar(loading_frame, mode="indeterminate", length=300)
        progress.pack(pady=20)
        progress.start()
        
        # Force update to show loading screen
        self.root.update()
    
    def generate_scenarios_with_gemini(self):
        try:
            # Number of scenarios to generate
            num_scenarios = 10
            
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
                    scenario = self.call_gemini_api(prompt)
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
    
    def after_scenarios_loaded(self):
        self.progress_label.config(text=f"Progress: 0/{len(self.scenarios)}")
        
        # If training mode is enabled, show training intro
        if self.training_mode:
            self.show_training_intro()
        else:
            self.display_next_scenario()
    
    def call_gemini_api(self, prompt):
        # Gemini API endpoint
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"
        
        # Request headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Request data
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        # Add API key as query parameter
        params = {
            "key": self.gemini_api_key
        }
        
        # Make the request
        response = requests.post(url, headers=headers, json=data, params=params)
        
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            
            # Extract text from the response
            if "candidates" in result and len(result["candidates"]) > 0:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                
                # Extract JSON from text using regex
                match = re.search(r'({.*})', text.replace('\n', ' '), re.DOTALL)
                if match:
                    try:
                        scenario_json = json.loads(match.group(1))
                        # Validate JSON structure
                        if all(key in scenario_json for key in ["email", "is_phishing", "explanation"]):
                            return scenario_json
                    except json.JSONDecodeError:
                        pass
            
            raise Exception(f"Failed to parse Gemini response: {response.text}")
        else:
            raise Exception(f"Gemini API request failed with status code {response.status_code}: {response.text}")
    
    def show_training_intro(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        training_frame = ttk.Frame(self.content_frame)
        training_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Training title
        ttk.Label(training_frame, text="TRAINING MODE", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Training content
        training_text = """Before we start the game, let's review some key indicators of phishing emails:

1. Suspicious sender addresses (e.g., misspelled domain names)
2. Urgent requests or threats
3. Grammar and spelling errors
4. Suspicious links (hover to check before clicking)
5. Requests for personal information
6. Unexpected attachments
7. Generic greetings like "Dear Customer"
8. Offers that seem too good to be true

In training mode, we'll analyze each scenario together before you make your decision."""
        
        training_content = scrolledtext.ScrolledText(training_frame, wrap=tk.WORD, width=60, height=15, font=("Helvetica", 12))
        training_content.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        training_content.insert(tk.END, training_text)
        training_content.config(state=tk.DISABLED)
        
        # Button to start
        ttk.Button(training_frame, text="Start Training", command=self.display_next_scenario).pack(pady=20)
    
    def get_premade_scenarios(self):
        scenarios = [
            {
                "email": """From: service@amaz0n.com
Subject: Urgent: Your Account Has Been Compromised
                
Dear Valued Customer,
                
We have detected suspicious activity on your account. Your account has been temporarily suspended.
                
Please click the link below to verify your information and restore your account:
http://amazonn-secure.com/verify
                
If you don't respond within 24 hours, your account will be permanently closed.
                
Amazon Security Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email contains a zero instead of an 'o' (amaz0n.com)
2. The link domain is misspelled (amazonn-secure.com)
3. The message creates urgency with threats of account closure
4. It asks you to click a suspicious link
5. It doesn't address you by name"""
            },
            {
                "email": """From: newsletter@spotify.com
Subject: Your Monthly Spotify Recap
                
Hi there,
                
Here's your monthly listening summary:
- You listened to 427 minutes of music this month
- Your top artist was The Weeknd
- Your favorite genre was Pop
                
Check out your personalized playlist based on your listening habits:
https://open.spotify.com/playlist/recommendations
                
Enjoy the music!
The Spotify Team""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (spotify.com)
2. The content is personalized based on your listening habits
3. The link goes to the official Spotify domain
4. There's no urgency or threats
5. It doesn't ask for personal information"""
            },
            {
                "email": """From: paypal-security@paypal-team.com
Subject: PayPal: Confirm Your Recent Transaction
                
Dear PayPal User,
                
We've detected a unusual transaction on your account for $750.00 to "Online Electronics Store".
                
If you did not make this transaction, you must immediate verify your account details by clicking the link below:
                
https://paypal-secure-center.com/verify
                
Your account will be locked if you do not respond within 12 hours.
                
Security Department
PayPal""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from the official PayPal domain (paypal.com)
2. The domain "paypal-team.com" is suspicious
3. The verification link goes to an unofficial website
4. There are grammar errors ("a unusual transaction", "immediate verify")
5. The message creates urgency with a time limit
6. It doesn't address you by name"""
            },
            {
                "email": """From: no-reply@linkedin.com
Subject: John Smith has sent you a connection request
                
LinkedIn
                
John Smith has sent you a connection request
                
I'd like to add you to my professional network on LinkedIn.
- John Smith, Senior Developer at Tech Solutions Inc.
                
[View profile]
                
You are receiving connection requests emails. Unsubscribe here.
                
© 2023 LinkedIn Corporation, 1000 W Maude Ave, Sunnyvale, CA 94085.""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (linkedin.com)
2. The format matches standard LinkedIn connection requests
3. The message is specific about who sent the request
4. It includes a normal LinkedIn footer with unsubscribe option
5. There's no urgency or threats
6. It doesn't ask for sensitive information"""
            },
            {
                "email": """From: microsoftsupport@outlook-team.com
Subject: Your Microsoft 365 subscription is expiring
                
MICROSOFT 365
                
Dear Customer,
                
Your Microsoft 365 subscription will expire in 2 days. To ensure no disruption to your service, please update your payment details urgently.
                
Click here to update your payment information: https://microsoft365-renewal.com
                
Note: Failure to update will result in immediate service termination.
                
Microsoft Support Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Microsoft's official domain
2. The domain "outlook-team.com" is suspicious
3. The link goes to an unofficial website
4. The message creates urgency
5. It doesn't address you by name
6. Microsoft typically sends subscription reminders well in advance"""
            },
            {
                "email": """From: noreply@netflix.com
Subject: Your Netflix bill
                
Your monthly Netflix subscription has been processed.
                
Billing date: April 3, 2023
Amount: $14.99
Next billing date: May 3, 2023
                
To view your receipt, visit netflix.com/YourAccount
                
Questions? Visit the Help Center: help.netflix.com
                
Netflix""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (netflix.com)
2. It's a standard billing notification with specific details
3. The message directs you to the official Netflix website
4. There's no urgency or threats
5. It doesn't ask you to click suspicious links
6. It offers legitimate help resources"""
            },
            {
                "email": """From: support@applesecure.net
Subject: Apple ID: Your account has been locked
                
Dear Customer,
                
Your Apple ID has been locked due to too many failed login attempts.
                
To unlock your account, please verify your information by clicking on the link below:
                
https://apple-id-unlock.com/verify
                
If you don't verify within 24 hours, your account will be permanently deleted.
                
Apple Support""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Apple's official domain (apple.com)
2. The domain "applesecure.net" is suspicious
3. The verification link goes to an unofficial website
4. The message creates urgency with threats of account deletion
5. It doesn't address you by name
6. Apple never threatens to delete accounts in this manner"""
            },
            {
                "email": """From: billing@amazon.com
Subject: Your Amazon.com order #112-7366937-2795436
                
Hello Rachel,
                
Thank you for your order. Your Amazon.com order #112-7366937-2795436 has shipped.
                
Your package was sent to:
Rachel Johnson
123 Main Street
Springfield, IL 62704
                
You can track your package at: amazon.com/your-orders
                
Order Details:
1x Book: "The Psychology of Money" - $15.99
                
Thank you for shopping with us.
Amazon.com""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (amazon.com)
2. It includes specific order details with a genuine-looking order number
3. It addresses the recipient by name
4. The tracking link directs to the official Amazon website
5. The message is informational with no urgency or threats
6. It doesn't ask for sensitive information"""
            },
            {
                "email": """From: service@bankofamerica-secure.com
Subject: URGENT: Unusual activity detected on your account
                
BANK OF AMERICA
                
Dear Client,
                
We have detected unusual activity on your account. For your security, we have limited access to your online banking.
                
CLICK HERE TO VERIFY YOUR IDENTITY AND RESTORE ACCESS
                
If we don't hear from you within 24 hours, your account will remain restricted.
                
Bank of America Security Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Bank of America's official domain
2. The domain "bankofamerica-secure.com" is suspicious
3. The "CLICK HERE" doesn't show the actual URL
4. The message creates urgency with threats of continued restriction
5. It doesn't address you by name
6. Banks typically don't send emails with "CLICK HERE" buttons for security issues"""
            },
            {
                "email": """From: no-reply@dropbox.com
Subject: John shared "Project Proposal" with you
                
Dropbox
                
John Smith (john.smith@company.com) shared "Project Proposal" with you
                
View file
                
The link to view this file will expire in 30 days.
                
Need help? Visit the Dropbox Help Center.
                
© 2023 Dropbox""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (dropbox.com)
2. The format matches standard Dropbox file sharing notifications
3. It includes specific details about who shared what
4. It mentions a reasonable expiration period for the link
5. It directs to legitimate help resources
6. There's no urgency or threats"""
            }
        ]
        return scenarios
    
    def display_next_scenario(self):
        if self.scenario_index >= len(self.scenarios):
            self.show_game_results()
            return
        
        self.current_scenario = self.scenarios[self.scenario_index]
        
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        scenario_frame = ttk.Frame(self.content_frame)
        scenario_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scenario heading
        ttk.Label(scenario_frame, text=f"Scenario {self.scenario_index + 1}/{len(self.scenarios)}", 
                 font=("Helvetica", 14, "bold")).pack(pady=10)
        
        # Email content
        email_frame = ttk.LabelFrame(scenario_frame, text="Email", padding=10)
        email_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        email_content = scrolledtext.ScrolledText(email_frame, wrap=tk.WORD, width=70, height=15, font=("Courier", 11))
        email_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        email_content.insert(tk.END, self.current_scenario["email"])
        email_content.config(state=tk.DISABLED)
        
        # If training mode, show explanation first
        if self.training_mode:
            explanation_frame = ttk.LabelFrame(scenario_frame, text="Analysis", padding=10)
            explanation_frame.pack(fill=tk.X, padx=20, pady=10)
            
            explanation_text = scrolledtext.ScrolledText(explanation_frame, wrap=tk.WORD, width=70, height=8, font=("Helvetica", 11))
            explanation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            explanation_text.insert(tk.END, self.current_scenario["explanation"])
            explanation_text.config(state=tk.DISABLED)
            
            ttk.Label(scenario_frame, text="Now, make your decision:", font=("Helvetica", 12)).pack(pady=5)
        
        # Decision buttons
        button_frame = ttk.Frame(scenario_frame)
        button_frame.pack(pady=20)
        
        # Button styling
        style = ttk.Style()
        style.configure("Green.TButton", background="green")
        style.configure("Red.TButton", background="red")
        
        legitimate_btn = ttk.Button(button_frame, text="Legitimate Email", 
                                  command=lambda: self.make_decision("L"), width=20)
        legitimate_btn.pack(side=tk.LEFT, padx=10)
        
        phishing_btn = ttk.Button(button_frame, text="Phishing Attempt", 
                                 command=lambda: self.make_decision("P"), width=20)
        phishing_btn.pack(side=tk.LEFT, padx=10)
        
        # Start the timer
        self.start_time = time.time()
        self.timer_running = True
        self.timer_value = 0
        self.update_timer()
        
        # Update progress label
        self.progress_label.config(text=f"Progress: {self.scenario_index + 1}/{len(self.scenarios)}")
    
    def update_timer(self):
        if self.timer_running:
            elapsed = time.time() - self.start_time
            self.timer_value = elapsed
            self.timer_label.config(text=f"Time: {elapsed:.1f}s")
            self.root.after(100, self.update_timer)
    
    def make_decision(self, choice):
        # Stop the timer
        self.timer_running = False
        time_taken = self.timer_value
        self.total_time += time_taken


    def make_decision(self, choice):
            # Stop the timer
            self.timer_running = False
            time_taken = self.timer_value
            self.total_time += time_taken
            
            # Check if the decision is correct
            is_phishing = self.current_scenario["is_phishing"]
            is_correct = (choice == 'P' and is_phishing) or (choice == 'L' and not is_phishing)
            
            # Calculate score
            score_earned = self.calculate_score(is_correct, time_taken)
            self.score += score_earned
            
            # Update stats
            if is_correct:
                self.correct_answers += 1
            else:
                self.incorrect_answers += 1
            
            # Update score label
            self.score_label.config(text=f"Score: {self.score}")
            
            # Show feedback
            self.show_feedback(is_correct, time_taken, score_earned)
        
    def calculate_score(self, is_correct, time_taken):
        # Base score
        base_score = 100 if is_correct else 0
        
        # Time bonus - faster correct answers get more points
        # Max bonus of 50 points for answering in under 15 seconds
        time_bonus = 0
        if is_correct:
            if time_taken < 15:
                time_bonus = 50
            elif time_taken < 30:
                time_bonus = 30
            elif time_taken < 45:
                time_bonus = 15
        
        return base_score + time_bonus

    def show_feedback(self, is_correct, time_taken, score_earned):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        feedback_frame = ttk.Frame(self.content_frame)
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Result heading
        if is_correct:
            result_text = "✓ CORRECT!"
            result_color = "green"
        else:
            result_text = "✗ INCORRECT!"
            result_color = "red"
        
        result_label = ttk.Label(feedback_frame, text=result_text, font=("Helvetica", 20, "bold"))
        result_label.pack(pady=10)
        
        # Score and time info
        if is_correct:
            ttk.Label(feedback_frame, text=f"You earned {score_earned} points!", 
                        font=("Helvetica", 14)).pack(pady=5)
        ttk.Label(feedback_frame, text=f"Time taken: {time_taken:.2f} seconds", 
                    font=("Helvetica", 12)).pack(pady=5)
        
        # Explanation
        explanation_frame = ttk.LabelFrame(feedback_frame, text="Explanation", padding=10)
        explanation_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        explanation_text = scrolledtext.ScrolledText(explanation_frame, wrap=tk.WORD, 
                                                    width=70, height=10, font=("Helvetica", 11))
        explanation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        explanation_text.insert(tk.END, self.current_scenario["explanation"])
        explanation_text.config(state=tk.DISABLED)
        
        # Email recap
        email_frame = ttk.LabelFrame(feedback_frame, text="Email Recap", padding=10)
        email_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        email_content = scrolledtext.ScrolledText(email_frame, wrap=tk.WORD, 
                                                width=70, height=6, font=("Courier", 10))
        email_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Just show the From and Subject lines for recap
        email_lines = self.current_scenario["email"].strip().split("\n")
        if len(email_lines) >= 2:
            email_recap = "\n".join(email_lines[:2])
            email_content.insert(tk.END, email_recap)
        else:
            email_content.insert(tk.END, self.current_scenario["email"])
        email_content.config(state=tk.DISABLED)
        
        # Button to continue
        ttk.Button(feedback_frame, text="Continue", command=self.next_scenario, width=20).pack(pady=20)

    def next_scenario(self):
        self.scenario_index += 1
        self.display_next_scenario()

    def show_game_results(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        results_frame = ttk.Frame(self.content_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Game over heading
        ttk.Label(results_frame, text=f"Game Over, {self.player_name}!", 
                    font=("Helvetica", 20, "bold")).pack(pady=10)
        
        # Results
        accuracy = (self.correct_answers / max(1, len(self.scenarios))) * 100
        avg_time = self.total_time / max(1, len(self.scenarios))
        
        results_text = f"""
        Final Score: {self.score}

        Correct Answers: {self.correct_answers}/{len(self.scenarios)} ({accuracy:.1f}%)

        Average Response Time: {avg_time:.2f} seconds
            """
        
        results_box = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                width=50, height=8, font=("Helvetica", 12))
        results_box.pack(padx=20, pady=10)
        results_box.insert(tk.END, results_text)
        results_box.config(state=tk.DISABLED)
        
        # Expert feedback
        feedback_frame = ttk.LabelFrame(results_frame, text="Expert Feedback", padding=10)
        feedback_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if accuracy >= 90:
            feedback = "Excellent! You're a phishing detection expert!"
        elif accuracy >= 70:
            feedback = "Good job! You're getting better at spotting phishing attempts."
        else:
            feedback = "Keep practicing! Phishing can be tricky to spot."
        
        ttk.Label(feedback_frame, text=feedback, font=("Helvetica", 12)).pack(pady=10)
        
        # Button frame
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(pady=20)
        
        # Add to leaderboard
        self.add_to_leaderboard()
        
        ttk.Button(button_frame, text="View Leaderboard", 
                    command=self.display_leaderboard, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Play Again", 
                    command=self.show_welcome_screen, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Exit", 
                    command=self.root.destroy, width=20).pack(side=tk.LEFT, padx=10)

        ...

def main():
    root = tk.Tk()
    app = PhishingGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()