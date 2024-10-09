import os
import requests
import time
import json
from datetime import datetime
from colorama import Fore, Style, init
from tabulate import tabulate
import readline
import pyautogui
import random

# Credit @AnnaQitty

# Initialize colorama for colored terminal output
init(autoreset=True)

# Base URL for the ClickApp API
BASE_URL = 'https://clickapp.awkwardmonkey.io/api/'

# Mobile user-agent for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QQ1A.191205.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.106 Mobile Safari/537.36',
}

# Helper function to introduce a delay
def delay(seconds):
    time.sleep(seconds)

# Fetch user data
def fetch_user_data(token):
    try:
        response = requests.get(BASE_URL + 'user/data', headers={
            **HEADERS,
            'Authorization': f'Bearer {token}'
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error fetching user data: {error.response.json().get('message')}")
    return None

# Fetch tasks
def fetch_tasks(token):
    try:
        response = requests.get(BASE_URL + 'tasks', headers={
            **HEADERS,
            'Authorization': f'Bearer {token}'
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error fetching tasks: {error.response.json().get('message')}")
    return None

# Start a task
def start_task(token, task_id):
    try:
        response = requests.post(BASE_URL + f'tasks/{task_id}/start', headers={
            **HEADERS,
            'Authorization': f'Bearer {token}'
        }, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error starting task: {error.response.json().get('message')}")
    return None

# Claim a task
def claim_task(token, task_id):
    try:
        response = requests.post(BASE_URL + f'tasks/{task_id}/claim', headers={
            **HEADERS,
            'Authorization': f'Bearer {token}'
        }, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error claiming task: {error.response.json().get('message')}")
    return None

# Daily check-in
def daily_checkin(token):
    try:
        response = requests.post(BASE_URL + 'checkins', headers={
            **HEADERS,
            'Authorization': f'Bearer {token}'
        }, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error during daily check-in: {error}")
    return None

# Display header
def display_header():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    print(Fore.CYAN + '========================================')
    print(Fore.CYAN + '=    🚀 ClickApp AWK Monkey Bot 🚀     =')
    print(Fore.CYAN + f'=       Created by @AnnaQitty           =')
    print(Fore.CYAN + '========================================')
    print()

# Create table for displaying accounts
def create_table(bearers):
    table_data = []
    headers = ['Number', 'Balance', 'Level', 'Rank']

    for idx, bearer in enumerate(bearers, start=1):
        user = fetch_user_data(bearer)
        if user:
            table_data.append([
                idx,
                user['balance'],
                user['level'],
                user['rank'],
            ])
    return tabulate(table_data, headers, tablefmt="grid")

# Handle all tasks
def handle_all_tasks(bearers):
    for index, bearer in enumerate(bearers):
        tasks = fetch_tasks(bearer)
        if tasks:
            print(f"#️⃣ {index + 1} Account:")
            for item in tasks['data']:  # Assuming tasks are in 'data' field
                if item['status'] == 'available':
                    print(f"🚀 Starting '{item['name']}' task...")
                    started_task = start_task(bearer, item['id'])
                    if started_task:
                        print(f"✔️ Task '{item['name']}' started! Now claiming...")
                        claimed_task = claim_task(bearer, item['id'])
                        if claimed_task:
                            print(f"✔️ Task '{item['name']}' claimed! Congrats! 🎉")
                else:
                    print(f"🛠 Claiming '{item['name']}' task...")
                    claimed_task = claim_task(bearer, item['id'])
                    if claimed_task:
                        print(f"✔️ Task '{item['name']}' claimed! Congrats! 🎉")
                delay(1)

# Tap Game Function
def tap_game():
    """Simulate continuous tapping in the tap game at maximum speed."""
    # Settings for the tap game
    OBSTACLE_HIT_PENALTY = 10  # Points deducted for hitting an obstacle
    COLLECT_INTERVAL = 0.01  # Very short time interval between taps (10ms)
    OBSTACLE_CHANCE = 0.2  # Chance of hitting an obstacle (20%)

    # Game state
    points = 0

    def tap_screen(x, y):
        """Simulate a tap on the screen at (x, y)."""
        pyautogui.click(x, y)

    print("Continuous tapping started! Press Ctrl+C to stop.")
    try:
        while True:  # Continuous loop
            # Randomly decide whether to tap a point or hit an obstacle
            if random.random() > OBSTACLE_CHANCE:
                # Simulate tapping on a point (random x, y coordinates)
                x = random.randint(100, 500)  # Replace with your game's valid x range
                y = random.randint(100, 500)  # Replace with your game's valid y range
                tap_screen(x, y)
                points += 1  # Increment points for successful tap
                # Print points every 100 taps for reduced overhead
                if points % 100 == 0:
                    print(f"Points collected: {points}")
            else:
                # Simulate hitting an obstacle
                points -= OBSTACLE_HIT_PENALTY
                if points < 0:
                    points = 0
                # Print penalty every 100 taps for reduced overhead
                if points % 100 == 0:
                    print(f"Points after hitting obstacle: {points}")

            time.sleep(COLLECT_INTERVAL)  # Wait briefly before the next tap
    except KeyboardInterrupt:
        print("\nTapping stopped.")
        print(f"Final points: {points}")

# Main function to run tasks
def handle_tasks(bearers):
    display_header()
    print(f"{Fore.YELLOW}🚀 Fetching data, please wait...\n")
    table = create_table(bearers)
    print(table)

    while True:
        print("\nSelect an option:")
        print("1: Run automation tasks")
        print("2: Daily check-in")
        print("3: Start tap game")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            handle_all_tasks(bearers)
        elif choice == '2':
            handle_daily_checkin(bearers)
        elif choice == '3':
            tap_game()
        else:
            print(f"{Fore.RED}Invalid option!")

# Sample bearer tokens for testing
BEARERS = [
    'your_token_1',
    'your_token_2'
]

# Start the task handler
handle_tasks(BEARERS)
