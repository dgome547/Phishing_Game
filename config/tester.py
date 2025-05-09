import sys, os, json


"""TESTER DEPRECATED NO LONGER SUPPORTED"""
# Add project root to sys.path before importing anything else
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import GeminiManager

def test_gemini_generation():
    manager = GeminiManager()
    scenarios = manager.generate_phishing_scenarios(num_scenarios=3)  # generates 3 phishing + 3 legit

    for idx, scenario in enumerate(scenarios, 1):
        print(f"\n--- Scenario {idx} ---")
        print("EMAIL:\n", scenario.get("email", "[Missing email]"))
        print("\nIS PHISHING:", scenario.get("is_phishing", "[Missing is_phishing]"))
        print("\nEXPLANATION:\n", scenario.get("explanation", "[Missing explanation]"))
        print("-" * 50)

if __name__ == "__main__":
    test_gemini_generation()