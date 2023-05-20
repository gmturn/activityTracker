class Date:
    def __init__(self, mm, dd, yyyy):
        if mm <= 12 and dd <= 31:
            self.mm = int(mm)
            self.dd = int(dd)
            self.yyyy = int(yyyy)
            self.completeDate = f"{self.mm}/{self.dd}/{self.yyyy}"

        else:
            raise ValueError(
                f"Error: dd or mm value is invalid: {mm}/{dd}/{yyyy}")

    def __str__(self):
        return self.completeDate
