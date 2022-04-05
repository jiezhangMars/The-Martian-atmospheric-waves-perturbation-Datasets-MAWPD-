import numpy as np
import tqdm

import time, os
from hanshu import closest, zeronanmean, findd, chazhi
import numpy as np
import scipy.io as scio
import h5py
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)
# time.sleep(60*60*5)
'''
check if the dineof process is ok once a ten minutes
'''
Tfile = 'T.mat'


lat = np.linspace(-87.5, 87.5, 36)  # 19
lon = np.linspace(5, 355, 36)  # 13
LSperiod = np.linspace(5, 360, 72)
localtime = np.linspace(2, 24, 12)
lev=np.linspace(1,100,100)

nlat = len(lat)
nlevs = len(lev)
Nt = len(localtime)  # Number of time steps in the 1-day window.

nsteps = 1  # number of days

dz = 360 / len(lon)  # Distance increment in degrees 360/12
dt = 24 / Nt  # time increment in Hours
Nz = len(lon)  # Number of samples available along longitude

df = 1 / (Nt * dt)  # temporal frequency
dk = 1 / (Nz * dz)  # spatial frequency

wavenumber = (np.arange(1, Nz + 1) - (Nz / 2 + 1)) * dk * 360

freq = (np.arange(1, Nt + 1) - (Nt / 2 + 1)) * df * 24  # we only use positive frequency here because of symmetry

# wavenumber = (np.arange(1, Nz + 1) - (round(Nz/ 2)  + 1)) * dk * 360
#
# freq = (np.arange(1, Nt + 1) - (round(Nt/ 2) + 1)) * df * 24  # we only use positive frequency here because of symmetry
with np.errstate(divide='ignore'):
    freq_d = 1. / freq


# print(wavenumber)


# -----------------------------------------------------------测试成功test 9 10
# T = np.load(file='E:\小程序\批量下载\data/MY_28_LS_6_T.npy')
# plt.contourf(np.mean(T,axis=(0,1)))
# amp_T_DW1,amp_T_DW2,amp_T_DW3,amp_T_DW4,amp_T_DW5,amp_T_DE1,amp_T_DE2,amp_T_DE3,amp_T_DE4,amp_T_DE5,amp_T_SPW1,amp_T_SPW2,amp_T_SPW3,amp_T_SPW4,amp_T_SPW5,amp_T_SE1,amp_T_SE2,amp_T_SE3,amp_T_SE4,amp_T_SE5,amp_T_SW1,amp_T_SW2,amp_T_SW3,amp_T_SW4,amp_T_SW5,amp_T_bg,amp_T_DS0=caltides(T)
# plt.contourf(amp_T_DW1)

# ---------------------------------------------

# MYDETAIL=np.linspace(MY[0],MY[-1],7*12+1)-(MY[1]-MY[0])/24
# MYDETAIL = np.linspace(MY[0], MY[-1], 7 * (len(LSperiod) - 1) + 1) - (MY[1] - MY[0]) / 2
MYDETAIL = LSperiod
tide_total = np.zeros([nlat, nlevs, len(MYDETAIL)])


num = np.zeros([len(MYDETAIL)])
num_t = np.zeros([nlat, nlevs, len(MYDETAIL)])
num_tide = np.zeros([nlat, nlevs, len(MYDETAIL)])

# data = h5py.File(Tfile, 'r')
# data = h5py.File('F:\dataset\step4_cal_tide\T.mat','r')
import scipy.io as scio
data=scio.loadmat(Tfile)
T=data['result1']
T[np.isnan(T)]=0
# T[0,0,0,:,:]

# IN
## localtimegap(4 6 12 16 20 24) lev lat lon
# out
# lat lev

amp_T_DW1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DW1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DW2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DW2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DW3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DW3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DW4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DW4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DW5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DW5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DS0 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DS0 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DE1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DE1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DE2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DE2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DE3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DE3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DE4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DE4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_DE5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_DE5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_bg = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_bg = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SPW1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SPW1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SPW2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SPW2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SPW3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SPW3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SPW4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SPW4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SPW5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SPW5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SW1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SW1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SW2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SW2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SW3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SW3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SW4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SW4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SW5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SW5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SE1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SE1 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SE2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SE2 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SE3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SE3 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SE4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SE4 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

amp_T_SE5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)
phs_T_SE5 = np.full([nlat, nlevs, len(MYDETAIL)], np.nan)

