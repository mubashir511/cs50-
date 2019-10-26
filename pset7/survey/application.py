import cs50
import csv
import os

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html", message="TODO")


@app.route("/form", methods=["POST"])
def post_form():

    form = []

    # Get data from the 'form.html'
    firstName = request.form.get("firstname")
    firstName = firstName.capitalize()
    middleName = request.form.get("middlename")
    middleName = middleName.capitalize()
    lastName = request.form.get("lastname")
    lastName = lastName.capitalize()

    email = request.form.get("email")
    phoneNumber = request.form.get("phoneNumber")

    batch = request.form.get("batch")
    department = request.form.get("department")
    rollno = request.form.get("rollNo")
    satisfaction = request.form.get("suggestion")

    error_msg = "you must provide "

    # Check for missing fileds
    if not firstName:
        error_msg = error_msg + "first name"
    if not middleName:
        error_msg = error_msg + ", middle name"
    if not lastName:
        error_msg = error_msg + ", last name"
    if not email:
        error_msg = error_msg + ", email"
    if not phoneNumber:
        error_msg = error_msg + ", phone number"
    if not batch:
        error_msg = error_msg + ", batch"
    if not department:
        error_msg = error_msg + ", department"
    if not rollno:
        error_msg = error_msg + ", roll no. "
    if not satisfaction:
        error_msg = error_msg + ", layout suggestion"

    # if data is not missing
    if error_msg == "you must provide ":
        # Save the field data into the list
        form_data = {"firstName": firstName, "middleName": middleName, "lastName": lastName, "email": email,
                     "phoneNumber": phoneNumber, "batch": batch, "department": department, "rollNo": rollno, "satisfaction": satisfaction}
        form.append(form_data)

        # Saving data into the csv file
        with open('survey.csv', 'a+', newline='') as csvfile:
            fieldnames = ['name', 'email', 'phone_no', 'batch', 'department', 'rollNo', 'satisfied_with_layout']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # ensure you're at the start of the file..
            csvfile.seek(0)

            # get the first character
            first_char = csvfile.read(1)
            if not first_char:
                writer.writeheader()

            writer.writerow({'name': (form_data['firstName'] + " " + form_data['middleName'] + " " + form_data['lastName']),
                             'email': form_data['email'], 'phone_no': form_data['phoneNumber'], 'batch': form_data['batch'],
                             'department': form_data['department'], 'rollNo': form_data['rollNo'], 'satisfied_with_layout': form_data['satisfaction']
                             })

        return redirect("/sheet")

    # else save and append data and move on to Table
    return render_template("error.html", message=error_msg)


@app.route("/sheet", methods=["GET"])
def get_sheet():

    # Create a list to store data from the csv file
    get_form = []
    count = 0
    # open the csv file
    infile = open("survey.csv", "r")

    # iterate over different data fields
    for line in infile:
        row = line.split(",")
        name = row[0]
        email = row[1]
        phone_no = row[2]
        batch = row[3]
        department = row[4]
        rollno = row[5]
        suggestion = row[6]

        # Save data captured from the csv file into list
        if count >= 1:
            file_data = {"count": count, "name": name, "email": email, "phoneNo": phone_no, "batch": batch,
                         "department": department, "rollNo": rollno, "satisfaction": suggestion}
            get_form.append(file_data)

        count += 1

    return render_template("sheet.html", get_form=get_form)