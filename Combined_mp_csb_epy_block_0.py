"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """    This block measures calculates the magnitude of peaks at three different frequencies,
            i.e. the carrier and lower and upper sidebands. The input is an FFT of the signal and the output is
            a 1x3 vector containing the peak values. 
         
            \n Parameters:
                    \n Length - Size of FFT. Bug with GNU radio means this may not update correctly. If it doesn't change the default value in the block definition
                    \n f1_ind - index of peak 1
                    \n f2_ind - index of peak 2
                    \n f3_ind - index of peak 3
                    \n searchSize - number of bins to consider around specified frequencies
    """

    def __init__(self, Length=1024, f1_ind=50,f2_ind=50,f3_ind=50,searchSize =10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='ThreeMax',   # will show up in GRC
            in_sig=[(np.float32,Length)],#(gr.sizeof_float*1)],
            out_sig=[(np.float32,3)]    
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.f1_ind= f1_ind
        self.f2_ind= f2_ind
        self.f3_ind= f3_ind
        self.Length = Length
        self.searchSize = searchSize
 

    def work(self, input_items, output_items):

        P1 = np.max( input_items[0][0][(self.f1_ind-self.searchSize):(self.f1_ind+self.searchSize)])
        P2 = np.max( input_items[0][0][(self.f2_ind-self.searchSize):(self.f2_ind+self.searchSize)])
        P3 = np.max( input_items[0][0][(self.f3_ind-self.searchSize):(self.f3_ind+self.searchSize)])

        top3 =np.array([P1,P2,P3])
        # print(top3)
        # vals = sorted_vec[:3]
        # #print(vals)
        # output_items[0][:]= vals
        output_items[0][:]= top3

        return len(output_items[0])

