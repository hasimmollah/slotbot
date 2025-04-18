from django.db import models

class InterviewSlot(models.Model):
    company = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'start_time', 'company')

    def __str__(self):
        return f"Slot from {self.start_time} to {self.end_time}, Booked: {self.is_booked}"