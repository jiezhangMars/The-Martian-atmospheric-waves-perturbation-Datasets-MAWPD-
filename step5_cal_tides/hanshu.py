import numpy as np
import tqdm
# import matplotlib.pyplot as plt
import time,os
# np.set_printoptions(threshold=np.inf)
# time.sleep(60*60*5)
from scipy.signal import savgol_filter
from scipy.interpolate import griddata#引入scipy中的二维插值库


def zeronanmean(list,number):
    list[list==0]=np.nan
    list=np.nanmean(list,number)
    list[np.isnan(list)]=0
    return list
def findd(a):
    b=[]
    c=[]
    value=[]
    for i in range(0,a.shape[0]):
        for j in range(0,a.shape[1]):
            if a[i,j]!=0:
                b.append(i)
                c.append(j)
                value.append(a[i,j])
    b=np.array(b)
    c=np.array(c)
    points=np.vstack((b,c))
    return points,value
def tiqu(watericeprofile,MYDETAIL,lev,bili):

    tiqux_a_watericeprofile = []
    tiquy_a_watericeprofile = []
    tiquz_a_watericeprofile = []
    tiquyanse_a_watericeprofile = []

    for k in range(0, 18):

        a_watericeprofile = np.copy(watericeprofile[k, :, :])
        a_watericeprofile[np.isnan(a_watericeprofile)] = 0
        for i in range(0, a_watericeprofile.shape[0]):
            for j in range(0, a_watericeprofile.shape[1]):
                # if a[i,j]==np.max(a[:,j]) and np.max(a[:,j])!=0:
                if a_watericeprofile[i, j] > bili * np.max(a_watericeprofile[i, :]):
                    tiquz_a_watericeprofile.append(lev[i])
                    tiqux_a_watericeprofile.append(MYDETAIL[j])
                    tiquy_a_watericeprofile.append(k)
                    tiquyanse_a_watericeprofile.append(a_watericeprofile[i, j])
    tiqux_a_watericeprofile = np.array(tiqux_a_watericeprofile)
    tiquz_a_watericeprofile = np.array(tiquz_a_watericeprofile)
    tiquy_a_watericeprofile = np.array(tiquy_a_watericeprofile)
    tiquyanse_a_watericeprofile = np.array(tiquyanse_a_watericeprofile)
    return tiqux_a_watericeprofile,tiquy_a_watericeprofile,tiquz_a_watericeprofile,tiquyanse_a_watericeprofile

def findgap(array):
    j=0
    for i in range(0,len(array)):
        if i==0:

            a=np.array([])
            b=np.array([])
            continue


        if i == len(array) - 1:
            a=a.astype('int64')
            b=b.astype('int64')
            if np.isnan(array[-1]):
                a=a[:-1]
            continue
        else:

            if not np.isnan(array[i-1]) and  np.isnan(array[i]):
                a=np.concatenate((a,np.array([i-1])))
                # print(np.array([i]))
                # print(a)

            if not np.isnan(array[i+1]) and np.isnan(array[i]):
                if np.isnan(array[0]) and j==0:
                    j+=1
                    continue
                b=np.concatenate((b,np.array([i+1])))

    return a,b

class setfig():
    '''
       在绘图前对字体类型、字体大小、分辨率、线宽、输出格式进行设置.
       para colume = 1.半栏图片 7*6cm
                     2.双栏长图 14*6cm
       x轴刻度默认为整数
       手动保存时，默认输出格式为 pdf
       案例 Sample.1:
            fig=setfig(column=2)
            plt.semilogy(x, color='blue', linestyle='solid', label='信号1')
            plt.legend(loc='upper left')
            plt.xlabel('时间/t')
            plt.ylabel('幅度')
            plt.title('冲击声信号')
            fig.show()
    '''

    def __init__(self, column):

        self.column = column  # 设置栏数
        # 对尺寸和 dpi参数进行调整
        plt.rcParams['figure.dpi'] = 300

        # 字体调整
        plt.rcParams['font.sans-serif'] = ['simhei']  # 如果要显示中文字体,则在此处设为：simhei,Arial Unicode MS
        plt.rcParams['font.weight'] = 'light'
        plt.rcParams['axes.unicode_minus'] = False  # 坐标轴负号显示
        plt.rcParams['axes.titlesize'] = 8  # 标题字体大小
        plt.rcParams['axes.labelsize'] = 7  # 坐标轴标签字体大小
        plt.rcParams['xtick.labelsize'] = 7  # x轴刻度字体大小
        plt.rcParams['ytick.labelsize'] = 7  # y轴刻度字体大小
        plt.rcParams['legend.fontsize'] = 6

        # 线条调整
        plt.rcParams['axes.linewidth'] = 1

        # 刻度在内，设置刻度字体大小
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'

        # 设置输出格式为PDF
        plt.rcParams['savefig.format'] = 'pdf'
        plt.rcParams['figure.autolayout'] = True

    @property
    def tickfont(self):
        plt.tight_layout()
        ax1 = plt.gca()  # 获取当前图像的坐标轴
        # 更改坐标轴字体，避免出现指数为负的情况
        tick_font = font_manager.FontProperties(family='it', size=7.0)
        ax1.xaxis.set_major_locator
        for labelx in ax1.get_xticklabels():
            labelx.set_fontproperties(tick_font)
        for labely in ax1.get_yticklabels():
            labely.set_fontproperties(tick_font)
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # x轴刻度设置为整数

    @property
    def Global_font(self):
        # 设置基本字体
        plt.rcParams['font.sans-serif'] = ['simhei']  # 如果要显示中文字体,则在此处设为：simhei,Arial Unicode MS
        plt.rcParams['font.weight'] = 'light'

    def show(self):
        # 改变字体
        self.Global_font
        self.tickfont
        # 改变图像大小
        cm_to_inc = 1 / 2.54  # 厘米和英寸的转换 1inc = 2.54cm
        gcf = plt.gcf()  # 获取当前图像
        if self.column == 1:
            gcf.set_size_inches(7 * cm_to_inc, 6 * cm_to_inc)
        else:
            gcf.set_size_inches(14 * cm_to_inc, 6 * cm_to_inc)

        plt.show()

















