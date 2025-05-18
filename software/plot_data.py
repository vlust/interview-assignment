import serial, time
import matplotlib.pyplot as plt
from collections import deque

SERIAL_PORT = 'COM5'
BAUDRATE = 115200
WINDOW = 60  # seconds

def main():
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    data = deque()
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], '-o')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Current (mA)")
    start = time.time()

    while True:
        raw = ser.readline().decode().strip()
        if not raw: continue
        t, current = map(float, raw.split(","))
        data.append((t, current))
        # keep last 60s
        while data and data[0][0] < t - WINDOW:
            data.popleft()

        xs, ys = zip(*data)
        line.set_data(xs, ys)
        ax.set_xlim(max(0, t - WINDOW), t + 1)
        ax.set_ylim(3.5, 20.5)
        fig.canvas.draw()
        fig.canvas.flush_events()

if __name__ == '__main__':
    main()
