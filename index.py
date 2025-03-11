from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage for events (replace with a database in production)
events = []

# Helper function to send notifications (mock implementation)
def send_notification(user_id, message):
    print(f"Sending notification to user {user_id}: {message}")
    # In a real application, integrate with an email/SMS service like Twilio or SendGrid.

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
    if "conflicts" not in data:
        return jsonify({"error": "conflicts field is required"}), 400

    conflicts = data.get("conflicts", [])

    # Log the conflicts (or send notifications)
    for conflict in conflicts:
        event1 = conflict.get("event1", {})
        event2 = conflict.get("event2", {})
        message = f"Conflict detected: {event1.get('title')} on {event1.get('event_date')} at {event1.get('event_time')} overlaps with {event2.get('title')} on {event2.get('event_date')} at {event2.get('event_time')}."
        print(message)  # Log the conflict (replace with actual notification logic)

    # Return a success response
    return jsonify({
        "success": True,
        "message": "Conflicts processed successfully.",
        "conflicts": conflicts
    })


if __name__ == '__main__':
    app.run(debug=True)