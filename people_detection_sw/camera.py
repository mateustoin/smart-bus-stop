import cv2
import numpy as np

# Load YOLO model (consider using yolov3-tiny for better performance)
net = cv2.dnn.readNet("./yolov4-tiny.weights", "./yolov4-tiny.cfg")

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

layer_names = net.getLayerNames()
output_layer_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

while True:
    # Read frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize the frame to a smaller size for faster detection
    (height, width) = frame.shape[:2]
    resized_frame = cv2.resize(
        frame, (320, 320)
    )  # Reduce the resolution for faster detection

    # Define the neural network input
    blob = cv2.dnn.blobFromImage(
        resized_frame, 1 / 255.0, (320, 320), swapRB=True, crop=False
    )
    net.setInput(blob)

    # Perform forward propagation
    outputs = net.forward(output_layer_names)

    # Initialize lists for detected boxes, confidences, and class IDs
    boxes = []
    confidences = []
    class_ids = []

    # Loop over the output layers
    for output in outputs:
        # Loop over the detections
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Only consider 'person' class and high confidence detections
            if (
                class_id == 0 and confidence > 0.5
            ):  # Person class (COCO dataset ID) and confidence threshold
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Append to lists
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression to eliminate redundant overlapping boxes with lower confidences
    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, score_threshold=0.5, nms_threshold=0.4
    )

    # Initialize people counter after NMS
    people_count = len(indices)

    # Draw bounding boxes around the people
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]

            # Draw bounding box for each person detected
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = f"Person: {confidences[i]:.2f}"
            cv2.putText(
                frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )

    # Display the frame with detections
    cv2.imshow("Real-Time Detection", frame)

    # Show people count in terminal
    print(f"Number of people detected: {people_count}")

    # Exit on 'q' key press or if the user closes the window
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.getWindowProperty("Real-Time Detection", cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
