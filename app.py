
import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

DAILY_API_KEY = "37fe6398f5dba51a1a627144d8d1b3335875b06178db3eef7eb96aaecca9b99c"  # Replace with your actual API key
DAILY_BASE_URL = "https://api.daily.co/v1"

@app.route('/')
def index():
    return render_template('index.html')

# Create a new room
@app.route('/create-room', methods=['POST'])
def create_room():
    headers = {
        "Authorization": f"Bearer {DAILY_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "properties": {
            "enable_chat": True,
            "enable_screenshare": True,  # Enable screen sharing
        }
    }
    response = requests.post(f"{DAILY_BASE_URL}/rooms", headers=headers, json=data)

    if response.status_code == 200:
        room_data = response.json()
        room_url = room_data.get('url')
        room_id = room_data.get('name')  # Use the room name as ID
        return jsonify({"redirect_url": f"/rooms.html?room_url={room_url}&room_id={room_id}"})
    else:
        return jsonify({"error": "Failed to create room", "details": response.json()}), response.status_code


# Join a room
@app.route('/join-room', methods=['POST'])
def join_room():
    room_id = request.json.get('room_id')
    user_name = request.json.get('user_name', 'Guest')

    room_url = f"https://smartmeet.daily.co/{room_id}"
    return jsonify({"redirect_url": f"/rooms.html?room_url={room_url}&room_id={room_id}&user_name={user_name}"})

# Generate a token for a participant
@app.route('/generate-token', methods=['POST'])
def generate_token():
    room_id = request.json.get('room_id')
    is_owner = request.json.get('is_owner', False)  # Check if the user is the host
    headers = {
        "Authorization": f"Bearer {DAILY_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "properties": {
            "is_owner": is_owner  # Set host role if True
        }
    }

    response = requests.post(f"{DAILY_BASE_URL}/rooms/{room_id}/tokens", headers=headers, json=data)

    if response.status_code == 200:
        token_data = response.json()
        return jsonify({"token": token_data["token"]})
    else:
        return jsonify({"error": response.json()}), response.status_code

@app.route('/rooms.html')
def rooms():
    return render_template('room.html')

if __name__ == '__main__':
    app.run(debug=True)

