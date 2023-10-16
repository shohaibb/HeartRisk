from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gender = request.form["gender"].lower()
        smoke = request.form["smoke"].lower()
        treatedsbp = request.form["treatedsbp"].lower()

        try:
            age = int(request.form["age"])
            tc = int(request.form["tc"])
            hdl = int(request.form["hdl"])
            sbp = int(request.form["sbp"])
        except ValueError:
            flash("Please enter valid numbers for age, cholesterol, HDL, and SBP.")
            return redirect(url_for('index'))
        
        if gender not in ["male", "female"]:
            flash("Please select a valid gender.")
            return redirect(url_for('index'))

        if smoke not in ["yes", "no"]:
            flash("Please specify if you smoke.")
            return redirect(url_for('index'))
        
        def calculate_risk():
            age = int(request.form.get('age'))
    
        if age < 20:
            flash("You are too young for this calculator to predict your risk of heart disease. If you have concerns about your health, please seek advice from a medical professional.")
            return redirect(url_for('index'))
        
        if tc < 90:
            flash("Please review your cholesterol data for accuracy; the recorded level appears quite low")
            return redirect(url_for('index'))
        
        if hdl < 0:
            flash("Please review your HDL data for accuracy; the recorded level appears quite low")
            return redirect(url_for('index'))
        
        if sbp < 0:
            flash("Please review your Systolic Blood Pressure data for accuracy; the recorded value appears quite low")
            return redirect(url_for('index'))
    

        if gender == "male":
            tcpoints = male_cholesterol_points(tc, age)
            agepoints = male_age_points(age)
            smokepoints = male_smoke_points(smoke, age)
            hdlpoints = male_hdl_points(hdl)
            sbppoints = male_sbp_points(treatedsbp, sbp)
        else:
            tcpoints = female_cholesterol_points(tc, age)
            agepoints = female_age_points(age)
            smokepoints = female_smoke_points(smoke, age)
            hdlpoints = female_hdl_points(hdl)
            sbppoints = female_sbp_points(treatedsbp, sbp)

        totalpoints = agepoints + tcpoints + smokepoints + hdlpoints + sbppoints 
        ten_year = 0  

        if gender == "male":
            ten_year = calculate_male_risk(totalpoints)
        else:
            ten_year = calculate_female_risk(totalpoints)

        return render_template("result.html", total_points=totalpoints, ten_year=ten_year)

    return render_template("index.html")

def male_age_points(age):
    if 20 <= age <= 34:
        return -9
    if 35 <= age <= 39:
        return -4
    if 40 <= age <= 44:
        return 0
    if 45 <= age <= 49:
        return 3
    if 50 <= age <= 54:
        return 6
    if 55 <= age <= 59:
        return 8
    if 60 <= age <= 64:
        return 10
    if 65 <= age <= 69:
        return 11
    if 70 <= age <= 74:
        return 12
    if 75 <= age <= 79:
        return 13
    return 0

def female_age_points(age):
    if 20 <= age <= 34:
        return -7
    if 35 <= age <= 39:
        return -3
    if 40 <= age <= 44:
        return 0
    if 45 <= age <= 49:
        return 3
    if 50 <= age <= 54:
        return 6
    if 55 <= age <= 59:
        return 8
    if 60 <= age <= 64:
        return 10
    if 65 <= age <= 69:
        return 12
    if 70 <= age <= 74:
        return 14
    if 75 <= age <= 79:
        return 16
    return 0

def male_cholesterol_points(tc, age):
    if tc < 160:
        return 0
    if 160 <= tc <= 199:
        if 20 <= age <= 39:
            return 4
        elif 40 <= age <= 49:
            return 3
        elif 50 <= age <= 59:
            return 2
        elif 60 <= age <= 69:
            return 1
        elif 70 <= age <= 79:
            return 0
    elif 200 <= tc <= 239:
        if 20 <= age <= 39:
            return 7
        elif 40 <= age <= 49:
            return 5
        elif 50 <= age <= 59:
            return 3
        elif 60 <= age <= 69:
            return 1
        elif 70 <= age <= 79:
            return 0
    elif 240 <= tc <= 279:
        if 20 <= age <= 39:
            return 9
        elif 40 <= age <= 49:
            return 6
        elif 50 <= age <= 59:
            return 4
        elif 60 <= age <= 69:
            return 2
        elif 70 <= age <= 79:
            return 1
    elif tc >= 280:
        if 20 <= age <= 39:
            return 11
        elif 40 <= age <= 49:
            return 8
        elif 50 <= age <= 59:
            return 5
        elif 60 <= age <= 69:
            return 3
        elif 70 <= age <= 79:
            return 1
    return 0

