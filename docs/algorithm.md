# Detection and counting algorithm

1. YOLOv8 Nano processes each camera frame and the pipeline retains only COCO class 0 (person).
2. Each camera has an independent tracker. The centroid is calculated as (x1 + x2) / 2.
3. A vertical line is positioned at LINE_X, initially the middle of a 640-pixel frame.
4. Both camera views are configured for right-to-left movement. A crossing occurs when previous_x > LINE_X and current_x <= LINE_X.
5. A tracked ID is added to a counted-ID set after its crossing, preventing repeated counting of that same track during the current run.
6. Entry camera crossing increments occupancy; exit camera crossing decrements it.
7. Occupancy is clamped to 0..total_slots. Available slots = total_slots - occupied.
8. Python sends the updated slot count to Arduino. If a person is visible at entry and capacity remains, the gate is requested open; otherwise it is requested closed.
9. When full, a new entry crossing triggers command E and the Arduino plays two beeps.

## Critical assumption
This is person-crossing-based occupancy estimation, not vehicle recognition. A pedestrian or passenger can affect the count, and multiple occupants of one vehicle can create errors. A production parking system should detect vehicles or use individual bay occupancy sensors.
