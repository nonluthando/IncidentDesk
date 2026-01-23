from datetime import datetime

# ---------- CREATE (API) ----------
def create_incident(conn, incident):
    conn.execute(
        """
        INSERT INTO incidents (title, description, severity, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            incident.title,
            incident.description,
            incident.severity,
            "OPEN",
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()


# ---------- CREATE (UI) ----------
def create_incident_simple(conn, title, description, severity):
    conn.execute(
        """
        INSERT INTO incidents (title, description, severity, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, description, severity, "OPEN", datetime.utcnow().isoformat())
    )
    conn.commit()


# ---------- READ (with filters) ----------
def get_incidents(conn, status=None, severity=None):
    query = "SELECT * FROM incidents WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if severity:
        query += " AND severity = ?"
        params.append(severity)

    query += " ORDER BY created_at DESC"

    return conn.execute(query, params).fetchall()


def get_incident(conn, incident_id):
    return conn.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,)
    ).fetchone()


# ---------- UPDATE ----------
def update_status(conn, incident_id, status):
    conn.execute(
        "UPDATE incidents SET status = ? WHERE id = ?",
        (status, incident_id)
    )
    conn.commit()


# ---------- DELETE ----------
def delete_incident(conn, incident_id):
    conn.execute(
        "DELETE FROM incidents WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
