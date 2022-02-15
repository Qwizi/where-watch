from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, unique=True)


class SiteLink(models.Model):
    url = models.CharField(max_length=255, unique=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)


class SeriesMixin(models.Model):
    title_eng = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, unique=True)
    poster = models.CharField(max_length=255, unique=True)
    premiere_date = models.DateField()
    update_date = models.DateField(auto_now=True)
    links = models.ManyToManyField(SiteLink)

    class Meta:
        abstract = True


class Series(SeriesMixin):
    pass


class Movie(SeriesMixin):
    pass
