from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []  # In-memory list of tasks

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    tasks.append(data)
    return jsonify({'message': 'Task added!'}), 201

@app.route('/tasks/<int:index>', methods=['PUT'])
def update_task(index):
    if index < 0 or index >= len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    tasks[index] = data
    return jsonify({'message': 'Task updated!'})

@app.route('/tasks/<int:index>', methods=['DELETE'])
def delete_task(index):
    if index < 0 or index >= len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    tasks.pop(index)
    return jsonify({'message': 'Task deleted!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


