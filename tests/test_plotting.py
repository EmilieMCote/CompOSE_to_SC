from CompOSE_to_SC.conversion import conv_h5 as convert
from CompOSE_to_SC.plotting import plot_EOS
from os import system
import h5py
from matplotlib.figure import Figure
import tarfile
from os.path import split

dir_path = '../PracticeFiles/'
f1tar = 'eoscomposeBHBDD2L.tar.gz'
f2tar = 'eoscomposeLS220.tar.gz'
def untar(path):
    """Untar practice files
    
    Decompress practice files for use in tests.
    Please remove these files after they are created with
    system('rm %s' % path)

    Args:
        None
    Returns:
        None
    """
    file =  tarfile.open(path)
    head,tail = split(path)
    file.extractall(head)
    file.close
    return head+tail.split('.')[0] + '.h5'


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
    with h5py.File(infile,'w') as blank:
        convert(infile, filename)
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

def test_plotting_single(filename = dir_path+f1tar,show = False):
    """Test plotting from a 'blank' H5 file

    Create a blank H5 file of all zeros and plot it

    Args:
        show (bool): whether to plot the figure

    Returns:
        None
    
    """
    # untar files
    outfile = untar(filename)
    fig = plot_EOS(outfile)
    system('rm %s' % outfile)
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