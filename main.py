import os
import time
import random
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import threading
from PIL import Image, ImageTk
from config.settings import generate_scenarios
from config.scenarios import get_premade_scenarios



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
        
        # Timer label (bold)
        self.timer_label = ttk.Label(self.main_frame, text="Time: 0s", font=("Helvetica", 12, "bold"))
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
            os.makedirs("data", exist_ok=True)  # Ensure 'data/' exists (very important 🫠)
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

        # Game mode options
        mode_frame = ttk.Frame(welcome_frame)
        mode_frame.pack(pady=10)

        self.game_mode = tk.StringVar(value="unlimited")
        ttk.Label(mode_frame, text="Game Mode:", font=("Helvetica", 12)).pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(mode_frame, text="Unlimited Time", variable=self.game_mode, value="unlimited").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(mode_frame, text="1-Minute Timed Mode", variable=self.game_mode, value="timed").pack(anchor=tk.W, padx=20)
        
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

        # Check for API key 
        self.use_gemini = (self.scenario_source.get() == "gemini")
        # (Removed premature return here if it doesn't work put it back here)

        # Set training mode
        self.training_mode = self.training_var.get()

        # Set game mode (timed/unlimited)
        self.is_timed_mode = self.game_mode.get() == "timed"
        self.countdown_seconds = 60 if self.is_timed_mode else None

        if self.is_timed_mode:
            self.start_time = time.time()
            self._last_answer_time = time.time()  
            self.timer_running = True
            self.update_timer()
        else:
            self.start_time = time.time()
            self._last_answer_time = time.time()  

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
            all_scenarios = get_premade_scenarios()
            self.scenarios = random.sample(all_scenarios, k=10)
            self.progress_label.config(text=f"Progress: 0/{len(self.scenarios)}")

            # If training mode is enabled -> show training intro
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
        
        # Create an indeterminate progress bar
        self.progress_bar = ttk.Progressbar(loading_frame, mode="indeterminate", length=300)
        self.progress_bar.pack(pady=20)
        self.progress_bar.start(10)
        
        # Force update to show loading screen
        self.root.update()
    
    def generate_scenarios_with_gemini(self):
        try:
            from functools import partial
            from config.settings import generate_scenarios
            # error with handling of first generation proposed fix of saving generations to txt
            # using 11 scenarios for testing for now. 
            self.scenarios = generate_scenarios(11)
            self.root.after(0, self.progress_bar.stop)
            self.root.after(0, self.after_scenarios_loaded)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate scenarios: {str(e)}"))
            self.root.after(0, self.show_welcome_screen)
    
    def after_scenarios_loaded(self):
        self.progress_label.config(text=f"Progress: 0/{len(self.scenarios)}")
        
        # If training mode is enabled, show training intro
        if self.training_mode:
            self.show_training_intro()
        else:
            self.display_next_scenario()
    
    
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
        
        # Start Button
        ttk.Button(training_frame, text="Start Training", command=self.display_next_scenario).pack(pady=20)
    
    
    
    def display_next_scenario(self):
        if self.scenario_index >= len(self.scenarios):
            self.show_game_results()
            return

        # Set per-question timer <<BEFORE>> setting current_scenario
        self._last_answer_time = time.time()
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

        # Decision buttons for UI
        button_frame = ttk.Frame(scenario_frame)
        button_frame.pack(pady=20)

        # Button styling
        style = ttk.Style()
        style.configure("Green.TButton", background="green")
        style.configure("Red.TButton", background="red")

        legitimate_btn = ttk.Button(button_frame, text="Legitimate Email", command=lambda: self.process_answer(False), width=20)
        legitimate_btn.pack(side=tk.LEFT, padx=20)

        phishing_btn = ttk.Button(button_frame, text="Phishing Email", command=lambda: self.process_answer(True), width=20)
        phishing_btn.pack(side=tk.LEFT, padx=20)

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_value = elapsed
            if hasattr(self, "is_timed_mode") and self.is_timed_mode:
                remaining = self.countdown_seconds - elapsed
                self.timer_label.config(text=f"Time Left: {remaining}s")
                if remaining <= 0:
                    self.timer_running = False
                    self.show_game_results()
                    return
            else:
                self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def process_answer(self, guessed_phishing):
        now = time.time()
        if not hasattr(self, "_last_answer_time"):
            self._last_answer_time = self.start_time
        elapsed_time = int(now - self._last_answer_time)
        # self._last_answer_time = now  # Add this back if program unhappy
        self.total_time += elapsed_time

        correct = self.current_scenario["is_phishing"] == guessed_phishing

        if correct:
            self.score += 10
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1

        self.score_label.config(text=f"Score: {self.score}")
        self.scenario_index += 1
        self.progress_label.config(text=f"Progress: {self.scenario_index}/{len(self.scenarios)}")
        if self.scenario_index < len(self.scenarios):
            self.display_next_scenario()
        else:
            self.show_game_results()

    def show_game_results(self):
        self.timer_running = False
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        results_frame = ttk.Frame(self.content_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        ttk.Label(results_frame, text="GAME OVER", font=("Helvetica", 20, "bold")).pack(pady=10)
        ttk.Label(results_frame, text=f"Final Score: {self.score}", font=("Helvetica", 14)).pack(pady=5)
        ttk.Label(results_frame, text=f"Correct Answers: {self.correct_answers}", font=("Helvetica", 14)).pack(pady=5)
        ttk.Label(results_frame, text=f"Incorrect Answers: {self.incorrect_answers}", font=("Helvetica", 14)).pack(pady=5)
        ttk.Label(results_frame, text=f"Average Response Time: {round(self.total_time / max(1, (self.correct_answers + self.incorrect_answers)), 2)}s", font=("Helvetica", 14)).pack(pady=5)

        # Total time formatted (timed mode fix)
        if hasattr(self, "is_timed_mode") and self.is_timed_mode:
            total_elapsed = self.countdown_seconds - max(0, self.countdown_seconds - self.timer_value)
        else:
            total_elapsed = self.timer_value
        total_minutes, total_seconds = divmod(total_elapsed, 60)
        total_time_formatted = f"{total_minutes:02}:{total_seconds:02}"
        ttk.Label(results_frame, text=f"Total Time Taken: {total_time_formatted}", font=("Helvetica", 14)).pack(pady=5)

        feedback_frame = ttk.Frame(results_frame)
        feedback_frame.pack(pady=10)

        # Just a hint of difference between runs
        good_results_feedback = [
            "Great job! You have a good eye for spotting phishing attempts.",
            "Excellent work! Your awareness is impressive.",
            "You nailed it! Keep up the vigilance."
        ]

        bad_results_feedback = [
            "Keep practicing! Phishing can be tricky to spot.",
            "Don't worry, with more practice you'll improve!",
            "Watch out for the red flags next time. You'll get better!"
        ]


        if self.correct_answers >= len(self.scenarios) * 0.7:
            feedback = random.choice(good_results_feedback)
        else:
            feedback = random.choice(bad_results_feedback)

        ttk.Label(feedback_frame, text=feedback, font=("Helvetica", 12)).pack(pady=10)

        # Button frame
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(pady=20)

        self.add_to_leaderboard()

        ttk.Button(button_frame, text="View Leaderboard", command=self.display_leaderboard, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Play Again", command=self.show_welcome_screen, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy, width=20).pack(side=tk.LEFT, padx=10)

def main():
    root = tk.Tk()
    app = PhishingGameGUI(root)
    try:
        root.iconbitmap("assets/icon.ico")
    except:
        pass  
    root.mainloop()

if __name__ == "__main__":
    main()
