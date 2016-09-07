from django.db import models


class Logs():
    pass


class Truck(models.Model):
    truck_name = models.CharField(max_length=200)
    truck_driver = models.CharField(max_length=200)
    truck_log = Logs()


class MapModelGeneral(models.Model):
    # Every map instance works with a given time interval
    ini_time = models.DateTimeField('Ini time')
    end_time = models.DateTimeField('End time')
    time_span = (ini_time, end_time)

    # The information about position is fetched from the truck class
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