for i_ls in tqdm.tqdm(range(0, len(MYDETAIL))):

    # IN
    ## localtimegap(4 6 12 16 20 24) lev lat lon
    # out
    # lat lev

    accuracy = 0.8
    # ------------------------FFT
    TTT = np.copy(T[i_ls, :, :, :, :])

    # gpz_mean = np.full([105, len(files)], np.nan)



    y = np.full([Nt, nlevs, nlat, Nz], np.nan, np.complex)
    # Pyy = np.full([Nt, nlevs, nlat, Nz], np.nan)
    ampl_s = np.full([Nt, nlevs, nlat, Nz], np.nan)
    ang_s = np.full([Nt, nlevs, nlat, Nz], np.nan)
    grid_t = np.full([Nt, nlevs, nlat, Nz], np.nan)
    grr = np.full([Nt, nlevs, nlat, Nz], np.nan)


    for i in range(nlat):
        for j in range(nlevs):
            if (TTT[:, j, i, :] == False).all() or (TTT[:, j, i, :] == 0).all():
                # zz=1
                continue
            # aassa = np.copy(TTT[:, j, i, :])
            # aassa[aassa > 0] = 1
            # if not np.sum(aassa) > 72 * accuracy: continue

            # no chazhi
            grid_t = chazhi(TTT[:, j, i, :])
            grr = np.copy(grid_t)

            y[:, j, i, :] = np.fft.fftshift(np.fft.fft2(grr))  # 2D fft
            ampl_s[:, j, i, :] = np.absolute(y[:, j, i, :]) / (Nz * Nt)  # amplitude
            ang_s[:, j, i, :] = np.angle(y[:, j, i, :])  # ph1ase
            # if i_ls>2:
            #     break

            if (ampl_s[:, j, i, :] == False).all():
                continue
            # ----------------------------筛选数据

            # -------------------------------
            # the amplitude of waves are doubled due to symmetry and only positive frequencies are considered

            amp_T_DW1[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == 1]
            phs_T_DW1[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == 1]

            amp_T_DW2[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == 2]
            phs_T_DW2[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == 2]

            amp_T_DW3[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == 3]
            phs_T_DW3[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == 3]

            amp_T_DW4[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == 4]
            phs_T_DW4[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == 4]

            amp_T_DW5[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == 5]
            phs_T_DW5[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == 5]

            amp_T_DS0[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == 0]
            phs_T_DS0[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == 0]

            amp_T_DE1[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == -1]
            phs_T_DE1[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == -1]

            amp_T_DE2[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == -2]
            phs_T_DE2[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == -2]

            amp_T_DE3[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == -3]
            phs_T_DE3[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == -3]

            amp_T_DE4[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == -4]
            phs_T_DE4[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == -4]

            amp_T_DE5[i,j,i_ls] = 2 * ampl_s[freq == 1, j, i, wavenumber == -5]
            phs_T_DE5[i,j,i_ls] = -ang_s[freq == 1, j, i, wavenumber == -5]

            amp_T_bg[i,j,i_ls] = ampl_s[freq == 0, j, i, wavenumber == 0]
            phs_T_bg[i,j,i_ls] = -ang_s[freq == 0, j, i, wavenumber == 0]

            amp_T_SPW1[i,j,i_ls] = 2 * ampl_s[freq == 0, j, i, wavenumber == 1]
            phs_T_SPW1[i,j,i_ls] = -ang_s[freq == 0, j, i, wavenumber == 1]

            amp_T_SPW2[i,j,i_ls] = 2 * ampl_s[freq == 0, j, i, wavenumber == 2]
            phs_T_SPW2[i,j,i_ls] = -ang_s[freq == 0, j, i, wavenumber == 2]

            amp_T_SPW3[i,j,i_ls] = 2 * ampl_s[freq == 0, j, i, wavenumber == 3]
            phs_T_SPW3[i,j,i_ls] = -ang_s[freq == 0, j, i, wavenumber == 3]

            amp_T_SPW4[i,j,i_ls] = 2 * ampl_s[freq == 0, j, i, wavenumber == 4]
            phs_T_SPW4[i,j,i_ls] = -ang_s[freq == 0, j, i, wavenumber == 4]

            amp_T_SPW5[i,j,i_ls] = 2 * ampl_s[freq == 0, j, i, wavenumber == 5]
            phs_T_SPW5[i,j,i_ls] = -ang_s[freq == 0, j, i, wavenumber == 5]

            amp_T_SW1[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == 1]
            phs_T_SW1[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == 1]

            amp_T_SW2[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == 2]
            phs_T_SW2[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == 2]

            amp_T_SW3[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == 3]
            phs_T_SW3[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == 3]

            amp_T_SW4[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == 4]
            phs_T_SW4[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == 4]

            amp_T_SW5[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == 5]
            phs_T_SW5[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == 5]

            amp_T_SE1[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == -1]
            phs_T_SE1[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == -1]

            amp_T_SE2[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == -2]
            phs_T_SE2[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == -2]

            amp_T_SE3[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == -3]
            phs_T_SE3[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == -3]

            amp_T_SE4[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == -4]
            phs_T_SE4[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == -4]

            amp_T_SE5[i,j,i_ls] = 2 * ampl_s[freq == 2, j, i, wavenumber == -5]
            phs_T_SE5[i,j,i_ls] = -ang_s[freq == 2, j, i, wavenumber == -5]




