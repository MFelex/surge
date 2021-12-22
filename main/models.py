from django.db import models


class RequestDistrict(models.Model):
    created_time = models.DateTimeField('Create Time', auto_now_add=True)
    updated_time = models.DateTimeField('Updated Time', auto_now=True)
    district = models.PositiveSmallIntegerField('District', db_index=True)
    requested_time = models.DateTimeField('Requested Time', db_index=True)
    requested_count = models.PositiveBigIntegerField('Requested Count')

    class Meta:
        db_table = 'request_district'

    def __str__(self):
        return f'{self.district} - {self.requested_time} - {self.requested_count}'


class Threshold(models.Model):
    created_time = models.DateTimeField('Create Time', auto_now_add=True)
    updated_time = models.DateTimeField('Updated Time', auto_now=True)
    request_count = models.PositiveBigIntegerField('Request Count', unique=True)
    coefficient = models.FloatField('Coefficient')

    class Meta:
        db_table = 'threshold'

    def __str__(self):
        return f'{self.request_count} - {self.coefficient}'
