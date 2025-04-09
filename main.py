import time
import os
import random
import json
from config.settings import get_response
from datetime import datetime

class PhishingGame:
    def __init__(self):
        self.player_name = ""
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_time = 0
        self.leaderboard = []
        self.load_leaderboard()
        self.training_mode = False
        self.scenario_index = 0
        
    def load_leaderboard(self):
        try:
            if os.path.exists("leaderboard.json"):
                with open("leaderboard.json", "r") as file:
                    self.leaderboard = json.load(file)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            self.leaderboard = []
    
    def save_leaderboard(self):
        try:
            with open("leaderboard.json", "w") as file:
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
            "avg_time": round(self.total_time / (self.correct_answers + self.incorrect_answers), 2) if (self.correct_answers + self.incorrect_answers) > 0 else 0,
            "timestamp": timestamp
        }
        self.leaderboard.append(result)
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.save_leaderboard()
    
    def display_leaderboard(self):
        print("\n===== LEADERBOARD =====")
        if not self.leaderboard:
            print("No records yet!")
            return
        
        print(f"{'Rank':<5}{'Name':<15}{'Score':<10}{'Correct':<10}{'Incorrect':<12}{'Avg Time':<10}")
        print("-" * 60)
        
        for i, entry in enumerate(self.leaderboard[:10], 1):
            print(f"{i:<5}{entry['name']:<15}{entry['score']:<10}{entry['correct']:<10}{entry['incorrect']:<12}{entry['avg_time']:<10}")
    
    def show_welcome(self):
        print("""
        ╔═════════════════════════════════════════════════╗
        ║                                                 ║
        ║      PHISHING AWARENESS TRAINING GAME           ║
        ║                                                 ║
        ╚═════════════════════════════════════════════════╝
        
        Welcome to the Phishing Awareness Training Game!
        
        In this game, you'll be presented with email scenarios,
        and your task is to determine whether they are legitimate
        or phishing attempts.
        
        You'll earn points based on your accuracy and speed.
        
        Let's see how well you can detect phishing attempts!
        """)
        
        self.player_name = input("Please enter your name: ")
        while not self.player_name.strip():
            self.player_name = input("Name cannot be empty. Please enter your name: ")
    
    def show_training_intro(self):
        print("""
        ╔═════════════════════════════════════════════════╗
        ║                                                 ║
        ║           TRAINING MODULE INTRODUCTION          ║
        ║                                                 ║
        ╚═════════════════════════════════════════════════╝
        
        Before we start the game, let's go through a brief training session.
        
        Common signs of phishing emails include:
        
        1. Suspicious sender addresses (e.g., misspelled domain names)
        2. Urgent requests or threats
        3. Grammar and spelling errors
        4. Suspicious links (hover to check before clicking)
        5. Requests for personal information
        6. Unexpected attachments
        7. Generic greetings like "Dear Customer"
        8. Offers that seem too good to be true
        
        In the training mode, we'll analyze each scenario together.
        In the game mode, you'll need to decide quickly and accurately.
        
        Press Enter to continue...
        """)
        input()
    
    def get_scenarios(self):
        scenarios = [
            {
                "email": """
From: service@amaz0n.com
Subject: Urgent: Your Account Has Been Compromised
                
Dear Valued Customer,
                
We have detected suspicious activity on your account. Your account has been temporarily suspended.
                
Please click the link below to verify your information and restore your account:
http://amazonn-secure.com/verify
                
If you don't respond within 24 hours, your account will be permanently closed.
                
Amazon Security Team
                """,
                "is_phishing": True,
                "explanation": """
This is a phishing attempt! Here are the red flags:
1. The sender's email contains a zero instead of an 'o' (amaz0n.com)
2. The link domain is misspelled (amazonn-secure.com)
3. The message creates urgency with threats of account closure
4. It asks you to click a suspicious link
5. It doesn't address you by name
                """
            },
            {
                "email": """
From: newsletter@spotify.com
Subject: Your Monthly Spotify Recap
                
Hi there,
                
Here's your monthly listening summary:
- You listened to 427 minutes of music this month
- Your top artist was The Weeknd
- Your favorite genre was Pop
                
Check out your personalized playlist based on your listening habits:
https://open.spotify.com/playlist/recommendations
                
Enjoy the music!
The Spotify Team
                """,
                "is_phishing": False,
                "explanation": """
This is legitimate! Here's why:
1. The sender's email is from the correct domain (spotify.com)
2. The content is personalized based on your listening habits
3. The link goes to the official Spotify domain
4. There's no urgency or threats
5. It doesn't ask for personal information
                """
            },
            {
                "email": """
From: paypal-security@paypal-team.com
Subject: PayPal: Confirm Your Recent Transaction
                
Dear PayPal User,
                
We've detected a unusual transaction on your account for $750.00 to "Online Electronics Store".
                
If you did not make this transaction, you must immediate verify your account details by clicking the link below:
                
https://paypal-secure-center.com/verify
                
Your account will be locked if you do not respond within 12 hours.
                
Security Department
PayPal
                """,
                "is_phishing": True,
                "explanation": """
This is a phishing attempt! Here are the red flags:
1. The sender's email is not from the official PayPal domain (paypal.com)
2. The domain "paypal-team.com" is suspicious
3. The verification link goes to an unofficial website
4. There are grammar errors ("a unusual transaction", "immediate verify")
5. The message creates urgency with a time limit
6. It doesn't address you by name
                """
            },
            {
                "email": """
From: no-reply@linkedin.com
Subject: John Smith has sent you a connection request
                
LinkedIn
                
John Smith has sent you a connection request
                
I'd like to add you to my professional network on LinkedIn.
- John Smith, Senior Developer at Tech Solutions Inc.
                
[View profile]
                
You are receiving connection requests emails. Unsubscribe here.
                
© 2023 LinkedIn Corporation, 1000 W Maude Ave, Sunnyvale, CA 94085.
                """,
                "is_phishing": False,
                "explanation": """
This is legitimate! Here's why:
1. The sender's email is from the correct domain (linkedin.com)
2. The format matches standard LinkedIn connection requests
3. The message is specific about who sent the request
4. It includes a normal LinkedIn footer with unsubscribe option
5. There's no urgency or threats
6. It doesn't ask for sensitive information
                """
            },
            {
                "email": """
From: microsoftsupport@outlook-team.com
Subject: Your Microsoft 365 subscription is expiring
                
MICROSOFT 365
                
Dear Customer,
                
Your Microsoft 365 subscription will expire in 2 days. To ensure no disruption to your service, please update your payment details urgently.
                
Click here to update your payment information: https://microsoft365-renewal.com
                
Note: Failure to update will result in immediate service termination.
                
Microsoft Support Team
                """,
                "is_phishing": True,
                "explanation": """
This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Microsoft's official domain
2. The domain "outlook-team.com" is suspicious
3. The link goes to an unofficial website
4. The message creates urgency
5. It doesn't address you by name
6. Microsoft typically sends subscription reminders well in advance
                """
            },
            {
                "email": """
From: noreply@netflix.com
Subject: Your Netflix bill
                
Your monthly Netflix subscription has been processed.
                
Billing date: April 3, 2023
Amount: $14.99
Next billing date: May 3, 2023
                
To view your receipt, visit netflix.com/YourAccount
                
Questions? Visit the Help Center: help.netflix.com
                
Netflix
                """,
                "is_phishing": False,
                "explanation": """
This is legitimate! Here's why:
1. The sender's email is from the correct domain (netflix.com)
2. It's a standard billing notification with specific details
3. The message directs you to the official Netflix website
4. There's no urgency or threats
5. It doesn't ask you to click suspicious links
6. It offers legitimate help resources
                """
            },
            {
                "email": """
From: support@applesecure.net
Subject: Apple ID: Your account has been locked
                
Dear Customer,
                
Your Apple ID has been locked due to too many failed login attempts.
                
To unlock your account, please verify your information by clicking on the link below:
                
https://apple-id-unlock.com/verify
                
If you don't verify within 24 hours, your account will be permanently deleted.
                
Apple Support
                """,
                "is_phishing": True,
                "explanation": """
This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Apple's official domain (apple.com)
2. The domain "applesecure.net" is suspicious
3. The verification link goes to an unofficial website
4. The message creates urgency with threats of account deletion
5. It doesn't address you by name
6. Apple never threatens to delete accounts in this manner
                """
            },
            {
                "email": """
From: billing@amazon.com
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
Amazon.com
                """,
                "is_phishing": False,
                "explanation": """
This is legitimate! Here's why:
1. The sender's email is from the correct domain (amazon.com)
2. It includes specific order details with a genuine-looking order number
3. It addresses the recipient by name
4. The tracking link directs to the official Amazon website
5. The message is informational with no urgency or threats
6. It doesn't ask for sensitive information
                """
            },
            {
                "email": """
From: service@bankofamerica-secure.com
Subject: URGENT: Unusual activity detected on your account
                
BANK OF AMERICA
                
Dear Client,
                
We have detected unusual activity on your account. For your security, we have limited access to your online banking.
                
CLICK HERE TO VERIFY YOUR IDENTITY AND RESTORE ACCESS
                
If we don't hear from you within 24 hours, your account will remain restricted.
                
Bank of America Security Team
                """,
                "is_phishing": True,
                "explanation": """
This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Bank of America's official domain
2. The domain "bankofamerica-secure.com" is suspicious
3. The "CLICK HERE" doesn't show the actual URL
4. The message creates urgency with threats of continued restriction
5. It doesn't address you by name
6. Banks typically don't send emails with "CLICK HERE" buttons for security issues
                """
            },
            {
                "email": """
From: no-reply@dropbox.com
Subject: John shared "Project Proposal" with you
                
Dropbox
                
John Smith (john.smith@company.com) shared "Project Proposal" with you
                
View file
                
The link to view this file will expire in 30 days.
                
Need help? Visit the Dropbox Help Center.
                
© 2023 Dropbox
                """,
                "is_phishing": False,
                "explanation": """
This is legitimate! Here's why:
1. The sender's email is from the correct domain (dropbox.com)
2. The format matches standard Dropbox file sharing notifications
3. It includes specific details about who shared what
4. It mentions a reasonable expiration period for the link
5. It directs to legitimate help resources
6. There's no urgency or threats
                """
            }
        ]
        return scenarios
    
    def display_scenario(self, scenario, is_training=False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nScenario {self.scenario_index + 1}/{len(self.scenarios)}")
        print("\n" + scenario["email"] + "\n")
        
        if is_training:
            print("In training mode, we'll analyze this together first.")
            input("Press Enter when you're ready to see the analysis...")
            print("\nANALYSIS:")
            print(scenario["explanation"])
            print("\nNow, let's practice making the decision.")
            
        return self.get_user_choice()
    
    def get_user_choice(self):
        start_time = time.time()
        while True:
            choice = input("\nIs this email legitimate (L) or a phishing attempt (P)? ").upper()
            if choice in ['L', 'P']:
                end_time = time.time()
                time_taken = end_time - start_time
                return choice, time_taken
            else:
                print("Invalid choice. Please enter 'L' for legitimate or 'P' for phishing.")
    
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
    
    def display_feedback(self, scenario, choice, time_taken, score_earned):
        is_phishing = scenario["is_phishing"]
        is_correct = (choice == 'P' and is_phishing) or (choice == 'L' and not is_phishing)
        
        print("\n" + "=" * 50)
        if is_correct:
            print(f"✓ CORRECT! You earned {score_earned} points!")
            print(f"Time taken: {time_taken:.2f} seconds")
        else:
            print("✗ INCORRECT!")
            print(f"Time taken: {time_taken:.2f} seconds")
        
        print("\nEXPLANATION:")
        print(scenario["explanation"])
        print("=" * 50)
        
        input("\nPress Enter to continue...")
        return is_correct
    
    def show_game_results(self):
        accuracy = (self.correct_answers / len(self.scenarios)) * 100 if len(self.scenarios) > 0 else 0
        avg_time = self.total_time / len(self.scenarios) if len(self.scenarios) > 0 else 0
        
        print("\n" + "=" * 50)
        print(f"Game Over, {self.player_name}!")
        print("=" * 50)
        print(f"Final Score: {self.score}")
        print(f"Correct Answers: {self.correct_answers}/{len(self.scenarios)} ({accuracy:.1f}%)")
        print(f"Average Response Time: {avg_time:.2f} seconds")
        
        # Add expert feedback based on performance
        if accuracy >= 90:
            print("\nExpert Feedback: Excellent! You're a phishing detection expert!")
        elif accuracy >= 70:
            print("\nExpert Feedback: Good job! You're getting better at spotting phishing attempts.")
        else:
            print("\nExpert Feedback: Keep practicing! Phishing can be tricky to spot.")
            
        self.add_to_leaderboard()
        self.display_leaderboard()
    
    def play_game(self):
        self.show_welcome()
        
        # Ask if player wants training mode
        while True:
            training_choice = input("Would you like to go through the training mode first? (Y/N): ").upper()
            if training_choice in ['Y', 'N']:
                self.training_mode = (training_choice == 'Y')
                break
            else:
                print("Invalid choice. Please enter 'Y' for Yes or 'N' for No.")
        
        if self.training_mode:
            self.show_training_intro()
        
        # Initialize game variables
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_time = 0
        self.scenarios = self.get_scenarios()
        random.shuffle(self.scenarios)
        
        # Game loop
        for i, scenario in enumerate(self.scenarios):
            self.scenario_index = i
            choice, time_taken = self.display_scenario(scenario, self.training_mode)
            
            self.total_time += time_taken
            
            is_phishing = scenario["is_phishing"]
            is_correct = (choice == 'P' and is_phishing) or (choice == 'L' and not is_phishing)
            
            score_earned = self.calculate_score(is_correct, time_taken)
            self.score += score_earned
            
            if is_correct:
                self.correct_answers += 1
            else:
                self.incorrect_answers += 1
            
            self.display_feedback(scenario, choice, time_taken, score_earned)
        
        self.show_game_results()
        
        # Ask if player wants to play again
        while True:
            play_again = input("\nWould you like to play again? (Y/N): ").upper()
            if play_again == 'Y':
                self.play_game()
                break
            elif play_again == 'N':
                print("Thank you for playing! Stay vigilant against phishing attempts!")
                break
            else:
                print("Invalid choice. Please enter 'Y' for Yes or 'N' for No.")


if __name__ == "__main__":
    game = PhishingGame()
    game.play_game()
