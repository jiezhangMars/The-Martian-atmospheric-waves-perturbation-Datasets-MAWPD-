from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
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

nc_obj = Dataset('L:\paper/NATURE_SCIENTIFIC_DATA\dataset\step6_plot\MAWPD.nc')
Solar_Longitude = nc_obj['Solar_Longitude'][:].data
Local_Time = nc_obj['Local_Time'][:].data
Altitude = nc_obj['Altitude'][:].data
Latitude = nc_obj['Latitude'][:].data
Longitude = nc_obj['Longitude'][:].data

nc_obj = scipy.io.loadmat('E_gridding.mat')
E_gridding=nc_obj['result1']

nc_obj = scipy.io.loadmat('E_DINEOF.mat')
E_DINEOF=nc_obj['T']

nc_obj = scipy.io.loadmat('GW_perturbation_gridding.mat')
GW_perturbation_gridding=nc_obj['result1']

nc_obj = scipy.io.loadmat('GW_perturbation_DINEOF.mat')
GW_perturbation_DINEOF=nc_obj['T']

nc_obj = scipy.io.loadmat('T_gridding.mat')
T_gridding=nc_obj['result1']

nc_obj = scipy.io.loadmat('T_DINEOF.mat')
T_DINEOF=nc_obj['T']

import h5py
f = h5py.File('height_normal_Mars.mat','r')
lon_height = np.squeeze(f['longitude'].value)#获取到特定键值的信息
lat_height = np.squeeze(f['latitude'].value)#获取到特定键值的信息
height = f['height_normal'].value#获取到特定键值的信息


E_gridding[E_gridding>5000]=np.nan
E_DINEOF[E_DINEOF>5000]=np.nan

# out1=np.squeeze(E_gridding[Solar_Longitude==30,Local_Time==12,Altitude==30,:,:])
# out2=np.squeeze(E_DINEOF[Solar_Longitude==30,Local_Time==12,Altitude==30,:,:])
# out3=np.squeeze(GW_perturbation_gridding[Solar_Longitude==30,Local_Time==12,Altitude==30,:,:])
# out4=np.squeeze(GW_perturbation_DINEOF[Solar_Longitude==30,Local_Time==12,Altitude==30,:,:])
# out5=np.squeeze(T_gridding[Solar_Longitude==30,Local_Time==12,Altitude==30,:,:])
# out6=np.squeeze(T_DINEOF[Solar_Longitude==30,Local_Time==12,Altitude==30,:,:])

# out1=np.squeeze(np.nanmean(E_gridding[Solar_Longitude==30,:,Altitude==30,:,:],axis=1))
# out2=np.squeeze(np.nanmean(E_DINEOF[Solar_Longitude==30,:,Altitude==30,:,:],axis=1))
# out3=np.squeeze(np.nanmean(GW_perturbation_gridding[Solar_Longitude==30,:,Altitude==30,:,:],axis=1))
# out4=np.squeeze(np.nanmean(GW_perturbation_DINEOF[Solar_Longitude==30,:,Altitude==30,:,:],axis=1))
# out5=np.squeeze(np.nanmean(T_gridding[Solar_Longitude==30,:,Altitude==30,:,:],axis=1))
# out6=np.squeeze(np.nanmean(T_DINEOF[Solar_Longitude==30,:,Altitude==30,:,:],axis=1))

out1=np.squeeze(np.nanmean(T_gridding[Solar_Longitude==30,:6,Altitude==30,:,:],axis=1))
out2=np.squeeze(np.nanmean(T_DINEOF[Solar_Longitude==30,:6,Altitude==30,:,:],axis=1))
out3=np.squeeze(np.nanmean(T_gridding[Solar_Longitude==30,6:,Altitude==30,:,:],axis=1))
out4=np.squeeze(np.nanmean(T_DINEOF[Solar_Longitude==30,6:,Altitude==30,:,:],axis=1))

