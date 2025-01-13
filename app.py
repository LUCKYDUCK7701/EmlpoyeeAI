import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from thread_manager import ThreadManager
from assistant_manager import AssistantManager
import openai

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Load the secret key from the environment

# Flask route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to assist the employee
@app.route('/assist', methods=['POST'])
def assist():
    data = request.get_json()
    query = data.get('query')

    # Create or retrieve the user's thread
    thread_manager = ThreadManager()
    thread_manager.create_thread()

    # Add message and run assistant
    thread_manager.add_message_to_thread(role="user", content=f"Help employee with this query: {query}?")
    summary = thread_manager.run_assistant(assistant_id=AssistantManager.assistant_id, instructions=f"Help employee with this query: {query}")

    return jsonify({'summary': summary})


if __name__ == '__main__':
    # Instantiate the assistant manager (only creates assistant once)
    assistant_manager = AssistantManager()

    try:
        # Simulate vector store creation (if not supported in SDK)
        vector_store = {"id": "simulated_vector_store", "name": "Org Docs"}
        print(f"Simulated vector store created: {vector_store}")

        # Ready the files for upload to OpenAI
        file_paths = ["org-data/organization_info.txt"]
        file_streams = [open(path, "rb") for path in file_paths]

        # Simulate file upload
        file_batch = {"status": "completed", "files": [path for path in file_paths]}
        print(f"Simulated file batch uploaded: {file_batch}")

        # Associate the vector store with the assistant
        assistant_manager.assistant["tool_resources"] = {
            "file_search": {"vector_store_ids": [vector_store["id"]]}
        }
        print(f"Simulated assistant updated with vector store: {assistant_manager.assistant}")

    except Exception as e:
        print(f"Error setting up vector store or file batch: {e}")

    # Run the Flask application
    app.run(debug=True)
