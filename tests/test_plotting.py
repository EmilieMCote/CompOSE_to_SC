from CompOSE_to_SC.conversion import conv_h5 as convert
from CompOSE_to_SC.plotting import plot_EOS
from os import system
import h5py
from matplotlib.figure import Figure
import tarfile
from os.path import split

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
    return head+ '/' +tail.split('.')[0] + '.h5'


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
