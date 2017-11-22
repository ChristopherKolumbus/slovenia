import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

dt = 0.001

t_steps = np.arange(0, 1, dt)
a_sig = np.sin(2*np.pi*t_steps*4+5)
b_sig = np.sin(2*np.pi*t_steps*4)
lag = np.argmax(signal.correlate(a_sig, b_sig))
#corr = signal.correlate(a_sig, b_sig)
c_sig = np.roll(b_sig, shift=int(np.ceil(lag)))

plt.plot(a_sig)
plt.plot(b_sig)
plt.plot(c_sig)
plt.show()