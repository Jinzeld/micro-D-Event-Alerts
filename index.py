from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage for events (replace with a database in production)
events = []

# Helper function to check if two events overlap
def events_overlap(event1, event2):
    # Combine date and time for both events
    event1_start = datetime.fromisoformat(f"{event1['event_date']}T{event1['event_time']}")
    event1_end = event1_start + timedelta(hours=1)  # Assuming each event lasts 1 hour
    event2_start = datetime.fromisoformat(f"{event2['event_date']}T{event2['event_time']}")
    event2_end = event2_start + timedelta(hours=1)  # Assuming each event lasts 1 hour

    return not (event1_end <= event2_start or event1_start >= event2_end)

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
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Fetch events for the user (replace with a database query)
    user_events = [event for event in events if event['user_id'] == user_id]

    # Check for conflicts
    conflicts = []
    for i in range(len(user_events)):
        for j in range(i + 1, len(user_events)):
            if events_overlap(user_events[i], user_events[j]):
                conflicts.append({
                    "event1": user_events[i],
                    "event2": user_events[j]
                })

    # Send notifications for conflicts
    for conflict in conflicts:
        event1 = conflict['event1']
        event2 = conflict['event2']
        message = f"Conflict detected: {event1['title']} on {event1['event_date']} at {event1['event_time']} overlaps with {event2['title']} on {event2['event_date']} at {event2['event_time']}."
        send_notification(user_id, message)

    return jsonify({"success": True, "conflicts": conflicts})

# Add an event (for testing purposes)
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json

    # Validate required fields
    required_fields = ['user_id', 'title', 'event_date', 'event_time']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Add the event to the in-memory list
    events.append(data)
    return jsonify({"success": True, "event": data})

# Root route to display a message
@app.route('/')
def home():
    return "Flask Microservice for Event Alerts is Running!"


if __name__ == '__main__':
    app.run(debug=True)