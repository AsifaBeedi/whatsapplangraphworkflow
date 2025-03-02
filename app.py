from flask import Flask, request, jsonify
from workflow import process_message_node
from asgiref.sync import async_to_sync

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is running! Send POST requests to /process_message"

@app.route('/process_message', methods=['POST'])
def process_message():  # Make this synchronous
    data = request.get_json()
    message = data.get('message', '')
    
    # Convert async function to sync
    sync_process = async_to_sync(process_message_node)
    response = sync_process(message)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)