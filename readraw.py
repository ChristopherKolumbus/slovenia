if True: ## load packages
    import numpy as np
    import matplotlib.pyplot as plt
    import thunderfish.dataloader as dl
    from scipy import signal
    from scipy.io.wavfile import write
    import time
    from numba import jit, int32, float64
    from pyaudio import play

hide = True
dofilt = True
doplot = True

def mygauss(dt,steps,sigma):
    time = np.arange(-dt*steps,dt*(steps+1),dt)
    mygauss = np.exp(-time**2/(2*sigma**2))
    mygauss = mygauss/np.sum(mygauss)
    return mygauss
@jit(int32[:](float64[:],float64))
def findpeaksJit(x,thresh=0.):
    peaks = np.zeros(len(x),dtype=np.int32)
    ind = range(1,len(x)-1)
    c = 0
    for i in ind:
        diffFwd = x[i+1]-x[i]
        diffBwd = x[i]-x[i-1]
        if diffFwd < 0 and diffBwd > 0 and x[i] > thresh:
            peaks[c] = i
            c += 1
    return peaks[:c]

read_start = 0
read_end = 10

with dl.open_data('2016/2016-07-24-1005/trace-3.raw',0.0,60.0) as data:
    if hide: # calculate Fs, dt, sample length, nyq, time axis ...
        Fs = data.samplerate
        dt = 1 / Fs
        samples = len(data)
        nyq = 0.5*Fs
        readout = data[round(read_start/dt):round(read_end/dt)]
        timeAx = np.arange(0,len(readout)*dt,dt)
        timeAx = timeAx[:len(readout)]  
    if dofilt:
        low = 6000/nyq
        high = 10000/nyq
        b, a = signal.butter(2, [low,high],btype='bandpass')
        readout = signal.filtfilt(b,a,readout)
    plt.figure()
    plt.psd(readout,Fs=Fs)

    plt.figure()
    if doplot:
        f, t, Sxx = signal.spectrogram(readout,fs=Fs,nperseg=32,noverlap=8,nfft=4096)#,return_onesided=True)
        freqSum = np.sum(Sxx,0)
        freqSumConv = np.convolve(freqSum,mygauss(dt,300,0.0001),mode='same')
        inds = findpeaksJit(freqSumConv,thresh=0.0001)
        #plt.pcolormesh(t,f,Sxx,cmap='inferno')
        #plt.ylim(7000,12000)
        play(np.array(readout))
        #plt.figure()
        plt.subplot(311)
        plt.plot(timeAx,readout)
        plt.subplot(312)
        plt.plot(t,freqSumConv)
        plt.plot(t[inds],freqSumConv[inds],'o')
        plt.subplot(313)
        plt.plot(t[inds[1:]],np.diff(t[inds]))
        plt.ylim(0,0.05)
        plt.figure()
        
        plt.show()
