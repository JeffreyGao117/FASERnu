import uproot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from scipy import stats

plt.close('all')
fig, axs = plt.subplots(2, 2, figsize=(12.5,10))
axs[0, 1].set_title('sqrt(x*x+y*y)<100&&CC==1&&ntracks<50')
axs[0, 1].set(xlabel='Z', ylabel='ntracks')
axs[0, 0].set(xlabel='v interaction Z (mm)')
axs[1, 0].set(xlabel='v interaction Z (mm)', ylabel='Efficiency')

offsetZ = 603.3

events = uproot.open('ntracks.root')
# events['nt'].show()  # for sanity
# events['ntReso'].show()  # for sanity
nt = events.get('nt')
ntReso = events.get('ntReso')
z = nt.array('z')
x = nt.array('x')
y = nt.array('y')
cc_nt = nt.array('CC')
cc_ntReso = ntReso.array('CC')
ntracks = nt.array('ntracks')
iev_reso = ntReso.array('iev')

# Graph 1 trackers
z_parse = []
ntracks_parse = []
# Graph 2 trackers
cc = []
cc1 = []
cc2 = []
cc3 = []

for iev in nt.array('iev'):
    if np.sqrt(x[int(iev)]**2+y[int(iev)]**2) < 100 and cc_nt[int(iev)] == 1 and ntracks[int(iev)] < 50:
        z_parse.append(z[int(iev)])
        ntracks_parse.append(ntracks[int(iev)])
    if cc_nt[int(iev)] == 1:
        cc.append(z[int(iev)])
        if ntracks[int(iev)] >= 1:
            cc1.append(z[int(iev)])
            if ntracks[int(iev)] >= 2:
                cc2.append(z[int(iev)])
                if ntracks[int(iev)] >= 3:
                    cc3.append(z[int(iev)])

cc2_max = max(cc2)
cc3_max = max(cc3)

axs[0, 1].hist2d(z_parse, ntracks_parse, bins=[75, 41], range=([offsetZ-1400, offsetZ+100], [1, 42]), cmin=1)
axs[0, 0].hist(cc, bins=15, range=(offsetZ-1400, offsetZ+100), color='#cccccc', edgecolor='black', linewidth=0.1)
axs[0, 0].hist(cc1, bins=15, range=(offsetZ-1400, offsetZ+100), color='#99ccff', edgecolor='black', linewidth=0.1)
axs[0, 0].hist(cc2, bins=15, range=(offsetZ-1400, offsetZ+100), color='#99cc00', edgecolor='black', linewidth=0.1)
axs[0, 0].hist(cc3, bins=15, range=(offsetZ-1400, offsetZ+100), color='#66ffff', edgecolor='black', linewidth=0.1)
axs[1, 0].hist(cc2, weights=[abs(n)/(len(cc2)*100) for n in cc2], bins=15, range=(offsetZ-1400, offsetZ+100),
               color='#99cc00', edgecolor='black', linewidth=0.1)
axs[1, 0].hist(cc3, weights=[abs(n)/(len(cc2)*100) for n in cc3], bins=15, range=(offsetZ-1400, offsetZ+100),
               color='#66ffff', edgecolor='black', linewidth=0.1)

axs[0, 1].yaxis.set_minor_locator(tck.AutoMinorLocator())
axs[0, 0].legend(['All', 'CC', 'CC connected with ≥ 2 trks', 'CC connected with ≥ 3 trks'], loc=[0.05,0.2])
axs[0, 0].annotate('     Hz  \n Entries: 505 \n Mean -40.83 \n RMS 386.3', xy=(450, 60))
axs[0, 0].yaxis.set_minor_locator(tck.AutoMinorLocator())
axs[1, 0].legend(['CC connected with ≥ 2 trks', 'CC connected with ≥ 3 trks'])
axs[1, 0].yaxis.set_minor_locator(tck.AutoMinorLocator())

plt.show()
fig.savefig('uproot_hists.png')