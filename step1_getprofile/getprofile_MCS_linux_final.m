clear all;close all;clc;   
% CoreNum=6; %设定机器CPU核心数量
% if isempty(gcp('nocreate')) %如果并行未开启
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
         
      
fid=fopen(strcat(file_path,Filesname (j).name));  %打开文本文件
% disp(strcat(file_path,Filesname (j).name));
cal_time=1;
cal_data=1;
lastcal_time=1;
    dataline=dataline+1;
this=0;
while ~feof(fid)
   this=this+1;
str = fgetl(fid)
s=regexp(str,',');   % 找出str中的空格, 以空格作为分割数据的字符
  
    lststr=str(s(1):s(2));
    lststr=lststr(9:16)
    lstnow(this)=str2num(lststr(1:2))+str2num(lststr(4:5))/60;
    Tnow(this)=str2num(str(s(15):s(16)));
    pressurenow(this)=str2num(str(s(37):s(38)));
    pressureerrnow(this)=str2num(str(s(38):s(39)));

end
%disp(time(lastcal_time,:)); error, why?

% lastcal_time=cal_time;
end
fclose(fid);
   
%temp=str2num(str(s(20):s(21)));%找出某个数据,作为保存与否的判断条件
disp(timenow);


