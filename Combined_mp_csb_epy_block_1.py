"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class PhaseDiff(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """This block measures the phase shift between two signals of the same frequency. 
            The inputs are the FFTs of each signal. The phase shift is calculated by measuring the 
            argument of the maximum correlation between the two inputs in a small region around 
            the frequency of interest. 
         
            \n Parameters:
                    \n Length - Size of FFT. Bug with GNU radio means this may not update correctly. If it doesn't change the default value in the block definition
                    \n CenterFreq - FFT center frequency
                    \n SignalFreq - Frequency of signal
                    \n BW - Bandwidth to consider, (Hz)
                    \n samp_rate - Sampling rate"""

    def __init__(self, Length = 1024,CenterFreq = 0,SignalFreq = 0,BW=0,samp_rate = 1000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Calculate Phase Shift',   # will show up in GRC
            in_sig=[(np.complex64, Length),(np.complex64, Length)],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        
        self.signal_ind = int((Length/samp_rate)*(SignalFreq-CenterFreq)+Length/2)
        self.Start = int((Length/samp_rate)*(SignalFreq-CenterFreq-BW)+Length/2)
        print("Start Index: ",self.Start,"\n")
        self.End = int((Length/samp_rate)*(SignalFreq-CenterFreq+BW)+Length/2)
        print("Stop Index: ",self.End,"\n")
        self.Length =Length
        self.CenterFreq = CenterFreq
        self.SignalFreq = SignalFreq
        self.BW = BW
        self.samp_rate = samp_rate

    def work(self, input_items, output_items):
        #print("In0 size FFT @ f0:   ",np.shape(input_items[0][0][self.Start:self.End]),"\n")
        #print("In1 size FFT @ f0:   ",np.shape(input_items[1][0][self.Start:self.End]),"\n")
        if self.BW!=0:
            crltn = np.correlate(input_items[0][0][self.Start:self.End],input_items[1][0][self.Start:self.End])
        else:
            crltn = input_items[0][0][self.Start]*input_items[1][0][self.Start]
        #crltn = np.correlate(input_items[0][0][self.signal_ind],input_items[1][0][self.signal_ind])

        diff = np.angle(crltn)
       
        output_items[0][:] = diff

        return len(output_items[0])
