clear all;close all;clc;
tic
% CoreNum=6;
% if isempty(gcp('nocreate'))
%     parpool(CoreNum);
% end
% load('./MCS_data/MCS_2014-11-11_2015-02-10.mat');
%%
% myCluster = parcluster('local');
% delete(myCluster.Jobs);
%% get alt
P0=650;
P=[16.5815200,12.9137000,10.0572000,7.8325550,6.1000000,4.7506850,3.6998370,2.8814360,2.2440650,1.747679,1.3610940,1.0600210,0.8255452,0.6429352,0.5007185,0.3899599,0.3037011,0.2365227,0.1842040,0.1434582,0.1117254,0.0870000,0.0678000,0.0528000,0.0411000,0.0320000,0.0249000,0.0194000,0.0151000,0.0118000,0.0091700,0.0071400,0.0055600,0.0043300,0.0033700,0.0026300,0.0020500,0.0015900];
P=P*100;
scaleH=11100;
h=-log(P./P0).*scaleH;
%% initialization
fileFolder=fullfile('./TES_profile_limb/');
dirOutput=dir(fullfile(fileFolder,'*.van'));
fileNames={dirOutput.name};
length_fileNames = size(fileNames,2);
T=zeros(1,38);

for k = 1:length_fileNames
    
    dataline=0;
    
    file_path =  fileNames{k};
    disp(file_path)
    [line_number]=get_line_number(strcat(fileFolder,file_path));
    
    dataname=['TES_' file_path];
    Length = length(file_path);
    
    %% transform file to mat
    disp('transform file to mat...')
    tic
    fid=fopen(strcat(fileFolder,file_path));
    FormatString=repmat('%f ',1,48);
    out =cell2mat(textscan(fid,FormatString,line_number,'HeaderLines',1));
    toc
    
    cal_time=1;
    cal_data=1;
    lastcal_time=1;
    
    
    
    %     h=waitbar(0,[file_path ' is under profiling...']);
    %% create zeros vector
    disp('create zeros vector')
    data_z=zeros(line_number,38);
    data_lst=zeros(line_number,1);
    data_lat=zeros(line_number,1);
    data_lon=zeros(line_number,1);
    data_date=zeros(line_number,3);
    data_ls=zeros(line_number,1);
    data_T=zeros(line_number,38);
    data_Terr=zeros(line_number,1);
    %% parfor begin
    disp('parfor begin...')
    %parfor
    parfor iii=1:line_number-1
        %% parameters
        str=out(iii,:);
        lon=str(6);
        lat=str(2);
        orbit=str(3);
        LS=str(5);
        LT=str(7);
        T=zeros(1,38);
        for i=1:38
            temp=str(9+i);T(i)=temp;
        end
        T(T==444.39999007)=nan;
        Terr=str(48);
        %% time
        second=1/24/3600;
        basetime1=datestr('01-01-2000 12:00:00');
        after=str(9);
        basetime3=datenum(basetime1)+after*second;
        trans_time=datestr(basetime3,'yyyy-mm-dd');
        date=[str2num(trans_time(1:4)),str2num(trans_time(6:7)),str2num(trans_time(9:10))];
        %% add data struct
        data_z(iii,:)=h;
        data_lst(iii,1)=LT;
        data_lat(iii,1)=lat;
        data_lon(iii,1)=lon;
        data_date(iii,:)=date;
        data_ls(iii,1)=LS;
        data_T(iii,:)=T(:);
        data_Terr(iii,1)=Terr;
        
        
    end
    
    data.z=data_z;
    data.lst=data_lst;
    data.lat=data_lat;
    data.lon=data_lon;
    data.date=data_date;
    data.ls=data_ls;
    data.T=data_T;
    data.Terr=data_Terr;
    %%
    if ~exist('./TES_LIMB_mat/')
        mkdir('./TES_LIMB_mat/');
    end
    save(['./TES_LIMB_mat/' dataname '.mat'],'data')
    toc
    tic
    
end







