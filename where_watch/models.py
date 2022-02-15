from turtle import pos
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Site(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=60, null=False, unique=True)
    url = fields.CharField(max_length=255, null=False, unique=True)


class SiteLink(models.Model):
    id = fields.IntField(pk=True)
    link = fields.CharField(max_length=255)
    site = fields.ForeignKeyField('models.Site', related_name='sites')


class Series(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, null=False, unique=True)
    title_eng = fields.CharField(max_length=255, null=False, unique=True)
    poster = fields.CharField(max_length=255)
    premiere_date = fields.DateField()
    update_date = fields.DateField()
    links = fields.ManyToManyField(
        'models.SiteLink', related_name='links', through='series_links')