def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)
def quweiduave(a,b,c):
    if b==c:
        a=a[c,:,:]
    else:
        a[a==0]=np.nan
        a=np.nanmean(a[b:c,:,:],0)
        a[np.isnan(a)]=0
    return a
def quweiduave_wind(a,b,c):
    if b==c:
        a=a[:,:,c]
    else:
        a[a==0]=np.nan
        a=np.nanmean(a[:,:,b:c],2)
        a[np.isnan(a)]=0
    return a
def pinghua(a,b,window,jieshu):


    a2=a[a.argsort()]
    b=b[a.argsort()]
    b2=savgol_filter(b, window,jieshu) # window size 51, polynomial order 3
    return a2,b2

def zhaozuidazhi(wi):
    k=np.zeros(wi.shape[0])
    p = np.zeros(wi.shape[0])
    ma=np.zeros(wi.shape[0])
    for i in range(0,wi.shape[0]):
        for  j in range(0,wi.shape[1]):
            if wi[i,j]>ma[i]:
                ma[i]=wi[i,j]
                k[i]=i
                p[i]=j
    return k,p


def chazhi(aa):
    aa[np.isnan(aa)]=0

    points,value=findd(aa)
    points=points.transpose()
    grid_x, grid_y = np.mgrid[1:12:12j, 1:36:36j]
    grid_z0 = griddata(points, value, (grid_x, grid_y), method='nearest')
    return grid_z0
def closest(mylist, Number):
    answer = []
    for i in mylist:
        answer.append(abs(Number - i))
    return answer.index(min(answer))

