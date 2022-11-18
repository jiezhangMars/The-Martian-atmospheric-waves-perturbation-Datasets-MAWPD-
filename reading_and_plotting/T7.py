from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib as mpl
from matplotlib.colors import LogNorm

# dimensions(sizes): Solar_Longitude(72), Local_Time(12), Altitude(100), Latitude(36), Longitude(36)
# variables(dimensions): float64 Solar_Longitude(Solar_Longitude), float64 Local_Time(Local_Time),
# float64 Altitude(Altitude), float64 Latitude(Latitude), float64 Longitude(Longitude),
# float64 Temperature(Longitude, Latitude, Altitude, Local_Time, Solar_Longitude),
# float64 GW(Longitude, Latitude, Altitude, Local_Time, Solar_Longitude),
# float64 E(Longitude, Latitude, Altitude, Local_Time, Solar_Longitude),
# float64 amp_T_DE1(Latitude, Altitude, Solar_Longitude), float64 amp_T_DE2(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_DE3(Latitude, Altitude, Solar_Longitude), float64 amp_T_DE4(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_DE5(Latitude, Altitude, Solar_Longitude), float64 amp_T_DS0(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_DW1(Latitude, Altitude, Solar_Longitude), float64 amp_T_DW2(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_DW3(Latitude, Altitude, Solar_Longitude), float64 amp_T_DW4(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_DW5(Latitude, Altitude, Solar_Longitude), float64 amp_T_SE1(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_SE2(Latitude, Altitude, Solar_Longitude), float64 amp_T_SE3(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_SE4(Latitude, Altitude, Solar_Longitude), float64 amp_T_SE5(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_SPW1(Latitude, Altitude, Solar_Longitude), float64 amp_T_SPW2(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_SPW3(Latitude, Altitude, Solar_Longitude), float64 amp_T_SPW4(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_SPW5(Latitude, Altitude, Solar_Longitude), float64 amp_T_SW1(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_SW2(Latitude, Altitude, Solar_Longitude), float64 amp_T_SW3(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_SW4(Latitude, Altitude, Solar_Longitude), float64 amp_T_SW5(Latitude, Altitude, Solar_Longitude),
# float64 amp_T_bg(Latitude, Altitude, Solar_Longitude), float64 phs_T_DE1(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_DE2(Latitude, Altitude, Solar_Longitude), float64 phs_T_DE3(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_DE4(Latitude, Altitude, Solar_Longitude), float64 phs_T_DE5(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_DS0(Latitude, Altitude, Solar_Longitude), float64 phs_T_DW1(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_DW2(Latitude, Altitude, Solar_Longitude), float64 phs_T_DW3(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_DW4(Latitude, Altitude, Solar_Longitude), float64 phs_T_DW5(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SE1(Latitude, Altitude, Solar_Longitude), float64 phs_T_SE2(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SE3(Latitude, Altitude, Solar_Longitude), float64 phs_T_SE4(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SE5(Latitude, Altitude, Solar_Longitude), float64 phs_T_SPW1(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SPW2(Latitude, Altitude, Solar_Longitude), float64 phs_T_SPW3(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SPW4(Latitude, Altitude, Solar_Longitude), float64 phs_T_SPW5(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SW1(Latitude, Altitude, Solar_Longitude), float64 phs_T_SW2(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SW3(Latitude, Altitude, Solar_Longitude), float64 phs_T_SW4(Latitude, Altitude, Solar_Longitude),
# float64 phs_T_SW5(Latitude, Altitude, Solar_Longitude), float64 phs_T_bg(Latitude, Altitude, Solar_Longitude)

nc_obj = Dataset('L:\paper/NATURE_SCIENTIFIC_DATA\dataset\step6_plot\MAWPD.nc')
Solar_Longitude = nc_obj['Solar_Longitude'][:].data
Local_Time = nc_obj['Local_Time'][:].data
Altitude = nc_obj['Altitude'][:].data
Latitude = nc_obj['Latitude'][:].data
Longitude = nc_obj['Longitude'][:].data

#plot1
# Global distributions of climate mean temperature for different Martian months at 20 km altitude.
amp_T_DW1=nc_obj['amp_T_DW1'][:].data
phs_T_DW1=nc_obj['phs_T_DW1'][:].data

