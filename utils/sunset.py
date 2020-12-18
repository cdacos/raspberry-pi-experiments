#!/bin/python
# pip install astral

from astral import Astral

city_name = 'London'

a = Astral()
a.solar_depresion = 'civil'
city = a[city_name]
sun = city.sun(local=True)

sunset = sun['sunset']

print(type(sunset))
print(sunset)

