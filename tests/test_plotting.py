from CompOSE_to_SC.conversion import conv_h5 as convert
from CompOSE_to_SC.plotting import plot_EOS
from os import system
import h5py
from matplotlib.figure import Figure
import tarfile

dir_path = '../PracticeFiles/'
f1tar = 'eoscomposeBHBDD2L.tar.gz'
f1h5 = f1tar.split('.')[0] + '.h5'
f2tar = 'eoscomposeLS220.tar.gz'
f2h5 = f2tar.split('.')[0] + '.h5'
def untar():
    """Untar practice files
    
    Decompress practice files for use in tests.
    Please remove these files after they are created with
    system('rm %s %s' % (dir_path+f1h5,dir_path+f2h5))

    Args:
        None
    Returns:
        None
    """
    with tarfile.open(dir_path+f1tar) as file:
        file.extractall(dir_path+f1h5)
    with tarfile.open(dir_path+f2tar) as file:
        file.extractall(dir_path+f2h5)



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

def test_plotting_single(filename = dir_path+f1h5,show = False):
    """Test plotting from a 'blank' H5 file

    Create a blank H5 file of all zeros and plot it

    Args:
        show (bool): whether to plot the figure

    Returns:
        None
    
    """
    # untar files
    untar()
    fig = plot_EOS(filename)
    system('rm %s %s' % (dir_path+f1h5,dir_path+f2h5))
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