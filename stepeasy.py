from machine import Pin
import time

pins = [
    [
        Pin(0, Pin.OUT),
        Pin(1, Pin.OUT),
        Pin(2, Pin.OUT),
        Pin(3, Pin.OUT)  
    ],
    [
        Pin(4, Pin.OUT),
        Pin(5, Pin.OUT),
        Pin(6, Pin.OUT),
        Pin(7, Pin.OUT)  
    ],
    [
        Pin(8, Pin.OUT),
        Pin(9, Pin.OUT),
        Pin(10, Pin.OUT),
        Pin(11, Pin.OUT)  
    ]
]

full_step_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

def turn(motor, count, speed=1, pause_ms=500):
    for _ in range(512*abs(count)/4):
        if count < 0:
            for step in reversed(full_step_sequence):
                for j, p in enumerate(motor):
                    p.value(step[j])
                    time.sleep_ms(int(1/speed))
        else:
            for step in full_step_sequence:
                for j, p in enumerate(motor):
                    p.value(step[j])
                    time.sleep_ms(int(1/speed)) 
    time.sleep_ms(pause_ms)

turn(pins[0], 1)

turn(pins[0], -1)