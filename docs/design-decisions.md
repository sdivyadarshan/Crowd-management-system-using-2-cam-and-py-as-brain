# Design decisions

- **Two cameras:** Entry and exit are observed from separate physical positions.
- **Python vision processing:** YOLO and OpenCV run on the computer; the Uno lacks the compute and memory for this workload.
- **Arduino actuation:** The Uno receives compact serial commands and handles servo, display, LEDs, buzzer, and buttons.
- **Vertical crossing line:** The camera arrangement produces horizontal movement in the image, so a vertical line is used.
- **Directional transition:** The algorithm compares previous and current centroids rather than counting any person merely found on one side of the line.
- **Person-only filter:** Other object classes do not contribute to the occupancy estimate.
- **Closed startup state:** The servo is commanded closed during Arduino startup.
- **Volatile count:** The current count resets on Python restart; persistent storage is not implemented.
- **Manual controls:** Local button actions can be superseded by later serial commands while Python is running.
