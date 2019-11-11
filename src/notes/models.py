import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings


class Trash(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' Trash'


class Label(models.Model):
    text = models.CharField(max_length=150)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' Label ' + self.pk


class Note(models.Model):
    white = 'W'
    red = 'R'
    blue = 'B'
    green = 'G'
    yellow = 'Y'
    pink = 'P'
    violet = 'V'
    COLORS = (
        (white, 'White'),
        (red, 'Red'),
        (blue, 'Blue'),
        (green, 'Green'),
        (yellow, 'Yellow'),
        (pink, 'Pink'),
        (violet, 'Violet'),
    )
    title = models.CharField(max_length=950, blank=True, null=True)
    archive = models.BooleanField(default=False)
    pin = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)
    new = models.BooleanField(default=False)
    color = models.CharField(max_length=1, choices=COLORS, default=white)
    user = models.ManyToManyField(to=settings.AUTH_USER_MODEL)
    label = models.ManyToManyField(to=Label, blank=True)
    trash = models.ForeignKey(to=Trash, on_delete=models.PROTECT, blank=True, null=True)
    delete_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'pk']

    def __str__(self):
        return ' Note ' + str(self.pk)


class Item(models.Model):
    done = 'T'
    not_done = 'F'
    is_not_checklist = 'N'

    STATUS_CHOICES = (
        (is_not_checklist, 'Is Not A Checklist'),
        (done, 'Done'),
        (not_done, 'Not Done'),
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=is_not_checklist)
    text = models.CharField(max_length=950)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.note) + ' Item ' + str(self.pk)


class Image(models.Model):
    image = models.ImageField(upload_to='note_images')
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.note) + ' Image ' + str(self.pk)


class Reminder(models.Model):
    no_repeat = 'N'
    daily = 'D'
    weekly = 'W'
    monthly = 'M'
    yearly = 'Y'
    REPEAT_CHOICES = (
        (no_repeat, 'Does Not Repeat'),
        (daily, 'Daily'),
        (weekly, 'Weekly'),
        (monthly, 'Monthly'),
        (yearly, 'Yearly'),
    )
    date_and_time = models.DateTimeField(default=timezone.now)
    # TODO: add costume repeat schedule
    repeat = models.CharField(max_length=1, choices=REPEAT_CHOICES, default=no_repeat)
    note = models.OneToOneField(to=Note, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.note) + ' Reminder ' + str(self.pk)

