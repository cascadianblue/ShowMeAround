from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import ForeignKey, TextField, CharField, FloatField
from django.db.models.base import Model
from django.db.models.fields import BooleanField, IntegerField, DateTimeField, EmailField
from django.db.models.fields.related import ManyToManyField


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', ]

    objects = UserManager()
    username = CharField(unique=True, max_length=30)
    email = EmailField(unique=True)
    name = CharField(max_length=100, blank=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_guide = BooleanField(default=False)
    date_joined = DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_best_identifier(self):
        return self.name if self.name else self.username

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_detail_url(self):
        return reverse_lazy('guides:user.detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse_lazy('guides:user.edit', kwargs={'pk': self.pk})

    def get_rating(self):
        if self.reviews.count():
            return sum([float(review.stars) for review in self.reviews.all()]) / float(self.reviews.count())  # TODO: test this
        else:
            return None

    def __str__(self):
        return ('Guide - %s' if self.is_guide else 'Tourist - %s') % self.name


class Tour(Model):
    title = TextField()
    description = TextField()

    guide = ForeignKey(User, related_name='guided_tours')
    tourists = ManyToManyField(User, related_name='taken_tours', blank=True)
    capacity = IntegerField()

    start_time = DateTimeField()
    end_time = DateTimeField()

    latitude = FloatField()
    longitude = FloatField()

    price = FloatField()

    def get_detail_url(self):
        return reverse_lazy('guides:tour.detail', kwargs={'pk': self.pk})

    def get_join_url(self):
        return reverse_lazy('guides:tour.join', kwargs={'pk': self.pk})

    def get_leave_url(self):
        return reverse_lazy('guides:tour.leave', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return self.get_detail_url()

    def __str__(self):
        return self.title


class Review(Model):
    class Meta:
        unique_together = ('author', 'tour')
    title = CharField(max_length=255, blank=True)
    text = TextField(blank=True)
    author = ForeignKey(User, related_name='authored_reviews')
    tour = ForeignKey(Tour, related_name='reviews')
    subject = ForeignKey(User)
    stars = IntegerField()

    def __str__(self):
        return