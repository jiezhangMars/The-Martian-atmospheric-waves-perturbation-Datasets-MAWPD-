clear all;close all;clc;
tic



fileFolder=fullfile('.\data_temperature\');
dirOutput=dir(fullfile(fileFolder,'*.TAB'));
fileNames={dirOutput.name};
length_fileNames = size(fileNames,2);

dataline=0;
for k = 1:length_fileNames
    file_path =  fileNames{k};
    
    Length = length(file_path);
    dataline=dataline+1;
    
    fid=fopen(strcat(fileFolder,file_path));  %打开文本文件
    cal_time=1;
    cal_data=1;
    lastcal_time=1;
    
    fline=0;
    while ~feof(fid)
        
        
        strs = fgetl(fid);
        str=strsplit(strs);


        fline=fline+1;
        if fline==16
            
            timenow=str(3);
            timenow=timenow{1};
            timenow=timenow(1:10);
            trans_time=datestr(timenow,'yyyy-mm-dd'); 
            datenow=[str2num(trans_time(1:4)),str2num(trans_time(6:7)),str2num(trans_time(9:10))];
            [MARSDATE,LS]=earth2mars(trans_time);
            
            
        end

if fline>42
    latnow=str(3);
    lat(fline-42)=str2num(latnow{1});
    lonnow=str(4);
    lon(fline-42)=str2num(lonnow{1});
    lstnow=str(5);
    lst(fline-42)=str2num(lstnow{1});
    szanow=str(6);
    sza(fline-42)=str2num(szanow{1});
    altnow=str(7);
    alt(fline-42)=str2num(altnow{1});
    Nnow=str(8);
    N(fline-42)=str2num(Nnow{1});
    Nerrnow=str(9);
    Nerr(fline-42)=str2num(Nerrnow{1});

  
end

 end
    data(dataline).z=alt;
    data(dataline).N=N;
    data(dataline).Nerr=Nerr;
    data(dataline).lst=lst;
    data(dataline).lat=lat;
    data(dataline).lon=lon;
    data(dataline).sza=sza;
    data(dataline).date=datenow;
    data(dataline).ls=LS;
    
end
save('data_odyssey.mat','data')
toc





  