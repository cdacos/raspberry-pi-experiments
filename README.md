# 2020 Notes

https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

```
sudo adduser carlos gpio
sudo adduser carlos i2c
sudo adduser carlos spi
```

```
source .venv/bin/activate
python blinkatest.py

gunicorn --bind 0.0.0.0:5000 web:app
```

---
# 2018 Notes

Reset GPIO

```
sudo python energie.py
```

socket 2 on (1110)

```
sudo python energie.py 1110
```

socket 1 on (1111) and off (0111)

```
sudo python energie.py 11110111
```

socket 2 on (1110) and off (0110)

```
sudo python energie.py 11100110
```

all sockets on (1011) and off (0011)

```
sudo python energie.py 10110011
```

AM2302 (DHT22)

Requires https://github.com/adafruit/Adafruit_Python_DHT

