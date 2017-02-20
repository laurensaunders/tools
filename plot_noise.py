import pandas as pd
import pickle
import math
import matplotlib.pyplot as plt

def plot_noise():
    for key in dan_on_noise.keys():
        f=open(dan_on_noise[key]+'data/2_BOLOS_INFO_AND_MAPPING.pkl','r')
        dan_on=pickle.load(f)
        f.close()
        g=open(dan_off_noise[key]+'data/2_BOLOS_INFO_AND_MAPPING.pkl','r')
        dan_off=pickle.load(g)
        g.close()
        al_on_spect=dan_on['0135/1/1/45']['noise']['spectrum']
        al_off_spect=dan_off['0135/1/1/45']['noise']['spectrum']
        al_spect_units=dan_on['0135/1/1/45']['noise']['spectrum_units']
        al_on_freqs=dan_on['0135/1/1/45']['noise']['freqs']
        al_off_freqs=dan_on['0135/1/1/45']['noise']['freqs']
        freqs_units=dan_on['0135/1/1/45']['noise']['freqs_units']
        nb_on_spect=dan_on['0135/2/4/45']['noise']['spectrum']
        nb_off_spect=dan_off['0135/2/4/45']['noise']['spectrum']
        nb_on_freqs=dan_on['0135/2/4/45']['noise']['freqs']
        nb_off_freqs=dan_off['0135/2/4/45']['noise']['freqs']
        plt.semilogy(al_on_freqs, al_on_spect, label='Al, DAN on')
        plt.semilogy(al_off_freqs, al_off_spect, label='Al, DAN off')
        plt.semilogy(nb_on_freqs, nb_on_spect, label='Nb, DAN on')
        plt.semilogy(nb_off_freqs, nb_off_spect, label='Nb, DAN off')
        plt.title('Noise, Amplitude = '+str(key))
        plt.ylabel('Amplitude in '+ str(al_spect_units))
        plt.xlabel('Frequency in '+ str(freqs_units))
        plt.legend()
        plt.savefig('noise_spectrum_'+str(key)+'.png')
        plt.show()
        raw_input('Hit enter when ready')

def find_channel_freqs():
    nb=pd.read_csv('stuff/LCNb.csv', sep='\t')
    al=pd.read_csv('stuff/LC433B.csv', sep='\t')
    nb_chan_freqs={}
    al_chan_freqs={}
    for ind in nb.index:
        nb_chan_freqs[nb['channel'][ind]]=float(nb['frequency'][ind])*1e-6
    for ind in al.index:
        al_chan_freqs[al['channel'][ind]]=float(al['frequency'][ind])*1e-6
    return al_chan_freqs, nb_chan_freqs