amp_T_DW1=np.transpose(amp_T_DW1,(2,1,0))
phs_T_DW1=np.transpose(phs_T_DW1,(2,1,0))
phs_T_DW1=phs_T_DW1/np.pi*12
np.nanmax(phs_T_DW1)
height=np.array([5,10,30,50,70])
# plt.figure(figsize=(25, 20))


fig, ax = plt.subplots(5, 2)
ax = ax.flatten()
titlelist = ['5', '10', '30', '50', '70']
level=np.arange(0,15,1)
for i in range(5):
    print(i)

    Temperature_to_plot = np.squeeze(amp_T_DW1[:, Altitude == height[i], :])

    Temperature_to_plot[0, 0] = 14

    locals()['im' + str(i + 1)] = ax[i * 2].contourf(Solar_Longitude, Latitude, Temperature_to_plot.transpose(),levels=level,
                                                      alpha=.75, cmap='bwr')

    plt.subplots_adjust(left=0.05, right=1, wspace=0.03, hspace=0.31, bottom=0.07, top=0.97)
    ax[i * 2].set_xticks(np.arange(0, 360, 30))
    ax[i * 2].set_yticks([-90, -60, -30, 0, 30, 60, 90])
    # 设置坐标刻度值的大小以及刻度值的字体
    # plt.title(chr(i+97),verticalalignment='top',loc='left')
    ax[i * 2].set_title('(' + chr(i + 97) + ') DW1 amplitude at ' + titlelist[i] + 'km', x=-0.078+0.2, y=0.92,
                        fontdict={'weight': 'heavy', 'size': 10, 'family': 'Times New Roman'})

ax[8].set_xlabel('Ls (°)', fontdict={'weight': 'normal', 'size': 12, 'family': 'Times New Roman'})
ax[8].set_ylabel('Latitude (°)', fontdict={'weight': 'normal', 'size': 12, 'family': 'Times New Roman'})

fc = fig.colorbar(im1, drawedges=True, ax=[ax[i] for i in [0, 2, 4, 6, 8]], pad=0.1, orientation='horizontal')
ax2 = fc.ax
ax2.tick_params(which='major', direction='in')
ax2.set_title('T(K)')
ax2.tick_params(which='minor', direction='in')
ax2.yaxis.set_minor_locator(mticker.MultipleLocator(0.1))  # 显示x轴副刻度

plt.rcParams['font.sans-serif'] = 'Times New Roman'

# norm = mpl.colors.BoundaryNorm([0,10,20,30,40,50,60,70,80,90,100,200,300,500,700], ncolors=15)

level=np.arange(-12,13)
for i in range(5):
    Temperature_to_plot = np.squeeze(phs_T_DW1[:, Altitude == height[i], :])



    locals()['im' + str(i + 1)] = ax[i * 2 + 1].contourf(Solar_Longitude, Latitude, Temperature_to_plot.transpose(),levels=level,
                                                          alpha=.75, cmap='bwr')

    plt.subplots_adjust(left=0.05, right=1, wspace=0.03, hspace=0.31, bottom=0.07, top=0.97)
    ax[i * 2 + 1].set_xticks(np.arange(0, 360, 30))
    ax[i * 2 + 1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
    # 设置坐标刻度值的大小以及刻度值的字体
    # plt.title(chr(i+97),verticalalignment='top',loc='left')
    ax[i * 2 + 1].set_title('(' + chr(i + 97+1) + ') DW1 phase at ' + titlelist[i] + 'km', x=-0.078+0.2, y=0.92,
                            fontdict={'weight': 'heavy', 'size': 10, 'family': 'Times New Roman'})

fc = fig.colorbar(im3, drawedges=True, shrink=0.9, ax=[ax[i] for i in [1, 3, 5, 7, 9]], pad=0.1,
                  orientation='horizontal')
ax2 = fc.ax
ax2.tick_params(which='major', direction='in',tick1On=True,tick2On=True)
ax2.set_title('Time(hour)')
ax2.tick_params(which='minor',direction='in')
from matplotlib.ticker import FormatStrFormatter
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# ax2.yaxis.set_minor_locator(mticker.MultipleLocator(25))#显示x轴副刻度

plt.rcParams['font.sans-serif'] = 'Times New Roman'

plt.subplots_adjust(left=0.07, bottom=0.3, right=0.98, top=0.97, wspace=0.16, hspace=0.49)

# plt.savefig('T_7.png',dpi=600,bbox_inches = 'tight')