# ------------------------test data 0
# for i in range(0,85):
#     if np.mean(amp_T_DW1[:]):
#         print(i)
# -------------------------

# amp_T_DW1_total[np.isnan(amp_T_DW1)] = 0
# amp_T_DW2_total[np.isnan(amp_T_DW2)] = 0
# amp_T_DW3_total[np.isnan(amp_T_DW3)] = 0
# amp_T_DW4_total[np.isnan(amp_T_DW4)] = 0
# amp_T_DW5_total[np.isnan(amp_T_DW5)] = 0
# amp_T_DE1_total[np.isnan(amp_T_DE1)] = 0
# amp_T_DE2_total[np.isnan(amp_T_DE2)] = 0
# amp_T_DE3_total[np.isnan(amp_T_DE3)] = 0
# amp_T_DE4_total[np.isnan(amp_T_DE4)] = 0
# amp_T_DE5_total[np.isnan(amp_T_DE5)] = 0
# amp_T_SPW1_total[np.isnan(amp_T_SPW1)] = 0
# amp_T_SPW2_total[np.isnan(amp_T_SPW2)] = 0
# amp_T_SPW3_total[np.isnan(amp_T_SPW3)] = 0
# amp_T_SPW4_total[np.isnan(amp_T_SPW4)] = 0
# amp_T_SPW5_total[np.isnan(amp_T_SPW5)] = 0
# amp_T_SE1_total[np.isnan(amp_T_SE1)] = 0
# amp_T_SE2_total[np.isnan(amp_T_SE2)] = 0
# amp_T_SE3_total[np.isnan(amp_T_SE3)] = 0
# amp_T_SE4_total[np.isnan(amp_T_SE4)] = 0
# amp_T_SE5_total[np.isnan(amp_T_SE5)] = 0
# amp_T_SW1_total[np.isnan(amp_T_SW1)] = 0
# amp_T_SW2_total[np.isnan(amp_T_SW2)] = 0
# amp_T_SW3_total[np.isnan(amp_T_SW3)] = 0
# amp_T_SW4_total[np.isnan(amp_T_SW4)] = 0
# amp_T_SW5_total[np.isnan(amp_T_SW5)] = 0
# amp_T_bg_total[np.isnan(amp_T_bg)] = 0
# amp_T_DS0_total[np.isnan(amp_T_DS0)] = 0
#
# phs_T_DW1_total[np.isnan(phs_T_DW1)] = 0
# phs_T_DW2_total[np.isnan(phs_T_DW2)] = 0
# phs_T_DW3_total[np.isnan(phs_T_DW3)] = 0
# phs_T_DW4_total[np.isnan(phs_T_DW4)] = 0
# phs_T_DW5_total[np.isnan(phs_T_DW5)] = 0
# phs_T_DE1_total[np.isnan(phs_T_DE1)] = 0
# phs_T_DE2_total[np.isnan(phs_T_DE2)] = 0
# phs_T_DE3_total[np.isnan(phs_T_DE3)] = 0
# phs_T_DE4_total[np.isnan(phs_T_DE4)] = 0
# phs_T_DE5_total[np.isnan(phs_T_DE5)] = 0
# phs_T_SPW1_total[np.isnan(phs_T_SPW1)] = 0
# phs_T_SPW2_total[np.isnan(phs_T_SPW2)] = 0
# phs_T_SPW3_total[np.isnan(phs_T_SPW3)] = 0
# phs_T_SPW4_total[np.isnan(phs_T_SPW4)] = 0
# phs_T_SPW5_total[np.isnan(phs_T_SPW5)] = 0
# phs_T_SE1_total[np.isnan(phs_T_SE1)] = 0
# phs_T_SE2_total[np.isnan(phs_T_SE2)] = 0
# phs_T_SE3_total[np.isnan(phs_T_SE3)] = 0
# phs_T_SE4_total[np.isnan(phs_T_SE4)] = 0
# phs_T_SE5_total[np.isnan(phs_T_SE5)] = 0
# phs_T_SW1_total[np.isnan(phs_T_SW1)] = 0
# phs_T_SW2_total[np.isnan(phs_T_SW2)] = 0
# phs_T_SW3_total[np.isnan(phs_T_SW3)] = 0
# phs_T_SW4_total[np.isnan(phs_T_SW4)] = 0
# phs_T_SW5_total[np.isnan(phs_T_SW5)] = 0
# phs_T_bg_total[np.isnan(phs_T_bg)] = 0
# phs_T_DS0_total[np.isnan(phs_T_DS0)] = 0
#
# num_tide[num_tide == 0] = 1
#
# amp_T_DW1_total[:] /= num_tide[:]
# amp_T_DW2_total[:] /= num_tide[:]
# amp_T_DW3_total[:] /= num_tide[:]
# amp_T_DW4_total[:] /= num_tide[:]
# amp_T_DW5_total[:] /= num_tide[:]
# amp_T_DE1_total[:] /= num_tide[:]
# amp_T_DE2_total[:] /= num_tide[:]
# amp_T_DE3_total[:] /= num_tide[:]
# amp_T_DE4_total[:] /= num_tide[:]
# amp_T_DE5_total[:] /= num_tide[:]
# amp_T_SPW1_total[:] /= num_tide[:]
# amp_T_SPW2_total[:] /= num_tide[:]
# amp_T_SPW3_total[:] /= num_tide[:]
# amp_T_SPW4_total[:] /= num_tide[:]
# amp_T_SPW5_total[:] /= num_tide[:]
# amp_T_SE1_total[:] /= num_tide[:]
# amp_T_SE2_total[:] /= num_tide[:]
# amp_T_SE3_total[:] /= num_tide[:]
# amp_T_SE4_total[:] /= num_tide[:]
# amp_T_SE5_total[:] /= num_tide[:]
# amp_T_SW1_total[:] /= num_tide[:]
# amp_T_SW2_total[:] /= num_tide[:]
# amp_T_SW3_total[:] /= num_tide[:]
# amp_T_SW4_total[:] /= num_tide[:]
# amp_T_SW5_total[:] /= num_tide[:]
# amp_T_bg_total[:] /= num_tide[:]
# amp_T_DS0_total[:] /= num_tide[:]
#
# phs_T_DW1_total[:] /= num_tide[:]
# phs_T_DW2_total[:] /= num_tide[:]
# phs_T_DW3_total[:] /= num_tide[:]
# phs_T_DW4_total[:] /= num_tide[:]
# phs_T_DW5_total[:] /= num_tide[:]
# phs_T_DE1_total[:] /= num_tide[:]
# phs_T_DE2_total[:] /= num_tide[:]
# phs_T_DE3_total[:] /= num_tide[:]
# phs_T_DE4_total[:] /= num_tide[:]
# phs_T_DE5_total[:] /= num_tide[:]
# phs_T_SPW1_total[:] /= num_tide[:]
# phs_T_SPW2_total[:] /= num_tide[:]
# phs_T_SPW3_total[:] /= num_tide[:]
# phs_T_SPW4_total[:] /= num_tide[:]
# phs_T_SPW5_total[:] /= num_tide[:]
# phs_T_SE1_total[:] /= num_tide[:]
# phs_T_SE2_total[:] /= num_tide[:]
# phs_T_SE3_total[:] /= num_tide[:]
# phs_T_SE4_total[:] /= num_tide[:]
# phs_T_SE5_total[:] /= num_tide[:]
# phs_T_SW1_total[:] /= num_tide[:]
# phs_T_SW2_total[:] /= num_tide[:]
# phs_T_SW3_total[:] /= num_tide[:]
# phs_T_SW4_total[:] /= num_tide[:]
# phs_T_SW5_total[:] /= num_tide[:]
# phs_T_bg_total[:] /= num_tide[:]
# phs_T_DS0_total[:] /= num_tide[:]
savepath='./tide_result_72_12_100_37_37_right_quality_control_nochazhi/'
if not os.path.exists(savepath):
    os.mkdir(savepath)
