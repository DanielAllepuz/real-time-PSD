# Real Time PSD
A small Python class that calculates the Power Spectral Density as you feed data to it

## Installation
There is no module at this moment, just copy `RTPSD.py` to your project folder.

## How to use
Instantiate `RealTimePSD`. The parameters (and their defaults) are the same as [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html), although not all of them are implemented (see below).
```python
# Create the object
rt_psd = RealTimePSD(samplerate, nperseg, noverlap=nperseg, window="hann_periodic", detrend="constant")
# Feed data
rt_psd.add_data(values)
# Check if a new estimate has been calculated from the new data
if rt_psd.new_estimate:
  freqs, psd = rt_psd.get_PSD() # Get the PSD estimate
else:
  # You can get the PSD estimate even if it has not been updated from the previous data, as long as at least nperseg values have been fed to RealTimePSD
  pass
```

## Parameters
The following parameters are implemented:
* `fs`: same as [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)
* `window`: same as [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)
* `nperseg`: same as [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)
* `noverlap`: same as [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)
* `detrend`: same as [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)
* `return_onesided`: same as [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)
### What's not implemented
The following parameters of [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html) are not currently implemented.
* ~`nfft`~: the length of the FFT is always `nperseg`
* ~`scaling`~: the units of the PSD are always of the form unit^2/Hz (default of [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html))
* ~`axis`~: not very useful in this case.
* ~`average`~: the mean is used, in contrast to the median (default of [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)).

## Testing
The code is tested against [`scipy.signal.welch`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html). Running `test.py` asserts that the result of `RealTimePSD` and `scipy.signal.welch` is the same.
