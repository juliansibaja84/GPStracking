from django.db import models


class Logs(models.Model):
    datetime = models.DateTimeField('Syrus registered time')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)


class Truck(models.Model):
    driver = models.CharField(max_length=200)
    log = models.ForeignKey(Logs, on_delete=models.CASCADE)


class MapModelGeneral(models.Model):
    # Every map instance works with a given time interval
    ini_time = models.DateTimeField('Ini time')
    end_time = models.DateTimeField('End time')
    time_span = (ini_time, end_time)

    # The information about position is fetched from the truck class
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
