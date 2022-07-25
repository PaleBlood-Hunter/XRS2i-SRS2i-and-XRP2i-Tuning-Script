import serial
import time
import sys
import os
import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path

ser = serial.Serial(timeout = 0.2)
TTTT = []

print("Please, inpiut the COM port number you are using: (e.g: 'COM4')")
user_port = input("")
print("Please, insert the baudrate of your reader")
user_baudrate = input("")


ser.baudrate = user_baudrate
ser.port = user_port
ser.open()

ser.write(bytes(b'{TTTT}'))

csv_path = Path(__file__).parent.joinpath('{TTTT}.csv')
if csv_path.is_file():
    os.remove(csv_path)


for i in range(63):
    buffer = ser.read_until(b']').decode('UTF-8')
    if buffer != "":
        TTTT.append(buffer)



df = pd.DataFrame(TTTT, columns=["TTTT"])
df = df.replace(r'\n','', regex=True)
df = df.replace(r'\r','', regex=True)
df.to_csv('{TTTT}.csv', index=False)


plt.rcParams["figure.autolayout"] = True
columns = ["TTTT",]
df = pd.read_csv("{TTTT}.csv", usecols=columns)

df = df["TTTT"].str[4:]

df = df.str.split()

for x in df:
    del x[2]

TV, Frequency = map(list, zip(*df))

y = 0
for x in TV:
    TV[y] = int(TV[y])
    y = y + 1

y = 0
for x in Frequency:
    Frequency[y] = int(Frequency[y])
    y = y + 1


plt.title("{TTTT} tune Test -Resonant Frequency vs. Tuning Step")
plt.xlabel("Tuning Value")
plt.ylabel("Frequency (HZ)")

plt.plot(TV, Frequency)
plt.show()

ser.write(bytes(b'{TV}'))

ser.close()
