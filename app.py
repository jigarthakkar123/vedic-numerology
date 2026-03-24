from flask import Flask, render_template, request
from datetime import datetime

from engine import *
from characteristics import CHARACTERISTICS, DASHA_MEANING
from engine import combined_dasha_interpretation

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    # ✅ DEFAULT DATA (VERY IMPORTANT FOR RENDER + FIRST LOAD)
    data = {
        "basic_grid": [["","",""],["","",""],["","",""]],
        "dasha_grid": [["","",""],["","",""],["","",""]],
        "root": 0,
        "destiny": 0,
        "md": 0,
        "ad": 0,
        "pd": 0,
        "power": {},
        "counts": {},
        "combined": "",
        "dob": "",
        "year_input": "",
        "month_input": ""
    }

    if request.method == "POST":

        dob = request.form.get("dob")

        # ✅ SAFE DOB PARSING
        if dob:
            parts = dob.split("-")
            birth_year = int(parts[0])
            birth_month = int(parts[1])
            birth_day = int(parts[2])
        else:
            # fallback (should not happen)
            birth_year = 2000
            birth_month = 1
            birth_day = 1

        # ✅ SAFE YEAR
        year_input = request.form.get("year")
        year = int(year_input) if year_input else datetime.now().year

        # ✅ SAFE MONTH
        month_input = request.form.get("month")
        month = int(month_input) if month_input else datetime.now().month

        # 🔢 CALCULATIONS
        root = root_number(birth_day)
        destiny = destiny_number(birth_day, birth_month, birth_year)

        digits = base_digits(birth_day, birth_month, birth_year)
        digits.append(root)
        digits.append(destiny)

        # ✅ BASIC COUNTS (ONLY DOB + ROOT + DESTINY)
        base_counts = count_numbers(digits.copy())

        # ✅ DASHA COUNTS (START FROM BASE)
        dasha_counts = base_counts.copy()

        md = mahadasha(root, birth_year, year)

        weekday = 1  # you can improve later
        ad = antardasha(year, root, birth_month, weekday)

        # ✅ DATE FIX (NO ERROR)
        # Safe day handling
        safe_day = min(birth_day, 28)

        start_date = datetime(year, birth_month, safe_day)
        target_date = datetime(year, month, 15)

        
        pd = pratyantar_number(start_date, ad, target_date)
        print("DEBUG → Month:", month, "PD:", pd)
        # APPLY DASHAS
        dasha_counts = apply_dasha(dasha_counts, md)
        dasha_counts = apply_dasha(dasha_counts, ad)
        dasha_counts = apply_dasha(dasha_counts, pd)

        basic_grid = build_grid(base_counts)
        dasha_grid = build_grid(dasha_counts)

        power = calculate_number_power(dasha_counts, root, destiny)

        combined_text = combined_dasha_interpretation(md, ad, pd)

        # ✅ FINAL DATA (OVERWRITE DEFAULT)
        data = {
            "basic_grid": basic_grid,   # ✅ GRID 1
            "dasha_grid": dasha_grid,   # ✅ GRID 2

            "root": root,
            "destiny": destiny,
            "md": md,
            "ad": ad,
            "pd": pd,

            "power": power,
            "counts": dasha_counts,
            "combined": combined_text,

            "dob": dob,
            "year_input": year,
            "month_input": month
        }

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)