from datetime import datetime
import pandas as pd
import random
import re
import pywhatkit as kit

DEFAULT_CC = "91"  # your country code

def normalize_number(raw_number: str, default_cc: str = DEFAULT_CC) -> str:
    s = re.sub(r"\D", "", str(raw_number))  # keep digits only
    s = s.lstrip("0")  # remove leading zeros
    if len(s) == 10:
        s = default_cc + s
    return s

today = datetime.now()
data = pd.read_csv("birthdays.csv")

# Find all birthdays today
birthday_people = data[(data["day"] == today.day) & (data["month"] == today.month)]

if birthday_people.empty:
    print("No birthdays today.")
else:
    for _, person in birthday_people.iterrows():
        # Pick random template
        file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
        with open(file_path, "r", encoding="utf-8") as f:
            contents = f.read().replace("[NAME]", person["name"])

        message = f"🎉 Happy Birthday {person['name']}! 🎂\n\n{contents}"
        number = normalize_number(person["number"])

        try:
            kit.sendwhatmsg_instantly("+" + number, message, wait_time=15, tab_close=True)
            print(f"✅ Sent instantly to {person['name']} ({number})")
        except Exception as e:
            print(f"❌ Failed to send to {person['name']} ({person['number']}): {e}")
