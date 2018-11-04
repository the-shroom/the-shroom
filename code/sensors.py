import Adafruit_DHT

for port in range(1,22):
    print('Reading port ', port)
    rh, T = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, port)
    print(rh, T)