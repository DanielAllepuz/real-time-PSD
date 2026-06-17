# https://github.com/DanielAllepuz/real-time-PSD
import numpy as np
from scipy.signal.windows import get_window
from scipy.signal import detrend
import matplotlib.pyplot as plt

class RealTimePSD():
    def __init__(self, samplerate, nperseg, noverlap=None, window='hann', onesided=True, detrend='constant'):
        self.samplerate = samplerate
        self.nperseg = int(nperseg)
        self.overlap = int(noverlap) if noverlap is not None else self.nperseg//2
        self.step = self.nperseg - self.overlap
        self.detrend = detrend

        self.window = get_window(window, self.nperseg)
        self.onesided = onesided
        
        self.factor = 1 / (self.samplerate * np.sum(self.window**2))
        if self.onesided:
            self.factor *= 2

        if nperseg % 2 == 0:
            self.nfreqs = (self.nperseg // 2) + 1
        else:
            self.nfreqs = (self.nperseg + 1) // 2
        
        self.freqs = np.fft.rfftfreq(self.nperseg, 1/self.samplerate)

        self.non_avg_fft2 = np.zeros(self.nfreqs)
        self.averages = 0
        self.new_estimate = False

        # Buffer tracking
        self.buffer = np.zeros(2 * self.nperseg, dtype=np.float64)
        self.buffer_pos = 0
        self.cursor = 0
        self.samples_available = 0

    def add_to_PSD(self, values):
        if self.detrend == False:
            detrended_values = values
        else:
            detrended_values = detrend(values, type=self.detrend)
        
        self.non_avg_fft2 += np.abs(np.fft.rfft(detrended_values * self.window))**2
        self.averages += 1
        self.new_estimate = True

    def get_PSD(self):
        if self.averages == 0:
            return self.freqs, np.zeros(self.nfreqs)
            
        psd = (self.factor * self.non_avg_fft2) / self.averages
        
        if self.onesided:
            psd[0] /= 2.0
            if self.nperseg % 2 == 0:
                psd[-1] /= 2.0
        
        self.new_estimate = False
        return self.freqs, psd

    def add_data(self, values):
        idx = 0
        while idx < len(values):
            # Calculate how much space is left in the buffer to prevent overflow
            space_left = len(self.buffer) - self.samples_available
            chunk_size = min(len(values) - idx, space_left)
            
            # Safe circular buffer writing that handles wrap-around boundaries
            end_pos = self.buffer_pos + chunk_size
            if end_pos <= len(self.buffer):
                self.buffer[self.buffer_pos:end_pos] = values[idx:idx+chunk_size]
            else:
                part1 = len(self.buffer) - self.buffer_pos
                part2 = chunk_size - part1
                self.buffer[self.buffer_pos:] = values[idx:idx+part1]
                self.buffer[:part2] = values[idx+part1:idx+chunk_size]
            
            self.buffer_pos = (self.buffer_pos + chunk_size) % len(self.buffer)
            self.samples_available += chunk_size
            idx += chunk_size

            while self.samples_available >= self.nperseg:
                end_cursor = self.cursor + self.nperseg
                
                # Safe circular reading
                if end_cursor <= len(self.buffer):
                    segment = self.buffer[self.cursor:end_cursor]
                else:
                    part1 = len(self.buffer) - self.cursor
                    part2 = self.nperseg - part1
                    segment = np.concatenate((self.buffer[self.cursor:], self.buffer[:part2]))
                
                self.add_to_PSD(segment)
                
                # Advance read cursor by the step size (nperseg - overlap)
                self.cursor = (self.cursor + self.step) % len(self.buffer)
                self.samples_available -= self.step

