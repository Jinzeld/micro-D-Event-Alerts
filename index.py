from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage for events (replace with a database in production)
events = []

# Helper function to check if two events overlap
def events_overlap(event1, event2):
    return not (event1['end_time'] <= event2['start_time'] or event1['start_time'] >= event2['end_time'])

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
        event_time = datetime.fromisoformat(event['start_time'])
        if now <= event_time <= now + timedelta(hours=24):
            upcoming_events.append(event)

    # Send notifications for upcoming events
    for event in upcoming_events:
        message = f"Reminder: You have an upcoming event - {event['title']} at {event['start_time']}."
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
        message = f"Conflict detected: {event1['title']} at {event1['start_time']} overlaps with {event2['title']} at {event2['start_time']}."
        send_notification(user_id, message)

    return jsonify({"success": True, "conflicts": conflicts})

# Add an event (for testing purposes)
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json
    events.append(data)
    return jsonify({"success": True, "event": data})

if __name__ == '__main__':
    app.run(debug=True)