def caltidesDW1(T1):
    # ------------------------FFT
    T = T1

    # gpz_mean = np.full([105, len(files)], np.nan)

    amp_T_DW1 = np.full([nlat, nlevs], np.nan)
    phs_T_DW1 = np.full([nlat, nlevs], np.nan)

    amp_T_DW2 = np.full([nlat, nlevs], np.nan)
    phs_T_DW2 = np.full([nlat, nlevs], np.nan)

    amp_T_DW3 = np.full([nlat, nlevs], np.nan)
    phs_T_DW3 = np.full([nlat, nlevs], np.nan)

    amp_T_DW4 = np.full([nlat, nlevs], np.nan)
    phs_T_DW4 = np.full([nlat, nlevs], np.nan)

    amp_T_DW5 = np.full([nlat, nlevs], np.nan)
    phs_T_DW5 = np.full([nlat, nlevs], np.nan)

    amp_T_DS0 = np.full([nlat, nlevs], np.nan)
    phs_T_DS0 = np.full([nlat, nlevs], np.nan)

    amp_T_DE1 = np.full([nlat, nlevs], np.nan)
    phs_T_DE1 = np.full([nlat, nlevs], np.nan)

    amp_T_DE2 = np.full([nlat, nlevs], np.nan)
    phs_T_DE2 = np.full([nlat, nlevs], np.nan)

    amp_T_DE3 = np.full([nlat, nlevs], np.nan)
    phs_T_DE3 = np.full([nlat, nlevs], np.nan)

    amp_T_DE4 = np.full([nlat, nlevs], np.nan)
    phs_T_DE4 = np.full([nlat, nlevs], np.nan)

    amp_T_DE5 = np.full([nlat, nlevs], np.nan)
    phs_T_DE5 = np.full([nlat, nlevs], np.nan)

    amp_T_bg = np.full([nlat, nlevs], np.nan)
    phs_T_bg = np.full([nlat, nlevs], np.nan)

    amp_T_SPW1 = np.full([nlat, nlevs], np.nan)
    phs_T_SPW1 = np.full([nlat, nlevs], np.nan)

    amp_T_SPW2 = np.full([nlat, nlevs], np.nan)
    phs_T_SPW2 = np.full([nlat, nlevs], np.nan)

    amp_T_SPW3 = np.full([nlat, nlevs], np.nan)
    phs_T_SPW3 = np.full([nlat, nlevs], np.nan)

    amp_T_SPW4 = np.full([nlat, nlevs], np.nan)
    phs_T_SPW4 = np.full([nlat, nlevs], np.nan)

    amp_T_SPW5 = np.full([nlat, nlevs], np.nan)
    phs_T_SPW5 = np.full([nlat, nlevs], np.nan)

    amp_T_SW1 = np.full([nlat, nlevs], np.nan)
    phs_T_SW1 = np.full([nlat, nlevs], np.nan)

    amp_T_SW2 = np.full([nlat, nlevs], np.nan)
    phs_T_SW2 = np.full([nlat, nlevs], np.nan)

    amp_T_SW3 = np.full([nlat, nlevs], np.nan)
    phs_T_SW3 = np.full([nlat, nlevs], np.nan)

    amp_T_SW4 = np.full([nlat, nlevs], np.nan)
    phs_T_SW4 = np.full([nlat, nlevs], np.nan)

    amp_T_SW5 = np.full([nlat, nlevs], np.nan)
    phs_T_SW5 = np.full([nlat, nlevs], np.nan)

    amp_T_SE1 = np.full([nlat, nlevs], np.nan)
    phs_T_SE1 = np.full([nlat, nlevs], np.nan)

    amp_T_SE2 = np.full([nlat, nlevs], np.nan)
    phs_T_SE2 = np.full([nlat, nlevs], np.nan)

    amp_T_SE3 = np.full([nlat, nlevs], np.nan)
    phs_T_SE3 = np.full([nlat, nlevs], np.nan)

    amp_T_SE4 = np.full([nlat, nlevs], np.nan)
    phs_T_SE4 = np.full([nlat, nlevs], np.nan)

    amp_T_SE5 = np.full([nlat, nlevs], np.nan)
    phs_T_SE5 = np.full([nlat, nlevs], np.nan)

    y = np.full([Nt, nlevs, nlat, Nz], np.nan, np.complex)
    # Pyy = np.full([Nt, nlevs, nlat, Nz], np.nan)
    ampl_s = np.full([Nt, nlevs, nlat, Nz], np.nan)
    ang_s = np.full([Nt, nlevs, nlat, Nz], np.nan)

    # ------------统计数据空值
    # zz/=num[i]
    # for i in range(nlat):
    #     for j in range(nlevs):
    #         if (T[:, j, i, :] == False).all() or (T[:, j, i, :] == 0).all():
    #             zz = 1
    #         print(1, j, 2, i)

    # 1890个点只有33个点有数据。。。。。。。。。。。。。。。。。。。。降低分辨率20210907 Lsperiod=np.linspoace(0,360,61)
    # 20210908经调整list_p类型wei float后经测试仅有234个点没有数据（1,5）
    # 换位LSperiod = np.linspace(0, 360, 13)试试看

    # ---------------------------------
    # --------------------20210908怀疑波动太大是由于间隔太大，考虑使ls和lon两个维度更密集一些
    # aaww/=num[i]
    # pop = T[:, 13, 0, :]
    # print(T[:, 13, 0, :])
    # dsa = amp_T_DW1[:, :, 5]
    # print(amp_T_DW1[:, :, 5])
    # ------------------20210908测试发现：满足数据量>0.8max的点比较少，但不是没有，所以考虑叠加两年的数据试试看。
    # for i in range(nlat):
    #     for j in range(nlevs):
    # aassa = T[:, j, i, :]
    # aassa[aassa > 0] = 1
    # if np.sum(aassa) > 72 * 0.8: print(1, i, 2, j)
    # ---------------------
    for i in range(nlat):
        for j in range(nlevs):

            if (T[:, j, i, :] == False).all() or (T[:, j, i, :] == 0).all():
                # zz=1
                continue
            y[:, j, i, :] = np.fft.fftshift(np.fft.fft2(T[:, j, i, :]))  # 2D fft
            ampl_s[:, j, i, :] = np.absolute(y[:, j, i, :]) / (Nz * Nt)  # amplitude
            ang_s[:, j, i, :] = np.angle(y[:, j, i, :])  # phase

            if (ampl_s[:, j, i, :] == False).all():
                continue
            # ----------------------------筛选数据
            aassa = T[:, j, i, :]
            aassa[aassa > 0] = 1
            if not np.sum(aassa) > 72 * 0.8: continue
            # -------------------------------
            # the amplitude of waves are doubled due to symmetry and only positive frequencies are considered

            amp_T_DW1[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == 1]
            phs_T_DW1[i,j] = -ang_s[freq == 1, j, i, wavenumber == 1]

            amp_T_DW2[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == 2]
            phs_T_DW2[i,j] = -ang_s[freq == 1, j, i, wavenumber == 2]

            amp_T_DW3[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == 3]
            phs_T_DW3[i,j] = -ang_s[freq == 1, j, i, wavenumber == 3]

            amp_T_DW4[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == 4]
            phs_T_DW4[i,j] = -ang_s[freq == 1, j, i, wavenumber == 4]

            amp_T_DW5[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == 5]
            phs_T_DW5[i,j] = -ang_s[freq == 1, j, i, wavenumber == 5]

            amp_T_DS0[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == 0]
            phs_T_DS0[i,j] = -ang_s[freq == 1, j, i, wavenumber == 0]

            amp_T_DE1[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == -1]
            phs_T_DE1[i,j] = -ang_s[freq == 1, j, i, wavenumber == -1]

            amp_T_DE2[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == -2]
            phs_T_DE2[i,j] = -ang_s[freq == 1, j, i, wavenumber == -2]

            amp_T_DE3[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == -3]
            phs_T_DE3[i,j] = -ang_s[freq == 1, j, i, wavenumber == -3]

            amp_T_DE4[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == -4]
            phs_T_DE4[i,j] = -ang_s[freq == 1, j, i, wavenumber == -4]

            amp_T_DE5[i,j] = 2 * ampl_s[freq == 1, j, i, wavenumber == -5]
            phs_T_DE5[i,j] = -ang_s[freq == 1, j, i, wavenumber == -5]

            amp_T_bg[i,j] = ampl_s[freq == 0, j, i, wavenumber == 0]
            phs_T_bg[i,j] = -ang_s[freq == 0, j, i, wavenumber == 0]

            amp_T_SPW1[i,j] = 2 * ampl_s[freq == 0, j, i, wavenumber == 1]
            phs_T_SPW1[i,j] = -ang_s[freq == 0, j, i, wavenumber == 1]

            amp_T_SPW2[i,j] = 2 * ampl_s[freq == 0, j, i, wavenumber == 2]
            phs_T_SPW2[i,j] = -ang_s[freq == 0, j, i, wavenumber == 2]

            amp_T_SPW3[i,j] = 2 * ampl_s[freq == 0, j, i, wavenumber == 3]
            phs_T_SPW3[i,j] = -ang_s[freq == 0, j, i, wavenumber == 3]

            amp_T_SPW4[i,j] = 2 * ampl_s[freq == 0, j, i, wavenumber == 4]
            phs_T_SPW4[i,j] = -ang_s[freq == 0, j, i, wavenumber == 4]

            amp_T_SPW5[i,j] = 2 * ampl_s[freq == 0, j, i, wavenumber == 5]
            phs_T_SPW5[i,j] = -ang_s[freq == 0, j, i, wavenumber == 5]

            amp_T_SW1[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == 1]
            phs_T_SW1[i,j] = -ang_s[freq == 2, j, i, wavenumber == 1]

            amp_T_SW2[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == 2]
            phs_T_SW2[i,j] = -ang_s[freq == 2, j, i, wavenumber == 2]

            amp_T_SW3[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == 3]
            phs_T_SW3[i,j] = -ang_s[freq == 2, j, i, wavenumber == 3]

            amp_T_SW4[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == 4]
            phs_T_SW4[i,j] = -ang_s[freq == 2, j, i, wavenumber == 4]

            amp_T_SW5[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == 5]
            phs_T_SW5[i,j] = -ang_s[freq == 2, j, i, wavenumber == 5]

            amp_T_SE1[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == -1]
            phs_T_SE1[i,j] = -ang_s[freq == 2, j, i, wavenumber == -1]

            amp_T_SE2[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == -2]
            phs_T_SE2[i,j] = -ang_s[freq == 2, j, i, wavenumber == -2]

            amp_T_SE3[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == -3]
            phs_T_SE3[i,j] = -ang_s[freq == 2, j, i, wavenumber == -3]

            amp_T_SE4[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == -4]
            phs_T_SE4[i,j] = -ang_s[freq == 2, j, i, wavenumber == -4]

            amp_T_SE5[i,j] = 2 * ampl_s[freq == 2, j, i, wavenumber == -5]
            phs_T_SE5[i,j] = -ang_s[freq == 2, j, i, wavenumber == -5]
    return amp_T_DW1