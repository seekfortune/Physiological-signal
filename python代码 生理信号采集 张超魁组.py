import serial
import matplotlib.pyplot as plt
import re

t = []
t_now = 0
data = []
all_heart = []
i = 0
dev = serial.Serial('COM2', 9600, timeout=1)

try:
    while True:
        num = dev.readline().decode()
        num = re.sub("\D", "", num)
        if not str.isdigit(num):
            continue
        num = int(num)
        data.append(num)
        t.append(i)
        while len(data) > 500:
            data.pop(0)
            t.pop(0)

        heart_ind = []
        count = 0

        for ind in range(len(data) - 1, 0, -1):
            if data[ind] > 600 and count < 3:
                if heart_ind and heart_ind[-1] - ind < 20:
                    continue
                count += 1
                heart_ind.append(ind)
        if len(heart_ind) == 3:
            all_heart.append((heart_ind[0] - heart_ind[-1]) / 3.5)
        else:
            all_heart.append(0)
        while len(all_heart) > 500:
            all_heart.pop(0)

        if i % 100 == 0:
            plt.clf()
            plt.subplot(2, 1, 1)
            plt.plot(t, data)
            plt.subplot(2, 1, 2)
            plt.plot(t, all_heart)
            plt.pause(0.001)
            plt.ioff()

        i += 1

except Exception:
    pass
finally:
    dev.close()
