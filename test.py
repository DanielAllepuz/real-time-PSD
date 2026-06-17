import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

from RTPSD import RealTimePSD

fs = 50e6
nperseg = 100
N = 10 * nperseg
np.random.seed(42)

detrend_types = [False, "constant", "linear"]
overlaps = [25, 50, 75]

plt.figure(figsize=(10, 5))
for l, overlap in enumerate(overlaps):
    noverlap = int(nperseg*(overlap/100))
    for k, detrend in enumerate(detrend_types):
        plt.subplot(len(detrend_types), len(overlaps), l+1 +k*len(overlaps))
        s = np.random.normal(size=N)

        rPSD = RealTimePSD(fs, nperseg, noverlap=noverlap, detrend=detrend)

        i = 0

        while i < len(s): # Data is fed to the PSD randomly
            j = i + int(np.random.uniform(0, N))
            j = min(N, j)
            rPSD.add_data(s[i:j])
            i = j

        freqs_RT, PSD_RT = rPSD.get_PSD()

        freqs, PSD = welch(s, fs, nperseg=nperseg, noverlap=noverlap, detrend=detrend)

        print(f"Detrend: {detrend}, Overlap: {overlap}%")
        assert np.allclose(PSD, PSD_RT)

        plt.plot(freqs, PSD, label="Scipy Welch", linewidth=4, alpha=0.5)
        plt.plot(freqs_RT, PSD_RT, label="RealTimePSD", linewidth=2, linestyle='--')
        plt.title(f"Detrend: {detrend}, Overlap: {overlap}%")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Density (V$^2$/Hz)")
        plt.legend()
        plt.grid(True)

plt.tight_layout()
plt.show()
