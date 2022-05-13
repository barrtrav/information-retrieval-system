# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IndexDocument(models.Model):
    lexer = models.TextField()
    title = models.TextField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'index_document'


class IndexRatings(models.Model):
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'index_ratings'


class IndexToken(models.Model):
    lexer = models.CharField(primary_key=True, max_length=20)
    documents = models.TextField()
    frequency = models.TextField()
    max_freq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'index_token'
