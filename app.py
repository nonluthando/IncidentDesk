from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
DATABASE = "incidentdesk.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return redirect(url_for("list_incidents"))


@app.route("/incidents")
def list_incidents():
    conn = get_db_connection()
    incidents = conn.execute(
        "SELECT * FROM incidents ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("incidents.html", incidents=incidents)


@app.route("/incidents/add", methods=["GET", "POST"])
def add_incident():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        severity = request.form["severity"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO incidents (title, description, severity, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, description, severity, "OPEN", datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()

        return redirect(url_for("list_incidents"))

    return render_template("add_incident.html")


@app.route("/incidents/<int:incident_id>", methods=["GET", "POST"])
def incident_detail(incident_id):
    conn = get_db_connection()

    if request.method == "POST":
        new_status = request.form["status"]
        conn.execute(
            "UPDATE incidents SET status = ? WHERE id = ?",
            (new_status, incident_id)
        )
        conn.commit()

    incident = conn.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,)
    ).fetchone()
    conn.close()

    return render_template("incident_detail.html", incident=incident)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