def female_cholesterol_points(tc, age):
    if tc < 160:
        return 0
    if 160 <= tc <= 199:
        if 20 <= age <= 39:
            return 4
        elif 40 <= age <= 49:
            return 3
        elif 50 <= age <= 59:
            return 2
        elif 60 <= age <= 69:
            return 1
        elif 70 <= age <= 79:
            return 1
    elif 200 <= tc <= 239:
        if 20 <= age <= 39:
            return 8
        elif 40 <= age <= 49:
            return 6
        elif 50 <= age <= 59:
            return 4
        elif 60 <= age <= 69:
            return 2
        elif 70 <= age <= 79:
            return 1
    elif 240 <= tc <= 279:
        if 20 <= age <= 39:
            return 11
        elif 40 <= age <= 49:
            return 8
        elif 50 <= age <= 59:
            return 5
        elif 60 <= age <= 69:
            return 3
        elif 70 <= age <= 79:
            return 2
    elif tc >= 280:
        if 20 <= age <= 39:
            return 13
        elif 40 <= age <= 49:
            return 10
        elif 50 <= age <= 59:
            return 7
        elif 60 <= age <= 69:
            return 4
        elif 70 <= age <= 79:
            return 2
    return 0

def male_smoke_points(smoke, age):
    if smoke == "yes":
        if 20 <= age <= 39:
            return 8
        elif 40 <= age <= 49:
            return 5
        elif 50 <= age <= 59:
            return 3
        elif 60 <= age <= 69:
            return 1
        elif 70 <= age <= 79:
            return 1
    return 0

def female_smoke_points(smoke, age):
    if smoke == "yes":
        if 20 <= age <= 39:
            return 9
        elif 40 <= age <= 49:
            return 7
        elif 50 <= age <= 59:
            return 4
        elif 60 <= age <= 69:
            return 2
        elif 70 <= age <= 79:
            return 1
    return 0

def male_hdl_points(hdl):
    if hdl >= 60:
        return -1
    elif 50 <= hdl <= 59:
        return 0
    elif 40 <= hdl <= 49:
        return 1
    elif hdl < 40:
        return 2
    return 0

def female_hdl_points(hdl):
    return male_hdl_points(hdl)

def male_sbp_points(treatedsbp, sbp):
    if treatedsbp == "yes":
        if sbp < 120:
            return 0
        elif 120 <= sbp <= 129:
            return 1
        elif 130 <= sbp <= 139:
            return 2
        elif 140 <= sbp <= 159:
            return 2
        else:  
            return 3
    else:  
        if sbp < 120:
            return 0
        elif 120 <= sbp <= 129:
            return 0
        elif 130 <= sbp <= 139:
            return 1
        elif 140 <= sbp <= 159:
            return 1
        else:  
            return 2

def female_sbp_points(treatedsbp, sbp):
    if treatedsbp == "yes":
        if sbp < 120:
            return 0
        elif 120 <= sbp <= 129:
            return 3
        elif 130 <= sbp <= 139:
            return 4
        elif 140 <= sbp <= 159:
            return 5
        else:  
            return 6
    else:  
        if sbp < 120:
            return 0
        elif 120 <= sbp <= 129:
            return 1
        elif 130 <= sbp <= 139:
            return 2
        elif 140 <= sbp <= 159:
            return 3
        else:  
            return 4
        
def calculate_male_risk(points):
    risk_dict = {
        (-float('inf'), 0): "<1",
        (0, 1): "1",
        (1, 2): "1",
        (2, 3): "1",
        (3, 4): "1",
        (4, 5): "1",
        (5, 6): "2",
        (6, 7): "2",
        (7, 8): "3",
        (8, 9): "4",
        (9, 10): "5",
        (10, 11): "6",
        (11, 12): "8",
        (12, 13): "10",
        (13, 14): "12",
        (14, 15): "16",
        (15, 16): "20",
        (16, 17): "25",
        (17, float('inf')): ">= 30"
    }
    
    for (low, high), risk in risk_dict.items():
        if low <= points < high:
            return risk
    return None 


def calculate_female_risk(points):
    risk_dict = {
        (-float('inf'), 9): "<1",
        (9, 10): "1",
        (10, 11): "1",
        (11, 12): "1",
        (12, 13): "1",
        (13, 14): "2",
        (14, 15): "2",
        (15, 16): "3",
        (16, 17): "4",
        (17, 18): "5",
        (18, 19): "6",
        (19, 20): "8",
        (20, 21): "11",
        (21, 22): "14",
        (22, 23): "17",
        (23, 24): "22",
        (24, 25): "27",
        (25, float('inf')): ">= 30"
    }
    
    for (low, high), risk in risk_dict.items():
        if low <= points < high:
            return risk
    return None 

    
if __name__ == "__main__":
    app.run(debug=True)
