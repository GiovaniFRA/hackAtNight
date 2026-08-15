from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Learn Flask", "completed": True}
]

# GET endpoint to retrieve all items
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

# POST endpoint to create a new item
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
        
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "completed": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

if __name__ == '__main__':
    app.run(debug=True)