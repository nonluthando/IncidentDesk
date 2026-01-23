from datetime import datetime

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

def get_incidents(conn, status=None):
    if status:
        return conn.execute(
            "SELECT * FROM incidents WHERE status = ? ORDER BY created_at DESC",
            (status,)
        ).fetchall()

    return conn.execute(
        "SELECT * FROM incidents ORDER BY created_at DESC"
    ).fetchall()

def get_incident(conn, incident_id):
    return conn.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,)
    ).fetchone()

def update_status(conn, incident_id, status):
    conn.execute(
        "UPDATE incidents SET status = ? WHERE id = ?",
        (status, incident_id)
    )
    conn.commit()
