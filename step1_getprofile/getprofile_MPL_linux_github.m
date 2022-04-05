clear all;close all;clc;   


p = genpath('/mnt/7d3fc9f7-c9d4-46ff-bc71-c15c1adc5e75/zj/zj/mars/MCS/atmos.nmsu.edu/PDS/data/');
linenow=length('/mnt/7d3fc9f7-c9d4-46ff-bc71-c15c1adc5e75/zj/zj/mars/MCS/atmos.nmsu.edu/PDS/data/');
lineori=length('/mnt/7d3fc9f7-c9d4-46ff-bc71-c15c1adc5e75/zj/zj/mars/MCS/atmos.nmsu.edu/PDS/data/');
linedif=linenow-lineori;
length_p = size(p,2);
path = {};
temp = [];
warning off 

for i = 1:length_p 
    if p(i) ~= ':'
        %window; linux:
        temp = [temp p(i)];
        
    else
%         disp(temp)
        if contains(temp,'DATA')
        temp = [temp '/']; 
        path = [path ; temp];
        temp = [];
        end
    end
end  

 clear p length_p temp;

 
dataline=0;
file_num = size(path,1);
timenow='';
lasttime='';
datanow=0;a=0;
start=5200;
for k = 1:file_num 
    
    if k<start
        continue;
    end
    
    %更换设备要重新设置70 100
    if length( path{k})>115+linedif && length( path{k})<150+linedif
        
    file_path =  path{k}; 
    Filesname = dir(strcat(file_path,'*.TAB'));
    Length = length(Filesname);
    dataline=dataline+1;
    

     for j = 1:Length   
         
      
fid=fopen(strcat(file_path,Filesname (j).name));  
% disp(strcat(file_path,Filesname (j).name));
cal_time=1;
cal_data=1;
lastcal_time=1;


while ~feof(fid)
   
str = fgetl(fid); 
s=regexp(str,',');   
%time


if length(s)==76
    

    if contains(str(s(1):s(2)),'Date')
        continue
    end
    astr=str(s(1):s(2));
    time(cal_time,:)=astr(4:end-2);
    timenow=astr(4:end-2);
    
    utcstr=str(s(2):s(3));
    utc(cal_time,:)=utcstr(4:end-2);
    
    
    if a==0
        lasttime=timenow;
        a=a+1;
    end
    
    trans_time=datestr(timenow,'yyyy-mm-dd');
    final_time(cal_time,:)=[str2num(trans_time(1:4)),str2num(trans_time(6:7)),str2num(trans_time(9:10))];
    
    szastr=str(s(10):s(11));
    sza(cal_time,:)=abs(90-str2num(szastr(2:end-1)));
    
    lsstr=str(s(4):s(5));
    ls(cal_time,:)=str2num(lsstr(2:end-1));
    
    lststr=str(s(11):s(12));
    lst(cal_time,:)=str2num(lststr(2:end-1))*24;
    
    cal_data=1;
cal_time=cal_time+1;
end


%data
if length(s)==14
    if contains(str(s(11):s(12)),'ice')
        continue
    end
    alt(cal_time,cal_data)=str2num(str(s(12):s(13)));   
    lat(cal_time,cal_data)=str2num(str(s(13):s(14)));   
    lon(cal_time,cal_data)=str2num(str(s(14):end)); 
    pressure(cal_time,cal_data)=str2num(str(s(1):s(2)));
    T(cal_time,cal_data)=str2num(str(s(2):s(3)));
    Terr(cal_time,cal_data)=str2num(str(s(3):s(4)));
    dust(cal_time,cal_data)=str2num(str(s(4):s(5)));
    dusterr(cal_time,cal_data)=str2num(str(s(5):s(6)));
    waterice(cal_time,cal_data)=str2num(str(s(8):s(9)));
    watericeerr(cal_time,cal_data)=str2num(str(s(9):s(10)));

    cal_data=cal_data+1;
    

end
if cal_time==1
    continue
end

if cal_time-lastcal_time==1 && cal_time>2
% disp(time(lastcal_time,:));
% disp(alt(lastcal_time,10))
% disp((k-1)*Length+j)
% disp(lastcal_time)
data(dataline,lastcal_time-1).time=final_time(lastcal_time,:);
data(dataline,lastcal_time-1).lst=lst(lastcal_time,:);
data(dataline,lastcal_time-1).sza=sza(lastcal_time,:);
data(dataline,lastcal_time-1).ls=ls(lastcal_time,:);
data(dataline,lastcal_time-1).utc=utc(lastcal_time,:);

data(dataline,lastcal_time-1).alt=alt(lastcal_time,:);
data(dataline,lastcal_time-1).lat=lat(lastcal_time,:);
data(dataline,lastcal_time-1).lon=lon(lastcal_time,:);

data(dataline,lastcal_time-1).pressure=pressure(lastcal_time,:);
data(dataline,lastcal_time-1).T=T(lastcal_time,:);
data(dataline,lastcal_time-1).Terr=Terr(lastcal_time,:);
data(dataline,lastcal_time-1).dust=dust(lastcal_time,:);
data(dataline,lastcal_time-1).dusterr=dusterr(lastcal_time,:);
data(dataline,lastcal_time-1).waterice=waterice(lastcal_time,:);
data(dataline,lastcal_time-1).watericeerr=watericeerr(lastcal_time,:);

datanow=data;
end
%disp(time(lastcal_time,:)); error, why?

lastcal_time=cal_time;
end
fclose(fid);
    end
    end
%temp=str2num(str(s(20):s(21)));
disp(timenow);

if rem(k,100)==0 | k==file_num
    a=datestr(lasttime,'yyyy-mm-dd');
    b=datestr(timenow,'yyyy-mm-dd');
    if a==b
        continue;
    end
    sttr=['./MCS_data_right/MCS_',a,'_',b,'.mat'];
    folder='./MCS_data_right/'; 
    if exist(folder)==0 
    mkdir(folder); 
    end
    save (sttr,'datanow');
    clear data,datanow;
    lasttime=timenow;
    dataline=0;
%     pack;
end
end