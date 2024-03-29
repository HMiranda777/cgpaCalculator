''' ---------------- INIVISIBL CLOUD TASK ---------------- '''

import csv
from flask import Flask, request, render_template, jsonify

ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__)
overall_credits = 0
overall_grade_sum = 0
gpa_list = []
arrears = []
grade_point = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5}


def gpaCalculator(csv_file, sem_no):
    total_credits = 0
    grade_sum = 0
    global overall_credits, overall_grade_sum, gpa_list, grade_point, arrears
    for k in csv_file:
        k[1] = k[1].lower().strip()
        if k[2] in grade_point:
            grade_sum += int(k[3]) * grade_point[k[2]]
            total_credits += int(k[3])

            if k[1] in arrears:
                arrears.remove(k[1]) #cleared arrear in next sem

        elif k[2] == "U" and k[1] not in arrears:
            arrears.append(k[1])

        else:
            print("Enter Valid Grades for ", k[1] )

    gpa_list[sem_no] = grade_sum / total_credits
    overall_grade_sum += grade_sum
    overall_credits += total_credits


@app.route('/')
def start():
    return render_template("cgpa.html")


@app.route("/cgpa", methods=['post'])
def Calculator():
    global overall_credits, overall_grade_sum, gpa_list, grade_point, arrears
    overall_credits = 0
    overall_grade_sum = 0
    gpa_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    arrears = []
    filename_list = []
    result = {}
    sem_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    input_files = request.files.getlist("csv")
    # print(input_files)
    for i in input_files:
        UPLOAD_FILE = "./" + i.filename
        app.config['UPLOAD_FOLDER'] = UPLOAD_FILE
        i.save(app.config['UPLOAD_FOLDER'])
        filename_list.append(i.filename)

    for j in filename_list:
        file = open("./" + j, "r")
        csv_file = csv.reader(file)
        next(csv_file)
        maximum = 0

        for k in csv_file:
            if int(k[0]) > maximum:
                maximum = int(k[0])

            sem_list[maximum - 1] = j
        #print(sem_list)

    for i in range(0, len(sem_list)):
        if sem_list[i] != 0:
            file = open("./" + sem_list[i], "r")
            csv_file = csv.reader(file)
            next(csv_file)
            gpaCalculator(csv_file, i)

    for j in range(0, len(gpa_list)):
        if gpa_list[j] != -1:
            result["gpa_sem_" + str(j + 1)] = gpa_list[j]
    result["cgpa"] = (overall_grade_sum / overall_credits)
    result["current_arrears"] = arrears
    return jsonify(result)


app.run(debug=True)


'''----------------------------------------------------------------------------------------------------------------------------------------'''
