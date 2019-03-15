#import two files, solenoid and water sensor
import multithreading, datetime

solenoid_valve = solen.solenoid(16)
water_sensor = wat.sensor(27,26)

class control_mechanism(threading.Thread):
    import time
    total_time = 0
    current_time = 0
    pause = False
    exit_cond = False
    solenoid_status = False
    solenoid = None
    def __init__(self, tt, sol):
        self.total_time = tt
        solenoid = sol
        threading.Thread.__init__(self)
    def run(self):
        while self.current_time < self.total_time and self.exit_cond is False:
            while self.pause is False and self.current_time < self.total_time and self.exit_cond is False:
                time_start = time.time()
                if self.solenoid_status is False:
                    self.solenoid.open()
                    self.solenoid_status = True
                time.sleep(0.001)
                time_end = time.time()
                self.current_time = self.current_time + time_end - time_start
            self.solenoid.close()
            self.solenoid_status = False
    def set_pause(self,status):
        self.pause = status
    def get_solenoid_status(self):
        return solenoid_status        

input("Press enter to start ::")

scheduled_time = 3000

scheduled_days = [0,0,0,0,0,0,0]

scheduled_days[2] = 1
scheduled_time = 15*60
exit_cond = False
while not exit_cond:
    today = datetime.datetime.today().weekday()
    if scheduled_days[today]:
        cm = control_mechanism(scheduled_time)
    time.sleep(600)



 