def plot_med_noise(txt_file, path_to_pkl, savepath, exp, chans=[]):
    df=pd.read_csv(txt_file, sep='\s+')
    refs={}
    for ind in df.index:
        refs[df['amp'][ind]]={'DAN_off_dump':df['DAN_off_dump'][ind].split('/')[-2], 'DAN_on_dump':df['DAN_on_dump'][ind].split('/')[-2]}
    al_on={}
    al_off={}
    nb_on={}
    nb_off={}
    num_bolos=len(chans)*2
    for key in refs:
        f=open(path_to_pkl+refs[key]['DAN_on_dump']+'/data/'+str(num_bolos)+'_BOLOS_INFO_AND_MAPPING.pkl', 'r')
        dan_on=pickle.load(f)
        f.close()
        g=open(path_to_pkl+refs[key]['DAN_off_dump']+'/data/'+str(num_bolos)+'_BOLOS_INFO_AND_MAPPING.pkl', 'r')
        dan_off=pickle.load(g)
        g.close()
        al_on[float(key)]={}
        al_off[float(key)]={}
        nb_on[float(key)]={}
        nb_off[float(key)]={}
        for chan in chans:
            al_on[float(key)][chan]={'median_noise':dan_on['0135/1/1/'+str(chan)]['noise']['median_noise'], 'rnormal':dan_on['0135/1/1/'+str(chan)]['bolo_rnormal']}
            al_off[float(key)][chan]={'median_noise':dan_off['0135/1/1/'+str(chan)]['noise']['median_noise'], 'rnormal':dan_off['0135/1/1/'+str(chan)]['bolo_rnormal']}
            nb_on[float(key)][chan]={'median_noise':dan_on['0135/2/4/'+str(chan)]['noise']['median_noise'], 'rnormal':dan_on['0135/2/4/'+str(chan)]['bolo_rnormal']}
            nb_off[float(key)][chan]={'median_noise':dan_off['0135/2/4/'+str(chan)]['noise']['median_noise'], 'rnormal':dan_off['0135/2/4/'+str(chan)]['bolo_rnormal']}

    al_chan_freqs, nb_chan_freqs = find_channel_freqs()

    fig1=plt.figure()
    fig1.set_size_inches((16,8))
    ch_cols=[]
    for aix, _amp in enumerate(al_on):
        for cix, chan in enumerate(chans):
            if aix == 0:
                channelnum=plt.scatter(_amp, float(al_on[_amp][chan]['median_noise'])/float((al_on[_amp][chan]['rnormal'])**float(exp)), marker="o", label='%.2f MHz, rnormal: %.2f'%(al_chan_freqs[chan],al_on[_amp][chan]['rnormal']))
                plt.scatter(_amp, float(al_off[_amp][chan]['median_noise'])/float((al_off[_amp][chan]['rnormal'])**float(exp)), marker="o", edgecolor=channelnum.get_edgecolor(), facecolor='none')
                ch_cols.append(channelnum.get_edgecolor())
            else:
                plt.scatter(_amp, float(al_on[_amp][chan]['median_noise'])/float((al_on[_amp][chan]['rnormal'])**float(exp)), marker="o", color=ch_cols[cix])
                plt.scatter(_amp, float(al_off[_amp][chan]['median_noise'])/float((al_off[_amp][chan]['rnormal'])**float(exp)), marker="o", edgecolor=ch_cols[cix], facecolor='none')

    plt.title('Median Noise vs. Amplitude (%s Channels), Aluminum\nFilled=DAN on, Open=DAN off'%(str(len(chans))), fontsize=24)
    plt.ylabel('Median Noise (pA/rtHz*rnormal)', fontsize=24)
    plt.xlabel('Bias Amplitude', fontsize=24)
    plt.legend()
    plt.ylim(1e0, 1e4)
    plt.xlim(5e-4, 1.1e-1)
    plt.xscale('log')
    plt.xticks(fontsize=20)
    plt.yscale('log')
    plt.yticks(fontsize=20)
    plt.savefig(savepath+'_al.png')
    plt.show()


    fig2=plt.figure()
    fig2.set_size_inches((16,8))
    ch_cols=[]
    for aix, _amp in enumerate(al_on):
        for cix, chan in enumerate(chans):
            if aix == 0:
                channelnum=plt.scatter(_amp, float(nb_on[_amp][chan]['median_noise'])/float((nb_on[_amp][chan]['rnormal'])**float(exp)), marker="o", label='%.2f MHz, rnormal: %.2f'%(nb_chan_freqs[chan],nb_on[_amp][chan]['rnormal']))
                plt.scatter(_amp, float(nb_off[_amp][chan]['median_noise'])/float((nb_off[_amp][chan]['rnormal'])**float(exp)), marker="o", edgecolor=channelnum.get_edgecolor(), facecolor='none')
                ch_cols.append(channelnum.get_edgecolor())
            else:
                plt.scatter(_amp, float(nb_on[_amp][chan]['median_noise'])/float((nb_on[_amp][chan]['rnormal'])**float(exp)), marker="o", color=ch_cols[cix])
                plt.scatter(_amp, float(nb_off[_amp][chan]['median_noise'])/float((nb_off[_amp][chan]['rnormal'])**float(exp)), marker="o", edgecolor=ch_cols[cix], facecolor='none')

    plt.title('Median Noise vs. Amplitude (%s Channels), Niobium\nFilled=DAN on, Open=DAN off'%(str(len(chans))), fontsize=24)
    plt.ylabel('Median Noise (pA/rtHz*rnormal)', fontsize=24)
    plt.xlabel('Bias Amplitude', fontsize=24)
    plt.legend()
    plt.ylim(1e0, 1e4)
    plt.xlim(5e-4, 1.1e-1)
    plt.xscale('log')
    plt.xticks(fontsize=20)
    plt.yscale('log')
    plt.yticks(fontsize=20)
    plt.savefig(savepath+'_nb.png')
    plt.show()
