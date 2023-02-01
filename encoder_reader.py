import pyb

ENC_MAX = 0xFFFF

class EncoderReader:
    count = 0
    last_raw_cnt = 0
    def __init__(self, pin_a, pin_b, timer):
        """!
        Creates an encoder reader on the passed pin names and
        timer number.
        @param pin_a (There will be several pin parameters)
        @param
        """
        # https://github.com/dhylands/upy-examples/blob/master/encoder2.py
        pa = pyb.Pin(pin_a, mode=pyb.Pin.IN)
        pb = pyb.Pin(pin_b, mode=pyb.Pin.IN)

        self.tim = pyb.Timer(timer, prescaler=0, period=ENC_MAX)
        self.ch_1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=pa)
        self.ch_2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=pb)

    def read(self):
        cnt = self.tim.counter()

        delta = cnt - self.last_raw_cnt

        # Overflow max -> min
        if delta > ENC_MAX // 2:
            delta = ENC_MAX - delta

        # Overflow min -> max
        elif delta < -ENC_MAX // 2:
            delta = -ENC_MAX - delta

        self.count += delta
        self.last_raw_cnt = cnt

        return self.count

    def zero(self):
        self.count = 0
