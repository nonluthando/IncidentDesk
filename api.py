from flask import Blueprint, request, jsonify
from database import get_db_connection
from crud import get_incidents, get_incident, create_incident_simple, update_status, delete_incident

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/incidents")
def api_list_incidents():
    status = request.args.get("status")
    severity = request.args.get("severity")

    conn = get_db_connection()
    incidents = get_incidents(conn, status=status, severity=severity)
    conn.close()

    return jsonify([dict(row) for row in incidents]), 200


@api_bp.get("/incidents/<int:incident_id>")
def api_get_incident(incident_id):
    conn = get_db_connection()
    incident = get_incident(conn, incident_id)
    conn.close()

    if incident is None:
        return jsonify({"error": "Incident not found"}), 404

    return jsonify(dict(incident)), 200


@api_bp.post("/incidents")
def api_create_incident():
    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    severity = data.get("severity", "").strip().upper()

    if not title or not description or not severity:
        return jsonify({"error": "title, description, and severity are required"}), 400

    conn = get_db_connection()
    create_incident_simple(conn, title, description, severity)
    conn.close()

    return jsonify({"message": "Incident created"}), 201


@api_bp.patch("/incidents/<int:incident_id>")
def api_update_incident_status(incident_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status", "").strip().upper()

    if not status:
        return jsonify({"error": "status is required"}), 400

    conn = get_db_connection()
    incident = get_incident(conn, incident_id)

    if incident is None:
        conn.close()
        return jsonify({"error": "Incident not found"}), 404

    update_status(conn, incident_id, status)
    conn.close()

    return jsonify({"message": "Incident updated"}), 200


@api_bp.delete("/incidents/<int:incident_id>")
def api_delete_incident(incident_id):
    conn = get_db_connection()
    incident = get_incident(conn, incident_id)

    if incident is None:
        conn.close()
        return jsonify({"error": "Incident not found"}), 404

    delete_incident(conn, incident_id)
    conn.close()

    return jsonify({"message": "Incident deleted"}), 200
