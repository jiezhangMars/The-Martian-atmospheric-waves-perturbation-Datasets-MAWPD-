clear all;close all;clc;
% CoreNum=6; 
% if isempty(gcp('nocreate'))
%     parpool(CoreNum);
% end
% load('./MCS_data/MCS_2014-11-11_2015-02-10.mat');

p = genpath('/home/gw/C/zj_now/data/MCS_read/step1_getprofile_MCS/data/');
length_p = size(p,2);
path = {};
temp = [];
warning off
dataline=0;
file_num = size(path,1);
timenow='';
lasttime='';
datanow=0;a=0;
file_path =  './data/';
Filesname = dir(strcat(file_path,'*.TAB'));
Length = length(Filesname);

for j = 1:Length
    
    
    fid=fopen(strcat(file_path,Filesname (j).name));  
    % disp(strcat(file_path,Filesname (j).name));
    cal_time=1;
    cal_data=1;
    lastcal_time=1;
    dataline=dataline+1;
    this=0;
    while ~feof(fid)
        this=this+1;
        str = fgetl(fid)
        s=regexp(str,',');  
        
        lststr=str(s(1):s(2));
        lststr=lststr(9:16)
        lstnow(this)=str2num(lststr(1:2))+str2num(lststr(4:5))/60;
        Tnow(this)=str2num(str(s(15):s(16)));
        pressurenow(this)=str2num(str(s(37):s(38)));
        pressureerrnow(this)=str2num(str(s(38):s(39)));
       
    end
   
end
fclose(fid);

disp(timenow);


