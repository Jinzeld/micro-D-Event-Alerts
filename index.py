from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage for events (replace with a database in production)
events = []

# Helper function to send notifications (mock implementation)
def send_notification(user_id, message):
    print(f"Sending notification to user {user_id}: {message}")
    # In a real application, integrate with an email/SMS service like Twilio or SendGrid.

# Helper function to check if two events overlap
def events_overlap(event1, event2):
    event1_start = datetime.fromisoformat(f"{event1['event_date']}T{event1['event_time']}")
    event1_end = event1_start + timedelta(hours=1)  # Assuming each event lasts 1 hour
    event2_start = datetime.fromisoformat(f"{event2['event_date']}T{event2['event_time']}")
    event2_end = event2_start + timedelta(hours=1)  # Assuming each event lasts 1 hour

    return not (event1_end <= event2_start or event1_start >= event2_end)

# Event Notification Microservice
@app.route('/check_upcoming_events', methods=['POST'])
def check_upcoming_events():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Fetch events for the user (replace with a database query)
    user_events = [event for event in events if event['user_id'] == user_id]

    # Check for upcoming events (within 24 hours)
    now = datetime.now()
    upcoming_events = []
    for event in user_events:
        # Combine event_date and event_time to create a full datetime object
        event_datetime = datetime.fromisoformat(f"{event['event_date']}T{event['event_time']}")
        if now <= event_datetime <= now + timedelta(hours=24):
            upcoming_events.append(event)

    # Send notifications for upcoming events
    for event in upcoming_events:
        message = f"Reminder: You have an upcoming event - {event['title']} on {event['event_date']} at {event['event_time']}."
        send_notification(user_id, message)

    return jsonify({"success": True, "upcoming_events": upcoming_events})

# Conflict Resolution Microservice
@app.route('/check_conflicts', methods=['POST'])
def check_conflicts():
    data = request.json

    # Validate required fields
    if "existing_events" not in data or "new_event" not in data:
        return jsonify({"error": "existing_events and new_event fields are required"}), 400

    existing_events = data.get("existing_events", [])
    new_event = data.get("new_event", {})

    # Check for conflicts between the new event and existing events
    conflicts = []
    for existing_event in existing_events:
        if events_overlap(new_event, existing_event):
            conflicts.append(existing_event)

    # Return the conflicting events
    return jsonify({
        "success": True,
        "message": "Conflicts processed successfully.",
        "conflicts": conflicts
    })

# Root route to display a message
@app.route('/')
def home():
    return "Flask Microservice for Event Alerts is Running!"


if __name__ == '__main__':
    app.run(debug=True)