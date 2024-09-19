class StringX:
    def __init__(self, x):
        self.x = x

    @property
    def int(self):
        return int(round(float(self.x), 0))