np.save(file=savepath+'amp_T_DW1.npy', arr=amp_T_DW1)  # lat lev LS
np.save(file=savepath+'amp_T_DW2.npy', arr=amp_T_DW2)
np.save(file=savepath+'amp_T_DW3.npy', arr=amp_T_DW3)
np.save(file=savepath+'amp_T_DW4.npy', arr=amp_T_DW4)
np.save(file=savepath+'amp_T_DW5.npy', arr=amp_T_DW5)

np.save(file=savepath+'amp_T_DE1.npy', arr=amp_T_DE1)
np.save(file=savepath+'amp_T_DE2.npy', arr=amp_T_DE2)
np.save(file=savepath+'amp_T_DE3.npy', arr=amp_T_DE3)
np.save(file=savepath+'amp_T_DE4.npy', arr=amp_T_DE4)
np.save(file=savepath+'amp_T_DE5.npy', arr=amp_T_DE5)

np.save(file=savepath+'amp_T_SPW1.npy', arr=amp_T_SPW1)
np.save(file=savepath+'amp_T_SPW2.npy', arr=amp_T_SPW2)
np.save(file=savepath+'amp_T_SPW3.npy', arr=amp_T_SPW3)
np.save(file=savepath+'amp_T_SPW4.npy', arr=amp_T_SPW4)
np.save(file=savepath+'amp_T_SPW5.npy', arr=amp_T_SPW5)

