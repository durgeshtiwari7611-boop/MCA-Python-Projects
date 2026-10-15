"""
Student Management System - Web UI (Flask)
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "student_mgmt_secret_2026"

DATA_FILE = "students.json"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4, ensure_ascii=False)


def generate_id(students):
    if not students:
        return "S001"
    max_num = 0
    for s in students:
        try:
            num = int(s["id"][1:])
            if num > max_num:
                max_num = num
        except:
            pass
    return f"S{max_num + 1:03d}"


@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json
        if data.get("username") == ADMIN_USERNAME and data.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return jsonify({"success": True})
        return jsonify({"success": False, "message": "Invalid credentials!"})
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/api/students")
def get_students():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    students = load_students()
    sort_by = request.args.get("sort", "")
    if sort_by == "name":
        students = sorted(students, key=lambda x: x["name"].lower())
    elif sort_by == "marks_desc":
        students = sorted(students, key=lambda x: x["marks"], reverse=True)
    elif sort_by == "marks_asc":
        students = sorted(students, key=lambda x: x["marks"])
    return jsonify(students)


@app.route("/api/students", methods=["POST"])
def add_student():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    students = load_students()
    
    # Validation
    if not data.get("name", "").strip():
        return jsonify({"error": "Name is required"}), 400
    try:
        age = int(data.get("age", 0))
        marks = float(data.get("marks", 0))
        if age < 15 or age > 50:
            return jsonify({"error": "Age must be 15-50"}), 400
        if marks < 0 or marks > 100:
            return jsonify({"error": "Marks must be 0-100"}), 400
    except:
        return jsonify({"error": "Invalid age or marks"}), 400

    student = {
        "id": generate_id(students),
        "name": data["name"].strip(),
        "age": age,
        "course": data.get("course", "").strip(),
        "marks": marks,
        "email": data.get("email", "").strip(),
        "phone": data.get("phone", "").strip()
    }
    students.append(student)
    save_students(students)
    return jsonify(student)


@app.route("/api/students/<sid>", methods=["PUT"])
def update_student(sid):
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    students = load_students()
    
    for s in students:
        if s["id"] == sid:
            if data.get("name"):
                s["name"] = data["name"].strip()
            if data.get("age"):
                s["age"] = int(data["age"])
            if data.get("course"):
                s["course"] = data["course"].strip()
            if data.get("marks") is not None:
                s["marks"] = float(data["marks"])
            if data.get("email") is not None:
                s["email"] = data["email"].strip()
            if data.get("phone") is not None:
                s["phone"] = data["phone"].strip()
            save_students(students)
            return jsonify(s)
    
    return jsonify({"error": "Student not found"}), 404


@app.route("/api/students/<sid>", methods=["DELETE"])
def delete_student(sid):
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    students = load_students()
    for i, s in enumerate(students):
        if s["id"] == sid:
            students.pop(i)
            save_students(students)
            return jsonify({"success": True})
    return jsonify({"error": "Student not found"}), 404


@app.route("/api/search")
def search_students():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    q = request.args.get("q", "").strip().lower()
    students = load_students()
    if not q:
        return jsonify(students)
    results = [s for s in students if q in s["name"].lower() or q in s["id"].lower() or q in s.get("course", "").lower()]
    return jsonify(results)


@app.route("/api/reports")
def get_reports():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    students = load_students()
    if not students:
        return jsonify({"total": 0})
    
    avg = sum(s["marks"] for s in students) / len(students)
    topper = max(students, key=lambda x: x["marks"])
    lowest = min(students, key=lambda x: x["marks"])
    
    courses = {}
    for s in students:
        courses[s["course"]] = courses.get(s["course"], 0) + 1
    
    grades = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for s in students:
        m = s["marks"]
        if m >= 90: grades["A"] += 1
        elif m >= 75: grades["B"] += 1
        elif m >= 60: grades["C"] += 1
        elif m >= 40: grades["D"] += 1
        else: grades["F"] += 1
    
    passed = len([s for s in students if s["marks"] >= 40])
    
    return jsonify({
        "total": len(students),
        "average": round(avg, 2),
        "topper": {"name": topper["name"], "marks": topper["marks"]},
        "lowest": {"name": lowest["name"], "marks": lowest["marks"]},
        "courses": courses,
        "grades": grades,
        "passed": passed,
        "failed": len(students) - passed
    })


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Student Management System - Web UI")
    print("  Open: http://127.0.0.1:5001")
    print("  Login: admin / admin123")
    print("="*50 + "\n")
    app.run(debug=True, port=5001)
