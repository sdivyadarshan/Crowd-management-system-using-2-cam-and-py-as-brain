# Testing checklist and observations

Only mark a test passed after performing it on the assembled hardware. No measured accuracy or latency is claimed in this repository.

## Hardware
- [ ] Uno uploads successfully and appears on the expected COM port.
- [ ] LCD starts and displays the expected message.
- [ ] LCD address is verified (0x27 default; some modules use 0x3F).
- [ ] Servo defaults to closed.
- [ ] Red and green LEDs indicate closed and open states.
- [ ] Manual open works when slots are available.
- [ ] Manual close closes the gate.
- [ ] E command produces exactly two beeps.
- [ ] Servo has a suitable supply and common ground.

## Vision
- [ ] Entry camera opens at configured index.
- [ ] Exit camera opens at configured index.
- [ ] Both video streams are stable at the selected resolution.
- [ ] Person bounding boxes appear.
- [ ] Non-person objects do not affect occupancy.
- [ ] Right-to-left entry crossing increments once.
- [ ] Right-to-left exit crossing decrements once.
- [ ] A person staying on one side is not repeatedly counted.
- [ ] Occlusion and multiple simultaneous people are evaluated.

## Integration
- [ ] Python connects to the Uno at 9600 baud.
- [ ] Available slots display correctly.
- [ ] Gate opens only under the configured entry-presence and capacity conditions.
- [ ] Gate closes when entry person is no longer detected.
- [ ] Entry crossing while full leaves count unchanged and triggers two beeps.
- [ ] R resets available slots to total capacity.
- [ ] Esc releases both cameras and serial connection.

## Observation log

| Date | Scenario | Expected | Actual | Result |
|---|---|---|---|---|
| TBD | Single entry crossing | Occupancy +1 | Not recorded | Not tested |
| TBD | Single exit crossing | Occupancy -1 | Not recorded | Not tested |
| TBD | Entry while full | No increment; two beeps | Not recorded | Not tested |
| TBD | Reset | Available = total | Not recorded | Not tested |

For stronger validation, measure precision/recall, crossing-count error, missed/duplicate events, end-to-end latency, frame rate, and continuous runtime. Record sample size and conditions.
