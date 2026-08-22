import utime
from machine import Pin

def main(): 
    t = Stepper(3, 4, 5)
    
    for _ in range(48):
        t.turn(1)

class Stepper:
    def __init__(self, step_pin, dir_pin, en_pin):
        self.steps_per_turn = 50
        self.step = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)
        self.en = Pin(en_pin, Pin.OUT)
        self.steps_per_rev = 200
        self.delay = 1/500
        self.wait = 0.125

    def set_speed(self, speed):
        self.delay = 1 / abs(min(speed, 500))  # delay in seconds

    def turn(self, amount):
        #turn on
        self.en.value(0)
        self.dir.value(int(amount < 0))
        for _ in range(abs(amount)*self.steps_per_rev/4):
            self.step.value(1)
            utime.sleep(self.delay)
            self.step.value(0)
        utime.sleep(self.wait)
        #turn off
        self.en.value(1)

        

if __name__ == "__main__":
    main()