from flask import Flask, request, jsonify
from face_recognition import capture_face, recognize_faces

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    student_name = data.get("name")

    if not student_name:
        return jsonify({"error": "Name is required"}), 400

    capture_face(student_name)
    return jsonify({"message": f"Face captured for {student_name}"}), 200

@app.route('/recognize', methods=['GET'])
def recognize():
    recognize_faces()
    return jsonify({"message": "Face recognition completed"}), 200

if __name__ == '__main__':
    app.run(debug=True)
