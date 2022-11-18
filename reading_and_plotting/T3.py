from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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

nc_obj = Dataset('MAWPD.nc')
Solar_Longitude = nc_obj['Solar_Longitude'][:].data
Local_Time = nc_obj['Local_Time'][:].data
Altitude = nc_obj['Altitude'][:].data
Latitude = nc_obj['Latitude'][:].data
Longitude = nc_obj['Longitude'][:].data

import h5py
f = h5py.File('height_normal_Mars.mat','r')
lon_height = np.squeeze(f['longitude'].value)#获取到特定键值的信息
lat_height = np.squeeze(f['latitude'].value)#获取到特定键值的信息
height = f['height_normal'].value#获取到特定键值的信息

#plot1
# Global distributions of climate mean temperature for different Martian months at 20 km altitude.
Temperature=nc_obj['Temperature'][:].data
Temperature=np.transpose(Temperature,(4,3,2,1,0))

fig, ax = plt.subplots(4, 3)
ax = ax.flatten()
for i in range(round(72/6)):
    Temperature_to_plot=np.squeeze(np.nanmean(Temperature[i*6:(i+1)*6,:,Altitude==20,:,:],axis=(0,1)))

    Temperature_to_plot[0,0]=156
    Temperature_to_plot[-1,-1]=188

    locals()['im'+str(i+1)] = ax[i].contourf(Longitude,Latitude,Temperature_to_plot,alpha=.9,cmap='bwr')
    ax[i].contour(lon_height, lat_height, height, colors='k', linewidths=1)
    plt.subplots_adjust(left=0.05, right=0.95, wspace=0.11, hspace=0.25, bottom=0.08, top=0.97)
    ax[i].set_yticks([-90,-60,-30,0,30,60,90])
    # 设置坐标刻度值的大小以及刻度值的字体
    # plt.title(chr(i+97),verticalalignment='top',loc='left')
    ax[i].set_title('('+chr(i + 97)+') Ls='+str(i*30)+'-'+str((i+1)*30)+' at 30 km', x=0.06+0.18,y=1,fontdict={'weight': 'heavy', 'size': 15,'family':'Times New Roman'})
    # plt.contour(Latitude,Longitude,Temperature_to_plot,colors='k',linewidth=0.01)

    ax[i].grid(linewidth=.3, linestyle='--')

ax[9].set_xlabel('Longitude (°)',fontdict={'weight': 'normal', 'size': 12,'family':'Times New Roman'})
ax[9].set_ylabel('Latitude (°)',fontdict={'weight': 'normal', 'size': 12,'family':'Times New Roman'})

# rect = [0.78, 0.25, 0.01, 0.5]
# cbar_ax = fig.add_axes(rect)
fc=fig.colorbar(im11, drawedges=True,shrink=0.4,  ax=[ax[i] for i in range(12)],pad=0.1,orientation='horizontal',spacing='proportional')
ax2=fc.ax
ax2.tick_params(which='major',direction='in')
ax2.set_title('T(K)')
ax2.tick_params(which='minor',direction='in')
ax2.yaxis.set_minor_locator(mticker.MultipleLocator(0.5))#显示x轴副刻度

plt.rcParams['font.sans-serif'] = 'Times New Roman'

plt.subplots_adjust(left=0.05, bottom=0.28, right=0.95, top=0.95, wspace=0.11, hspace=0.47)

# plt.savefig('T_3.png',dpi=600,bbox_inches = 'tight')
