import utime
from machine import Pin

def main(): 
    s = Stepper(0, 1, 2)
    s.turn(1, 4)
    s.turn(0, 4)
    s.turn(0, 3)

class Stepper:
    def __init__(self, step_pin, dir_pin, slp_pin):
        self.steps_per_turn = 50
        self.step = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)
        self.slp = Pin(slp_pin, Pin.OUT)

        self.slp.value(0)
        
    def turn(self, direction, amount = 1, speed = 0.002):

        #turn on
        self.slp.value(1)

        self.dir.value(direction)
        for _ in range(self.steps_per_turn*amount):
            self.step.value(1)
            utime.sleep_us(int(1/speed))
            self.step.value(0)
            utime.sleep_us(int(1/speed))
        utime.sleep_us(int(1/speed)*500)

        self.slp.value(0)

if __name__ == "__main__":
    main()