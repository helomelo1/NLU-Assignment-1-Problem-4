import re
from datetime import date


def calculate_age(day, month, year):
    today = date.today()
    age = today.year - year
    if (today.month, today.day) < (month, day):
        age -= 1
    return age


def extract_surname(text):
    text = text.strip()

    m = re.search(r'(?:my name is|i am|i\'m)\s+([A-Za-z]+\s+[A-Za-z]+)', text, re.I)
    if m:
        return m.group(1).split()[-1]

    m = re.search(r'^([A-Za-z]+)\s+([A-Za-z]+)$', text)
    if m:
        return m.group(2)

    return None


def parse_birthday(text):
    text = text.strip()

    m = re.search(r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b', text)
    if m:
        d, mth, y = map(int, m.groups())
        if y < 100:
            y += 1900 if y > 25 else 2000
        return d, mth, y

    months = {
        "jan":1,"january":1,"feb":2,"february":2,"mar":3,"march":3,
        "apr":4,"april":4,"may":5,"jun":6,"june":6,"jul":7,"july":7,
        "aug":8,"august":8,"sep":9,"september":9,"oct":10,"october":10,
        "nov":11,"november":11,"dec":12,"december":12
    }

    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})', text, re.I)
    if m:
        d, mon, y = m.groups()
        mon = mon.lower()
        if mon in months:
            return int(d), months[mon], int(y)

    return None


def detect_mood(text):
    text = text.lower()

    if re.search(r'not.*(good|happy|fine|ok)', text):
        return "negative"

    if re.search(r'sad+|bad+|tir+ed|stress+|angr+y', text):
        return "negative"

    if re.search(r'hap+?y|good+|gr+eat|awesome|fine|ok+', text):
        return "positive"

    return "neutral"



def chatbot():
    print("Reggy: Hello! I'm Reggy.")
    print("Reggy: What's your full name? (type 'exit' anytime)")

    stage = 0
    surname = None

    while True:
        user = input("You: ").strip()

        if re.search(r'\b(exit|quit|bye)\b', user.lower()):
            print("Reggy: It was nice chatting with you. Goodbye.")
            break

        if stage == 0:
            surname = extract_surname(user)
            if surname:
                print(f"Reggy: Nice to meet you, {surname}. When is your birthday?")
                stage = 1
            else:
                print("Reggy: Could you tell me your full name?")
            continue

        if stage == 1:
            parsed = parse_birthday(user)
            if parsed:
                d, m, y = parsed
                age = calculate_age(d, m, y)
                print(f"Reggy: You are {age} years old. How are you feeling today?")
                stage = 2
            else:
                print("Reggy: I couldn't understand the date. Try another format.")
            continue

        if stage == 2:
            mood = detect_mood(user)

            if mood == "positive":
                print(f"Reggy: That's great to hear, {surname}.")
            elif mood == "negative":
                print(f"Reggy: I'm sorry you're feeling that way, {surname}.")
            else:
                print(f"Reggy: Thanks for sharing, {surname}.")

            stage = 3
            continue

        if re.search(r'what.*my name', user.lower()):
            print(f"Reggy: Your surname is {surname}.")

        elif re.search(r'\bhow are you\b', user.lower()):
            print("Reggy: I'm doing well, thanks for asking.")

        elif re.search(r'\b(wow|nice|cool|great)\b', user.lower()):
            print("Reggy: I'm glad you think so.")

        elif re.search(r'\bthank', user.lower()):
            print("Reggy: You're welcome.")

        else:
            print(f"Reggy: That's interesting, {surname}. Tell me more.")


if __name__ == "__main__":
    chatbot()
