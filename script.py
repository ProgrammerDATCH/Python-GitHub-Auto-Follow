# script.py

import argparse
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import requests
from GithubAPIBot import GithubAPIBot

def run_bot(username):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--user-target", help="Follow the followers of a target user")
    parser.add_argument("-f", "--file", help="Follow users from a pre-generated file")
    parser.add_argument("-p", "--popular", help="Follow the followers of the most popular users from a given country")
    parser.add_argument("-m", "--max-follow", help="Max number of users to follow")
    parser.add_argument("-smin", "--sleep-min", help="Min number of range to randomize sleep seconds between actions")
    parser.add_argument("-smax", "--sleep-max", help="Max number of range to randomize sleep seconds between actions")
    parser.add_argument("-slmin", "--sleep-min-limited", help="Min number of range to randomize sleep seconds when account limited")
    parser.add_argument("-slmax", "--sleep-max-limited", help="Max number of range to randomize sleep seconds when account limited")
    parser.add_argument("-sh", "--sleep-hour", help="Hour for the bot to go to sleep")
    parser.add_argument("-sm", "--sleep-minute", help="Minute for the bot to go to sleep")
    parser.add_argument("-st", "--sleep-time", help="Total time (in hours) for the bot to sleep")
    args = parser.parse_args(["-t", username])

    sleepSecondsActionMin = int(args.sleep_min or 20)
    sleepSecondsActionMax = int(args.sleep_max or 120)
    sleepSecondsLimitedMin = int(args.sleep_min_limited or 600)
    sleepSecondsLimitedMax = int(args.sleep_max_limited or 1500)

    load_dotenv()

    USER = os.getenv("GITHUB_USER")
    TOKEN = os.getenv("TOKEN")

    bot = GithubAPIBot(
        USER,
        TOKEN,
        sleepSecondsActionMin,
        sleepSecondsActionMax,
        sleepSecondsLimitedMin,
        sleepSecondsLimitedMax,
        args.sleep_hour,
        args.sleep_minute,
        args.sleep_time,
        args.max_follow,
    )

    # Grab users from given user's followers
    if args.user_target:
        bot.getFollowers(args.user_target)

    # Write users to be followed to file
    filename = (
        "./logs/"
        + str(datetime.now().strftime("%m-%d-%Y__%H-%M"))
        + "__"
        + str(len(bot.usersToAction))
        + "-followed-users.json"
    )
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as f:
        json.dump(bot.usersToAction, f, indent=4)

    bot.follow()

if __name__ == "__main__":
    run_bot()
