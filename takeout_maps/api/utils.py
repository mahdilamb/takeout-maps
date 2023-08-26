from annotated_types import Interval


class ValidatableInterval(Interval):
    def __call__(self, val):
        # TODO (Mahdi): gt,lt
        if self.ge is not None and val < self.ge:
            raise ValueError()
        if self.le is not None and val > self.le:
            raise ValueError()
        return val
