import os
import requests
import time
import json
from datetime import datetime
from colorama import Fore, Style, init
from tabulate import tabulate
import readline

# Initialize colorama for colored terminal output
init(autoreset=True)

BASE_URL = 'https://fintopio-tg.fintopio.com/api/'

# Helper function to introduce a delay
def delay(seconds):
    time.sleep(seconds)

# Fetch referral data
def fetch_referral_data(token):
    try:
        response = requests.get(BASE_URL + 'referrals/data', headers={
            'Authorization': f'Bearer {token}'
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error fetching referral data: {error.response.json().get('message')}")
    return None

# Fetch tasks
def fetch_tasks(token):
    try:
        response = requests.get(BASE_URL + 'hold/tasks', headers={
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
        response = requests.post(BASE_URL + f'hold/tasks/{task_id}/start', headers={
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
        response = requests.post(BASE_URL + f'hold/tasks/{task_id}/claim', headers={
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
        response = requests.post(BASE_URL + 'daily-checkins', headers={
            'Authorization': f'Bearer {token}'
        }, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error during daily check-in: {error}")
    return None

# Start farming
def start_farming(token):
    try:
        response = requests.post(BASE_URL + 'farming/farm', headers={
            'Authorization': f'Bearer {token}'
        }, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error starting farming: {error}")
    return None

# Claim farming rewards
def claim_farming(token):
    try:
        response = requests.post(BASE_URL + 'farming/claim', headers={
            'Authorization': f'Bearer {token}'
        }, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error claiming farming: {error}")
    return None

# Fetch diamond status
def fetch_diamond(token):
    try:
        response = requests.get(BASE_URL + 'clicker/diamond/state', headers={
            'Authorization': f'Bearer {token}'
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error fetching diamond: {error.response.json().get('message')}")
    return None

# Claim a diamond
def claim_diamond(token, diamond_number):
    try:
        response = requests.post(BASE_URL + 'clicker/diamond/complete', headers={
            'Authorization': f'Bearer {token}'
        }, json={'diamondNumber': diamond_number})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"{Fore.RED}❌ Error claiming diamond: {error}")
    return None

# Display header
def display_header():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    printf " + "Fore.CYAN + " + "   ___ \n"
    printf " + "Fore.CYAN + " + " o|* *|o  ╔╦═╦╗╔╦╗╔╦═╦╗ \n"
    printf " + "Fore.CYAN + " + " o|* *|o  ║║╔╣╚╝║║║║║║║ \n"
    printf " + "Fore.CYAN + " + " o|* *|o  ║║╚╣╔╗║╚╝║╩║║ \n"
    printf " + "Fore.CYAN + " + "  \===/   ║╚═╩╝╚╩══╩╩╝║ \n"
    printf " + "Fore.CYAN + " + "   |||    ╚═══════════╝ \n"
    printf " + "Fore.CYAN + " + "   ||| \n"
    printf " + "Fore.CYAN + " + "   |||    ╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗ \n"
    printf " + "Fore.CYAN + " + "   |||    ║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║ \n"
    printf " + "Fore.CYAN + " + "___|||___ ╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝ \n"

# Create table for displaying accounts
def create_table(bearers):
    table_data = []
    headers = ['Number', 'Balance', 'Referral(s)', 'Level', 'Rank']

    for idx, bearer in enumerate(bearers, start=1):
        user = fetch_referral_data(bearer)
        if user:
            table_data.append([
                idx,
                user['balance'],
                f"{user['activations']['used']}/{user['activations']['total']}",
                user['level']['name'],
                user['leaderboard']['position'],
            ])
    return tabulate(table_data, headers, tablefmt="grid")

# Handle all tasks
def handle_all_tasks(bearers):
    for index, bearer in enumerate(bearers):
        tasks = fetch_tasks(bearer)
        if tasks:
            print(f"#️⃣ {index + 1} Account:")
            for item in tasks['tasks']:
                if item['status'] == 'available':
                    print(f"🚀 Starting '{item['slug']}' task...")
                    started_task = start_task(bearer, item['id'])
                    if started_task and started_task['status'] == 'verifying':
                        print(f"✔️ Task '{item['slug']}' started!")
                        print(f"🛠 Claiming {item['slug']} task...")
                        claimed_task = claim_task(bearer, item['id'])
                        if claimed_task:
                            print(f"✔️ Task '{item['slug']}' claimed! Congrats! 🎉")
                else:
                    print(f"🛠 Claiming {item['slug']} task...")
                    claimed_task = claim_task(bearer, item['id'])
                    if claimed_task:
                        print(f"✔️ Task '{item['slug']}' claimed! Congrats! 🎉")
                delay(1)

# Handle diamond cracking
def handle_diamond(bearers):
    for index, bearer in enumerate(bearers):
        print(f"#️⃣ {index + 1} Account:")
        try:
            diamond_info = fetch_diamond(bearer)
            if diamond_info and diamond_info['state'] == 'unavailable':
                print(f"{Fore.RED}❌ Diamond not available, try again on {datetime.fromtimestamp(diamond_info['timings']['nextAt'])}")
            else:
                print(f"💎 Cracking the diamond...")
                delay(1)
                claim_diamond(bearer, diamond_info['diamondNumber'])
                print(f"{Fore.GREEN}✔️ Diamond cracked! You got {diamond_info['settings']['totalReward']} 💎")
        except Exception as error:
            print(f"{Fore.RED}❌ Error cracking diamond: {error}")
        delay(0.5)

# Handle daily check-in
def handle_daily_checkin(bearers):
    for index, bearer in enumerate(bearers):
        print(f"#️⃣ {index + 1} Account:")
        checkin_data = daily_checkin(bearer)
        if checkin_data and checkin_data['claimed']:
            print(f"{Fore.GREEN}✔️ Daily check-in successful!")
        else:
            print(f"{Fore.RED}📅 You've already done the daily check-in. Try again tomorrow!")
        print(f"{Fore.GREEN}📅 Total daily check-ins: {checkin_data['totalDays']}")
        print(f"{Fore.GREEN}💰 Daily reward: {checkin_data['dailyReward']}")
        print(f"{Fore.GREEN}💵 Balance after check-in: {checkin_data['balance']}")

# Handle farming
def handle_farming(bearers):
    for index, bearer in enumerate(bearers):
        print(f"#️⃣ {index + 1} Account:")
        try:
            farm_info = claim_farming(bearer)
            if farm_info:
                print(f"{Fore.GREEN}🌱 Farming started!")
                print(f"{Fore.GREEN}🌱 Start time: {datetime.fromtimestamp(farm_info['timings']['start'])}")
                print(f"{Fore.GREEN}🌾 End time: {datetime.fromtimestamp(farm_info['timings']['finish'])}")
        except Exception as error:
            print(f"{Fore.RED}❌ Error handling farming: {error}")
        delay(1)

# Main function to run tasks
def handle_tasks(bearers):
    display_header()
    print(f"{Fore.YELLOW}🚀 Fetching data, please wait...\n")
    table = create_table(bearers)
    print(table)

    mode = input('Do you want to run the bot one-time (1) or continuously (2)?\n\nEnter 1 or 2: ')
    if mode == '1':
        handle_all_tasks(bearers)
    elif mode == '2':
        while True:
            print(f"{Fore.CYAN}Starting automatic flow...")
            handle_all_tasks(bearers)
            print(f"{Fore.YELLOW}⏳ Waiting 30 minutes before the next run...")
            delay(30 * 60)
    else:
        print(f"{Fore.RED}Invalid option!")

# Sample bearer tokens for testing
BEARERS = [
    'your_token_1',
    'your_token_2'
]

# Start the task handler
handle_tasks(BEARERS)
