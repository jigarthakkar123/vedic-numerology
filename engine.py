from datetime import datetime, timedelta
from constants import *

def reduce_digit(n):
    while n > 9:
        n = sum(int(x) for x in str(n))
    return n


def root_number(day):
    return reduce_digit(day)


def destiny_number(day,month,year):
    digits=[int(x) for x in f"{day}{month}{year}"]
    return reduce_digit(sum(digits))


def base_digits(day,month,year):

    year_digits=str(year)[2:]

    digits=[int(x) for x in f"{day}{month}{year_digits}" if x!="0"]

    return digits


def count_numbers(digits):

    counts={i:0 for i in range(1,10)}

    for d in digits:
        counts[d]+=1

    return counts


def build_grid(counts):

    grid=[]

    for row in VEDIC_GRID:

        r=[]

        for n in row:

            if counts[n]==0:
                r.append("-")
            else:
                r.append(str(n)*counts[n])

        grid.append(r)

    return grid


def apply_dasha(counts,number):

    counts[number]+=1

    return counts


def mahadasha(root,birth_year,target_year):

    sequence=list(range(root,10))+list(range(1,root))

    year=birth_year
    index=0

    while True:

        num=sequence[index%9]
        duration=num

        if year<=target_year<year+duration:
            return num

        year+=duration
        index+=1


def antardasha(year,root,month,weekday):

    last_two=year%100
    total=last_two+root+month+weekday

    return reduce_digit(total)


# Correct Pratyantar logic
def pratyantar_number(start_date, antardasha, target_date):

    number = antardasha
    current = start_date

    # Maximum cycle duration ~360 days
    for _ in range(60):

        duration = number * 8
        end = current + timedelta(days=duration)

        if current <= target_date < end:
            return number

        current = end
        number += 1

        if number > 9:
            number = 1

    # fallback (should never happen)
    return antardasha

def pratyantar_calendar(start_date, antardasha):

    from datetime import timedelta

    result = []

    current = start_date
    number = antardasha

    for _ in range(12):

        duration = number * 8
        end = current + timedelta(days=duration)

        result.append({
            "start": current,
            "end": end,
            "number": number
        })

        current = end

        number += 1
        if number > 9:
            number = 1

    return result

def calculate_number_power(counts, root, destiny):

    
    power = {i: 0 for i in range(1,10)}
    
    # Root → 30%
    power[root] += 30

    # Destiny → 40%
    power[destiny] += 40

    # Find unique remaining numbers (excluding root & destiny)
    remaining_numbers = []

    for num in range(1,10):
        if counts[num] > 0 and num != root and num != destiny:
            remaining_numbers.append(num)

    # Divide 30% among unique numbers
    if len(remaining_numbers) > 0:

        share = 30 / len(remaining_numbers)

        for num in remaining_numbers:
            power[num] += round(share, 2)

    return power
def number_nature(num, count, destiny):

    # 🔵 DESTINY OVERRIDE (VERY IMPORTANT)
    if num == destiny:
        return "Positive"

    # Normal rules
    if num in [1,2,3,5,7,9]:
        if count == 1:
            return "Positive"
        elif count > 1:
            return "Negative"

    if num in [4,8]:
        if count % 2 == 0:
            return "Positive"
        else:
            return "Negative"

    if num == 6:
        if count == 1:
            return "Positive"
        elif count > 1:
            return "Negative"

    return "Neutral"

def combined_dasha_interpretation(md, ad, pd):

    # Base meanings
    meaning = {
        1: "leadership and self-focus",
        2: "emotional sensitivity and relationships",
        3: "creativity and expression",
        4: "discipline and obstacles",
        5: "communication and change",
        6: "responsibility and family matters",
        7: "spiritual thinking and isolation",
        8: "karmic pressure and financial matters",
        9: "high energy and aggression"
    }

    # Special intelligent rules
    special_cases = {

        (9,2,5): "High aggression with emotional sensitivity may lead to conflicts in communication or arguments.",
        (6,2,1): "Strong focus on relationships and emotional decisions may lead to important life commitments.",
        (8,4,7): "This period may bring struggles, delays, and isolation requiring patience and discipline.",
        (5,3,1): "Creative communication and leadership may bring new opportunities and growth.",
        (9,1,8): "Strong action and authority may bring power but also risk of conflicts or ego clashes."
    }

    # Check special cases
    if (md, ad, pd) in special_cases:
        return special_cases[(md, ad, pd)]

    # Default intelligent sentence
    return (
        f"{meaning[md].capitalize()} combined with {meaning[ad]} "
        f"and influenced by {meaning[pd]} may create situations where "
        f"these energies interact strongly in your life."
    )