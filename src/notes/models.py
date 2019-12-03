from django.db import models
from django.utils import timezone
from django.conf import settings


class Label(models.Model):
    text = models.CharField(max_length=150)

    def __str__(self):
        return ' Label ' + self.pk


class Note(models.Model):
    title = models.CharField(max_length=950, blank=True, null=True)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='NoteConfig')

    def __str__(self):
        return ' Note ' + str(self.pk)


class NoteConfig(models.Model):
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
    is_archive = models.BooleanField(default=False)
    is_pin = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=1, choices=COLORS, default=white)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    labels = models.ManyToManyField(to=Label, blank=True)
    trash_delete_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('order', 'pk')

    def __str__(self):
        return 'Note Config note ' + str(self.note.id) + ' user ' + str(self.user.id)


class NoteContent(models.Model):
    done = 'T'
    not_done = 'F'
    is_not_checklist = 'N'

    STATUS_CHOICES = (
        (is_not_checklist, 'Is Not A Checklist'),
        (done, 'Done'),
        (not_done, 'Not Done'),
    )

    order = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=is_not_checklist)
    text = models.CharField(max_length=950)
    note = models.ForeignKey(to=Note, on_delete=models.CASCADE)

    class Meta:
        ordering = ('order', 'pk')

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
