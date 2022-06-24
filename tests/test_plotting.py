from CompOSE_to_SC.conversion import conv_h5 as convert
from CompOSE_to_SC.plotting import plot_EOS
from os import system
import h5py
from matplotlib.figure import Figure

def make_blank(filename):
    """Create blank H5 file

    Make a blank file to use in tests. Make sure to remove these files afterwards.

    Args:
        filename (str): string containing path or filename of H5 file containing all zeros.
        This file will be in the StellarCollapse format
    
    Returns:
        None
    """
    infile = 'blank.h5'
    with blank as h5py.File(infile,'r'):
        convert(infile, outfile)
    # now remove blank
    system('rm %s' % infile)

def test_plotting_single_blank(show = False):
    """Test plotting from a 'blank' H5 file

    Create a blank H5 file of all zeros and plot it

    Args:
        show (bool): whether to plot the figure

    Returns:
        None
    
    """
    # create zero file
    converted_file = 'zeros.h5'
    make_blank(converted_file)
    fig = plot_EOS(converted_file)
    assert isinstance(fig,Figure)
    if show:
        fig.show()

def test_plotting_len1_list_blank(show = False):
    """Test plotting from a 'blank' H5 file

    Create a blank H5 file of all zeros and plot it as a list

    Args:
        show (bool): whether to plot the figure

    Returns:
        None
    
    """
    # create zero file
    converted_file = 'zeros.h5'
    make_blank(converted_file)
    fig = plot_EOS([converted_file])
    assert isinstance(fig,Figure)
    if show:
        fig.show()

    