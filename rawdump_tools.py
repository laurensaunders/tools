# plot rawdumps

import pickle
import matplotlib.pyplot as plt

def rawdump_data(rawdump_pkls={}):
    '''
    Quick function to help separate and label data for plotting.

    Parameters
    ----------
    rawdump_pkls: dict('label':'pkl_file')

    Returns
    -------
    data_helper: dict(spectrum, freqs, label)
    '''
    data_helper={}
    for label in rawdump_pkls:
        f=open(rawdump_pkls[item])
        item=pickle.load(f)
        f.close()

        freqs=item['full_data']['spectrum_freqs']*1e-6
        spectrum=item['full_data']['spectrum_real']

        data_helper[item]={'spectrum':spectrum, 'freqs':freqs, 'label':label}

    return data_helper

def plot_tool(data_helper, savetofile):
    '''
    Plotting tool for rawdumps.

    Parameters
    ----------
    data_helper: dict(spectrum, freqs, label)
    savetofile: str() of (full path to) filename to save the plot to

    Returns
    -------
    None
    '''
    plt.figure()
    plt.title('Rawdump Overplot')
    plt.xlabel('Frequency (MHz)')
    ax1=plt.subplot(211)
    plt.ylabel('Output ($\mu$V/rtHz)')
    ax2=plt.subplot(212)
    plt.ylabel('Output ($\mu$V/rtHz)')

    for data in data_helper:
        ax1.plot(data['freqs'], data['spectrum'], label=data['label'])
        ax2.semilogy(data['freqs'], data['spectrum'], label=data['label'])

    plt.legend()
    plt.savefig(savetofile)
    plt.show()

def plot_rawdump(rawdump_pkls={}, savetofile):
    '''
    Tool to pull data from rawdump pkl files and plot the spectra, in lin-lin
    plots as well as semilog y

    Parameters
    ----------
    rawdump_pkls: dict('label':'pkl_file')
    savetofile: str() of (full path to) filename to save the plot to

    Returns
    -------
    None
    '''
    data_helper=rawdump_data(rawdump_pkls=rawdump_pkls)
    plot_tool(data_helper=data_helper, savetofile=savetofile)
