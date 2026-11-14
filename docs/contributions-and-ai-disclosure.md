# Contributions and AI assistance disclosure

This draft distinguishes student-led work from AI-assisted implementation. The project owner should edit it to match the work actually performed.

## Student / project-owner contributions
Based on the development discussions, student-led work includes:
- Selecting and developing the project concept and intended application.
- Assembling the Arduino Uno, servo, LCD, LEDs, buzzer, push buttons, and wiring.
- Connecting and troubleshooting two USB webcams.
- Testing camera access and identifying the working indices (entry 1 and exit 2 on the development computer).
- Uploading Arduino sketches and running the Python application locally.
- Defining expected behavior: entry/exit camera roles, right-to-left crossing, slot display, gate behavior, manual controls, and full-capacity warning.
- Integrating the hardware and observing its behavior.

Retain only statements that accurately describe the student's own work.

## AI-assisted work
AI assistance was used to explain concepts, suggest and revise Arduino/Python code, troubleshoot reported errors, and prepare repository structure and documentation. The current code and text were drafted with AI assistance from the requirements and test observations discussed.

AI-generated code must be reviewed, understood, and validated by the project owner. The student remains responsible for final implementation, safety, correctness, and claims made in presentations or interviews.

## Validation status
This repository describes intended behavior and provides a test procedure. It does not claim that every feature in this snapshot has been re-tested on the physical build. Record actual test outcomes before presenting performance claims.

## Suggested interview explanation
"I developed and assembled the two-camera Arduino prototype and defined the expected system behavior. I used AI as a development assistant for code iteration, troubleshooting, and documentation, then integrated and tested the system on my hardware. I can explain the camera pipeline, tracking and line-crossing logic, serial protocol, and Arduino actuator control. I also understand that this prototype estimates occupancy from people crossing a line rather than recognizing vehicles."
