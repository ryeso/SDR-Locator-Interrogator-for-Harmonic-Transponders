"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class CSB_calc(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """This block takes a 1x3 vector corresponding to the lower sideband, carrier, and upper sideband power
      in dB and calculates the C/SB ratio from the carrier and the average of the two sidebands."""

    def __init__(self,):  # only default arguments here
        """arguments to this function show up as parameters in GRC """
        gr.sync_block.__init__(
            self,
            name='C/SB Calculator',   # will show up in GRC
            in_sig=[(np.float32,3)],
            out_sig=[np.float32,np.float32,np.float32,np.float32]    
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).


    def work(self, input_items, output_items):
        LSB = input_items[0][0][0]
        C = input_items[0][0][1]
        RSB = input_items[0][0][2]

        # if abs(RSB-LSB)>2:
        #     print("\nWarning: Right sideband exceeds left by ",(RSB-LSB)," dB\n") 
        
        SB_avg = (LSB+RSB)/2
        CSB = C-SB_avg

        output_items[0][:] = CSB
        output_items[1][:] =LSB
        output_items[2][:] = C
        output_items[3][:] = RSB

        return len(output_items[0])

