import pyb

from encoder_reader import EncoderReader


class MotorDriver:
    """!
    This class implements a motor driver for an ME405 kit.
    """

    def __init__(self, en_pin, in1pin, in2pin, timer):
        """!
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety.
        @param en_pin GPIO pin that enables the motor to run
        @param in1pin GPIO pin number for the first motor output pin
        @param in2pin GPIO pin number for the second motor output pin
        @param timer number that corresponds to passed motor GPIO
        """
        print("Creating a motor driver")
        # initialize GPIO
        self.enable_motor = pyb.Pin(en_pin, pyb.Pin.OUT_PP)
        self.pin_1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        self.pin_2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        self.timer = pyb.Timer(timer, freq=20000)
        self.ch_1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.pin_1)
        self.ch_2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.pin_2)
        # initialize the motors to have 0 speed
        self.enable_motor.value(True)
        self.ch_1.pulse_width_percent(0)
        self.ch_2.pulse_width_percent(0)

    def set_duty_cycle(self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed float holding the duty
                cycle of the voltage sent to the motor, -100-100
        """
        #
        if level < 0:
            level = level * -1
            self.ch_1.pulse_width_percent(0)
            self.ch_2.pulse_width_percent(level)
        elif level > 0:
            self.ch_1.pulse_width_percent(level)
            self.ch_2.pulse_width_percent(0)
        else:
            self.ch_1.pulse_width_percent(0)
            self.ch_2.pulse_width_percent(0)
            self.ch_2.pulse_width_percent(0)


if __name__ == '__main__':
    m1 = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    enc = EncoderReader(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    dir = 1
    level = 0
    while True:
        print(enc.read())
        pyb.delay(50)
        m1.set_duty_cycle(level)
        level += dir

        if level <= -100 or level >= 100:
            dir = -dir

