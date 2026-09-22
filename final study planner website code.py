from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

# --- Simple Helper Functions to Read and Write Text Files ---


def read_file(filename):
    items = []
    try:
        f = open(filename, "r")
        for line in f:
            line = line.strip()
            if line:
                items.append(line)
        f.close()
    except FileNotFoundError:
        pass
    return items


def write_file(filename, items):
    f = open(filename, "w")
    for item in items:
        f.write(item + "\n")
    f.close()


def read_text(filename):
    try:
        f = open(filename, "r")
        content = f.read()
        f.close()
        return content
    except FileNotFoundError:
        return ""


def write_text(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()


# --- HTML Template (Pure HTML, Zero CSS) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Daily Planner</title>
</head>
<body>

    <h1>🎓 Student Daily Planner & Workspace</h1>
    <p>A simple Python-based workspace for college tasks, project ideas, and deadlines.</p>
    <hr>

    <!-- SECTION 1: TO-DO TASKS -->
    <h2>1. Daily To-Do Tasks</h2>
    <form action="/add_task" method="POST">
        <label for="task">New Task: </label>
        <input type="text" name="task" id="task" placeholder="e.g. Maths Tutorial Sheet 3" size="40" required>
        <input type="submit" value="Add Task">
    </form>

    <ol>
        {% for task in tasks %}
            <li>
                {{ task }} 
                <a href="/delete_task/{{ loop.index0 }}">[Delete]</a>
            </li>
        {% endfor %}
    </ol>

    <hr>

    <!-- SECTION 2: DEADLINES -->
    <h2>2. Upcoming Deadlines & Exams</h2>
    <form action="/add_deadline" method="POST">
        <label for="subject">Subject / Event: </label>
        <input type="text" name="subject" id="subject" placeholder="e.g. Physics Mid-Sem" required>
        
        <label for="date">Date: </label>
        <input type="date" name="date" id="date" required>
        
        <input type="submit" value="Add Deadline">
    </form>

    <ul>
        {% for dl in deadlines %}
            <li>
                {{ dl }} 
                <a href="/delete_deadline/{{ loop.index0 }}">[Remove]</a>
            </li>
        {% endfor %}
    </ul>

    <hr>

    <!-- SECTION 3: PROJECT IDEAS & NOTES -->
    <h2>3. Brainstorming / Project Ideas</h2>
    <p>Write your rough ideas, hackathon notes, or thoughts below:</p>
    <form action="/save_ideas" method="POST">
        <textarea name="ideas" rows="6" cols="60" placeholder="Type your ideas here...">{{ ideas }}</textarea>
        <br>
        <input type="submit" value="Save Notes">
    </form>

    <hr>

    <!-- SECTION 4: CLEAR ALL DATA -->
    <h2>4. Reset Planner</h2>
    <form action="/clear_all" method="POST">
        <input type="submit" value="Reset Entire Planner">
    </form>

</body>
</html>
"""


# --- URL Routes / Logic ---


@app.route("/")
def home():
    tasks = read_file("tasks.txt")
    deadlines = read_file("deadlines.txt")
    ideas = read_text("ideas.txt")
    return render_template_string(
        HTML_TEMPLATE, tasks=tasks, deadlines=deadlines, ideas=ideas
    )


@app.route("/add_task", methods=["POST"])
def add_task():
    new_task = request.form.get("task")
    if new_task:
        tasks = read_file("tasks.txt")
        tasks.append(new_task)
        write_file("tasks.txt", tasks)
    return redirect("/")


@app.route("/delete_task/<int:index>")
def delete_task(index):
    tasks = read_file("tasks.txt")
    if 0 <= index < len(tasks):
        tasks.pop(index)
        write_file("tasks.txt", tasks)
    return redirect("/")


@app.route("/add_deadline", methods=["POST"])
def add_deadline():
    subject = request.form.get("subject")
    date = request.form.get("date")
    if subject and date:
        deadlines = read_file("deadlines.txt")
        entry = subject + " (Due Date: " + date + ")"
        deadlines.append(entry)
        write_file("deadlines.txt", deadlines)
    return redirect("/")


@app.route("/delete_deadline/<int:index>")
def delete_deadline(index):
    deadlines = read_file("deadlines.txt")
    if 0 <= index < len(deadlines):
        deadlines.pop(index)
        write_file("deadlines.txt", deadlines)
    return redirect("/")


@app.route("/save_ideas", methods=["POST"])
def save_ideas():
    notes = request.form.get("ideas")
    write_text("ideas.txt", notes)
    return redirect("/")


@app.route("/clear_all", methods=["POST"])
def clear_all():
    write_file("tasks.txt", [])
    write_file("deadlines.txt", [])
    write_text("ideas.txt", "")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)