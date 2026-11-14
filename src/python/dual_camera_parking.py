import cv2
import serial
import time
from ultralytics import YOLO

# ---------------- CONFIGURATION ----------------
SERIAL_PORT = "COM8"
BAUD_RATE = 9600
ENTRY_CAMERA_INDEX = 1
EXIT_CAMERA_INDEX = 2
FRAME_WIDTH, FRAME_HEIGHT = 640, 480
MODEL_PATH = "yolov8n.pt"
CONFIDENCE = 0.40
LINE_X = FRAME_WIDTH // 2
CROSSING_DIRECTION = "right_to_left"


def open_camera(index, name):
    cam = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not cam.isOpened():
        raise RuntimeError(f"{name} camera could not open at index {index}")
    return cam


def send(arduino, command):
    arduino.write((command + "\n").encode("utf-8"))


def crossings_for_result(result, previous_x, counted_ids):
    """Return new right-to-left person crossings and whether a person is visible."""
    crossings = 0
    visible = False
    if result.boxes is None or result.boxes.id is None:
        return crossings, visible

    ids = result.boxes.id.int().cpu().tolist()
    classes = result.boxes.cls.int().cpu().tolist()
    boxes = result.boxes.xyxy.cpu().tolist()

    for track_id, cls_id, coords in zip(ids, classes, boxes):
        if cls_id != 0:
            continue
        visible = True
        x1, y1, x2, y2 = coords
        center_x = int((x1 + x2) / 2)

        if track_id in previous_x and track_id not in counted_ids:
            old_x = previous_x[track_id]
            if CROSSING_DIRECTION == "right_to_left":
                crossed = old_x > LINE_X and center_x <= LINE_X
            else:
                crossed = old_x < LINE_X and center_x >= LINE_X
            if crossed:
                crossings += 1
                counted_ids.add(track_id)

        previous_x[track_id] = center_x

    return crossings, visible


def annotate(frame, title, color, available=None, occupied=None, total=None):
    h, w = frame.shape[:2]
    x = min(LINE_X, w - 1)
    cv2.line(frame, (x, 0), (x, h - 1), (255, 0, 0), 2)
    cv2.putText(frame, "COUNT LINE", (max(5, x - 110), 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, title, (10, 35), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, color, 2)
    if available is not None:
        cv2.putText(frame, f"Available: {available}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Occupied: {occupied}/{total}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    return frame


def main():
    total_slots = int(input("Enter total parking slots: ").strip())
    if total_slots <= 0:
        raise ValueError("Total slots must be greater than zero.")

    occupied = 0
    available = total_slots
    last_available_sent = None
    last_gate_sent = None
    arduino = None
    entry_cam = None
    exit_cam = None

    print("Starting. Press R to reset or Esc to quit.")
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        entry_cam = open_camera(ENTRY_CAMERA_INDEX, "Entry")
        exit_cam = open_camera(EXIT_CAMERA_INDEX, "Exit")

        # Separate YOLO instances keep each camera's ByteTrack state independent.
        entry_model = YOLO(MODEL_PATH)
        exit_model = YOLO(MODEL_PATH)

        entry_previous, exit_previous = {}, {}
        entry_counted, exit_counted = set(), set()

        send(arduino, f"S{available}")
        send(arduino, "C")
        last_available_sent, last_gate_sent = available, "C"

        while True:
            ok1, frame1 = entry_cam.read()
            ok2, frame2 = exit_cam.read()
            if not ok1 or not ok2:
                print("Camera frame error. Check USB connections and indices.")
                break

            r1 = entry_model.track(
                frame1, persist=True, tracker="bytetrack.yaml",
                classes=[0], conf=CONFIDENCE, verbose=False
            )[0]
            r2 = exit_model.track(
                frame2, persist=True, tracker="bytetrack.yaml",
                classes=[0], conf=CONFIDENCE, verbose=False
            )[0]

            entry_events, entry_visible = crossings_for_result(
                r1, entry_previous, entry_counted
            )
            exit_events, _ = crossings_for_result(
                r2, exit_previous, exit_counted
            )

            if entry_events:
                accepted = min(entry_events, total_slots - occupied)
                occupied += accepted
                if accepted:
                    print(f"ENTRY +{accepted}; occupied={occupied}")

            if exit_events:
                removed = min(exit_events, occupied)
                occupied -= removed
                if removed:
                    print(f"EXIT -{removed}; occupied={occupied}")

            available = total_slots - occupied
            if available != last_available_sent:
                send(arduino, f"S{available}")
                last_available_sent = available

            # Gate is open only while a person is visible at entry and capacity exists.
            desired_gate = "O" if entry_visible and available > 0 else "C"
            if desired_gate != last_gate_sent:
                send(arduino, desired_gate)
                last_gate_sent = desired_gate

            # Warn only on a new entry crossing while full, not every frame.
            if available == 0 and entry_events > 0:
                send(arduino, "E")
                print("Full capacity: warning sent.")

            display1 = annotate(r1.plot(), "ENTRY CAMERA", (0, 255, 0),
                                available, occupied, total_slots)
            display2 = annotate(r2.plot(), "EXIT CAMERA", (0, 0, 255))
            cv2.imshow("Entry Camera - Right to Left", display1)
            cv2.imshow("Exit Camera - Right to Left", display2)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("r"), ord("R")):
                occupied = 0
                available = total_slots
                entry_previous.clear()
                exit_previous.clear()
                entry_counted.clear()
                exit_counted.clear()
                send(arduino, f"S{available}")
                send(arduino, "C")
                last_available_sent, last_gate_sent = available, "C"
                print(f"RESET; available={available}")
            elif key == 27:
                break

    finally:
        if entry_cam is not None:
            entry_cam.release()
        if exit_cam is not None:
            exit_cam.release()
        cv2.destroyAllWindows()
        if arduino is not None and arduino.is_open:
            try:
                send(arduino, "C")
            except serial.SerialException:
                pass
            arduino.close()


if __name__ == "__main__":
    main()
