from flask import Flask, render_template, request
from datetime import datetime
from engine import *
from characteristics import CHARACTERISTICS, DASHA_MEANING
from engine import combined_dasha_interpretation

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    def index():

    # ✅ DEFAULT SAFE VALUES
        data = {
            "grid": [["","",""],["","",""],["","",""]],
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

        dob = request.form["dob"]

        parts = dob.split("-")

        birth_year = int(parts[0])
        birth_month = int(parts[1])
        birth_day = int(parts[2])

        # ✅ CLEAN YEAR/MONTH
        year_input = request.form.get("year")
        year = int(year_input) if year_input else datetime.now().year

        month_input = request.form.get("month")
        month = int(month_input) if month_input else datetime.now().month

        # calculations
        root = root_number(birth_day)
        destiny = destiny_number(birth_day, birth_month, birth_year)

        digits = base_digits(birth_day, birth_month, birth_year)
        digits.append(root)
        digits.append(destiny)

        counts = count_numbers(digits)

        md = mahadasha(root, birth_year, year)

        weekday = 1
        ad = antardasha(year, root, birth_month, weekday)

        # ✅ FIXED DATE
        start_date = datetime(year, birth_month, birth_day)
        target_date = datetime(year, month, 15)

        pd = pratyantar_number(start_date, ad, target_date)

        counts = apply_dasha(counts, md)
        counts = apply_dasha(counts, ad)
        counts = apply_dasha(counts, pd)

        grid = build_grid(counts)

        power = calculate_number_power(counts, root, destiny)
        combined_text = combined_dasha_interpretation(md, ad, pd)

        data = {
            "grid": grid,
            "root": root,
            "destiny": destiny,
            "md": md,
            "ad": ad,
            "pd": pd,
            "power": power,
            "counts": counts,
            "combined": combined_text
        }

    return render_template("index.html", data=data)

if __name__ == "__main__":
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=10000)