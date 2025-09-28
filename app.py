from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (in-memory storage for simplicity)
tasks = [
    {"id": 1, "task": "Learn DevOps", "done": False},
    {"id": 2, "task": "Build CI/CD Pipeline", "done": False}
]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Task is required"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "task": data['task'],
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    if 'done' in data:
        task['done'] = data['done']

    return jsonify(task), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

