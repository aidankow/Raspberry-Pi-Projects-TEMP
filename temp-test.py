import explorerhat, time

while True:
    analog_value = explorerhat.analog.one.read()
    voltage = analog_value * 3.3
    temp_c = (voltage - 0.5) * 100
    print("Temperature: ", round(temp_c, 2), "°C")
    if temp_c > 30:
        explorerhat.output.one.on()
        time.sleep(2)
        explorerhat.output.one.off()
    time.sleep(2)