np.save(file=savepath+'amp_T_SE1.npy', arr=amp_T_SE1)
np.save(file=savepath+'amp_T_SE2.npy', arr=amp_T_SE2)
np.save(file=savepath+'amp_T_SE3.npy', arr=amp_T_SE3)
np.save(file=savepath+'amp_T_SE4.npy', arr=amp_T_SE4)
np.save(file=savepath+'amp_T_SE5.npy', arr=amp_T_SE5)

np.save(file=savepath+'amp_T_SW1.npy', arr=amp_T_SW1)
np.save(file=savepath+'amp_T_SW2.npy', arr=amp_T_SW2)
np.save(file=savepath+'amp_T_SW3.npy', arr=amp_T_SW3)
np.save(file=savepath+'amp_T_SW4.npy', arr=amp_T_SW4)
np.save(file=savepath+'amp_T_SW5.npy', arr=amp_T_SW5)

np.save(file=savepath+'amp_T_bg.npy', arr=amp_T_bg)
np.save(file=savepath+'amp_T_DS0.npy', arr=amp_T_DS0)

np.save(file=savepath+'phs_T_DW1.npy', arr=phs_T_DW1)
np.save(file=savepath+'phs_T_DW2.npy', arr=phs_T_DW2)
np.save(file=savepath+'phs_T_DW3.npy', arr=phs_T_DW3)
np.save(file=savepath+'phs_T_DW4.npy', arr=phs_T_DW4)
np.save(file=savepath+'phs_T_DW5.npy', arr=phs_T_DW5)

np.save(file=savepath+'phs_T_DE1.npy', arr=phs_T_DE1)
np.save(file=savepath+'phs_T_DE2.npy', arr=phs_T_DE2)
np.save(file=savepath+'phs_T_DE3.npy', arr=phs_T_DE3)
np.save(file=savepath+'phs_T_DE4.npy', arr=phs_T_DE4)
np.save(file=savepath+'phs_T_DE5.npy', arr=phs_T_DE5)

np.save(file=savepath+'phs_T_SPW1.npy', arr=phs_T_SPW1)
np.save(file=savepath+'phs_T_SPW2.npy', arr=phs_T_SPW2)
np.save(file=savepath+'phs_T_SPW3.npy', arr=phs_T_SPW3)
np.save(file=savepath+'phs_T_SPW4.npy', arr=phs_T_SPW4)
np.save(file=savepath+'phs_T_SPW5.npy', arr=phs_T_SPW5)

np.save(file=savepath+'phs_T_SE1.npy', arr=phs_T_SE1)
np.save(file=savepath+'phs_T_SE2.npy', arr=phs_T_SE2)
np.save(file=savepath+'phs_T_SE3.npy', arr=phs_T_SE3)
np.save(file=savepath+'phs_T_SE4.npy', arr=phs_T_SE4)
np.save(file=savepath+'phs_T_SE5.npy', arr=phs_T_SE5)

np.save(file=savepath+'phs_T_SW1.npy', arr=phs_T_SW1)
np.save(file=savepath+'phs_T_SW2.npy', arr=phs_T_SW2)
np.save(file=savepath+'phs_T_SW3.npy', arr=phs_T_SW3)
np.save(file=savepath+'phs_T_SW4.npy', arr=phs_T_SW4)
np.save(file=savepath+'phs_T_SW5.npy', arr=phs_T_SW5)

np.save(file=savepath+'phs_T_bg.npy', arr=phs_T_bg)
np.save(file=savepath+'phs_T_DS0.npy', arr=phs_T_DS0)
