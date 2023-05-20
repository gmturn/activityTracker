class Time:
    def __init__(self, date, hh, mm):
        if hh <= 24 and mm <= 59:
            self.date = date
            self.hh = int(hh)
            self.mm = int(mm)
            self.completeTime = f"{self.date} {self.hh}:{self.mm}"

        else:
            raise ValueError(
                f"Error: Time Model was given incorrect hh or mm value: {hh}:{mm}.")

    def __str__(self):
        return self.completeTime
