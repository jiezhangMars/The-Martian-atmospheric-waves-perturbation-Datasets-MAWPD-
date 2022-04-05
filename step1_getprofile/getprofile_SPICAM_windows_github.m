clear all;close all;clc;
tic



fileFolder=fullfile('.\data_temperature\');
dirOutput=dir(fullfile(fileFolder,'*.lbl'));
fileNames={dirOutput.name};
length_fileNames = size(fileNames,2);

dataline=0;
for k = 1:length_fileNames
    file_path =  fileNames{k};
    if ~contains(file_path,'TOBS_ORB')
        continue;
    end
    Length = length(file_path);
    dataline=dataline+1;
    
    fid=fopen(strcat(fileFolder,file_path));  
    cal_time=1;
    cal_data=1;
    lastcal_time=1;
    
    fline=0;
    while ~feof(fid)
        
        
        str = fgetl(fid);
        s=regexp(str,'=');  
        
        %             if ~isempty(s)
        %                 fline=fline+1;
        %             disp(['fline' num2str(fline)])
        %             disp(str(s(1)+1:end))
        %             end
        if isempty(s)
            continue;
        end
        fline=fline+1;
        if fline==16
            timenow=str(s(1)+1:end);
            timenow=timenow(1:10);
            trans_time=datestr(timenow,'yyyy-mm-dd');
            datenow=[str2num(trans_time(1:4)),str2num(trans_time(6:7)),str2num(trans_time(9:10))];
        end
        
        if fline==20
            orbitnow=str2num(str(s(1)+1:end));
        end
        if fline==21
            latnow=str2num(str(s(1)+1:end));
        end
        if fline==22
            lonnow=str2num(str(s(1)+1:end));
        end
        if fline==23
            lsnow=str2num(str(s(1)+1:end));
        end
        if fline==24
            lstnow=str(s(1)+1:end);
            lstnow=lstnow(3:10);
            hour=str2num(lstnow(1:2));minite=str2num(lstnow(4:5));
            lstnow=hour+minite/60;
        end
        if fline==25
            data(dataline).orbitnumber=orbitnow;
            data(dataline).lst=lstnow;
            data(dataline).lat=latnow;
            data(dataline).lon=lonnow;
            data(dataline).date=datenow;
            data(dataline).ls=lsnow;
        end
        if fline>25
            continue;
        end
        
    end
    fclose(fid);
    
prefix=file_path(1:end-4);
fileTAB=[fileFolder prefix '.TAB'];
fid=fopen(fileTAB);
fline=0;
while ~feof(fid) 
    fline=fline+1;
    str = fgetl(fid);
    s=regexp(str,'      ');
    alt(fline)=str2num(str(s(1):s(2)));
    T(fline)=str2num(str(s(2):s(3)));
    Terr(fline)=str2num(str(s(5):end));

end
    data(dataline).z=alt;
    data(dataline).T=T;
    data(dataline).Terr=Terr;

    
end
save('data_spicam.mat','data')
toc