fig, ax = plt.subplots(2, 2)
ax = ax.flatten()
titlelist=['Prior to DINEOF: 0-12 h, 30 km, 30° Ls','After DINEOF: 0-12 h, 30 km, 30° Ls','Prior to DINEOF: 12-24 h, 30 km, 30° Ls','After DINEOF: 12-24 h, 30 km, 30° Ls']
for i in range(4):
    Temperature_to_plot=locals()['out'+str(i+1)]

    if i<2:
        Temperature_to_plot[Temperature_to_plot<150]=150
        Temperature_to_plot[Temperature_to_plot>172.5]=172.5
        Temperature_to_plot[0,0]=174

    else:
        Temperature_to_plot[Temperature_to_plot < 144] = 144
        Temperature_to_plot[Temperature_to_plot > 176] = 176

    locals()['im'+str(i+1)] = ax[i].contourf(Longitude,Latitude,Temperature_to_plot,alpha=.9,cmap='bwr')
    # if i%2==1:
    #     cb=plt.colorbar()
    #     cb.set_label('K',fontdict={'weight': 'heavy', 'size': 10,'family':'Times New Roman'})

    ax[i].contour(lon_height,lat_height,  height,colors='k',linewidths=1)
    plt.subplots_adjust(left=0.09,bottom=0.08, right=1,  top=0.97, wspace=0.06, hspace=0.15)
    ax[i].set_yticks(np.arange(-90,105,15))
    # 设置坐标刻度值的大小以及刻度值的字体
    # plt.title(chr(i+97),verticalalignment='top',loc='left')
    ax[i].set_title('('+chr(i + 97)+') '+titlelist[i], x=0.06+0.25,y=1,fontdict={'weight': 'heavy', 'size': 15,'family':'Times New Roman'})

    # plt.contour(Latitude,Longitude,Temperature_to_plot,colors='k',linewidth=0.01)
    ax[i].set_xticks([-180,-150,-120,-90, -60, -30, 0, 30, 60, 90,120,150,180])
    ax[i].grid(linewidth=.3,linestyle='--')

ax[2].set_xlabel('Longitude (°)',fontdict={'weight': 'normal', 'size': 12,'family':'Times New Roman'})
ax[2].set_ylabel('Latitude (°)',fontdict={'weight': 'normal', 'size': 12,'family':'Times New Roman'})

fc=fig.colorbar(im2, ax=[ax[i] for i in range(2)],pad=0.005)
ax2=fc.ax
ax2.tick_params(which='major',direction='in')
ax2.set_title('T(K)')
ax2.tick_params(which='minor',direction='in')
ax2.yaxis.set_minor_locator(mticker.MultipleLocator(0.5))#显示x轴副刻度

fc=fig.colorbar(im4, ax=[ax[i] for i in [2,3]],pad=0.005)
ax2=fc.ax
ax2.tick_params(which='major',direction='in')
ax2.set_title('T(K)')
ax2.tick_params(which='minor',direction='in')
ax2.yaxis.set_minor_locator(mticker.MultipleLocator(0.5))#显示x轴副刻度

plt.rcParams['font.sans-serif'] = 'Times New Roman'

# plt.subplots_adjust(left=0.04, bottom=0.08, right=0.85, top=0.97, wspace=0.06, hspace=0.1)

# plt.savefig('T_2_re.png',dpi=600,bbox_inches = 'tight')
#
# #plot1
# # Global distributions of climate mean temperature for different Martian months at 20 km altitude.
# Temperature=nc_obj['Temperature'][:].data
# Temperature=np.transpose(Temperature,(4,3,2,1,0))
# plt.figure(figsize=(25, 20))
# for i in range(round(72/6)):
#     Temperature_to_plot=np.squeeze(np.nanmean(Temperature[i*6:(i+1)*6,:,Altitude==20,:,:],axis=(0,1)))
#     plt.subplot(4, 3, i + 1)
#     plt.contourf(Longitude,Latitude,Temperature_to_plot,alpha=.75,cmap='nipy_spectral')
#     cb=plt.colorbar()
#     cb.set_label('K',fontdict={'weight': 'heavy', 'size': 10,'family':'Times New Roman'})
#     plt.subplots_adjust(left=0.04, right=1, wspace=0.1, hspace=0.25, bottom=0.05, top=0.97)
#     plt.yticks([-90,-60,-30,0,30,60,90])
#     # 设置坐标刻度值的大小以及刻度值的字体
#     # plt.title(chr(i+97),verticalalignment='top',loc='left')
#     plt.title('('+chr(i + 97)+')', x=-0.12,y=0.9,fontdict={'weight': 'heavy', 'size': 15,'family':'Times New Roman'})
#     # plt.contour(Latitude,Longitude,Temperature_to_plot,colors='k',linewidth=0.01)
#
# plt.savefig('T_4.2.tif',dpi=300)
#
#
