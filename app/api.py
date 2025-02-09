from flask import Flask, request, jsonify
import torch
import cv2
import numpy as np
from ultralytics import YOLO


app = Flask(__name__)

# Load YOLO model
model = YOLO("app/model/best.pt")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    # Run inference
    results = model(image)
    detections = []

    class_names = [
        "Malaysian Water Monitor Lizard",
        "Clouded Monitor Lizard",
        "Dumeril's Monitor Lizard",
        "Basket Stinkhorn",
        "Bracket Fungi",
        "Geastrum Triplex",
        "Asian Hornet",
        "Giant Honey Bee",
        "Digger Bee"
    ]

    MIN_CONFIDENCE = 0.7

    for box in results[0].boxes:
        class_id = int(box.cls.item())
        bbox = [float(coord) for coord in box.xyxy[0].tolist()]
        confidence = float(box.conf.item())
        if confidence < MIN_CONFIDENCE:
            continue

        detections.append({
            "class_name": class_names[class_id],
            "confidence": confidence
        })

    return jsonify({"detections": detections})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
