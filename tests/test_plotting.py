from CompOSE_to_SC.conversion import conv_h5 as convert
from CompOSE_to_SC.plotting import plot_EOS
from os import system
import h5py
from matplotlib.figure import Figure

def test_plotting_blank():
    """Test plotting a 'blank' H5 file

    Create a blank H5 file of all zeros and plot it

    Args:
        None

    Returns:
        None
    
    """
    # create blank file
    infile = 'blank.h5'
    outfile = 'zeros.h5'
    with blank as h5py.File(infile,'r'):
        convert(infile, outfile)
        fig = plot_EOS(infile)
        assert isinstance(fig,Figure)
    # now remove blank and zeros
    system('rm %s %s' % (infile,outfile))