
%%
clear all
tic

disp('calculation begins...');

MY_LS=linspace(0,360,73);
for i=1:length(MY_LS)-1
    MY_LSmiddle(i)=(MY_LS(i)+MY_LS(i+1))/2;
end
gapMY_LS=MY_LSmiddle(1)-MY_LS(1);
LT=linspace(0,24,13);
for i=1:length(LT)-1
    LTmiddle(i)=(LT(i)+LT(i+1))/2;
end
gapLT=LTmiddle(1)-LT(1);
%% km
ALT=linspace(0,100,101);
for i=1:length(ALT)-1
    ALTmiddle(i)=(ALT(i)+ALT(i+1))/2;
end
gapALT=ALTmiddle(1)-ALT(1);


LAT=linspace(-90,90,37);
for i=1:length(LAT)-1
    LATmiddle(i)=(LAT(i)+LAT(i+1))/2;
end
gapLAT=LATmiddle(1)-LAT(1);


LON=linspace(-180,180,37);
for i=1:length(LON)-1
    LONmiddle(i)=(LON(i)+LON(i+1))/2;
end
gapLON=LONmiddle(1)-LON(1);

profilefolder='./profile/';
Filesname = dir(strcat(profilefolder,'*.mat'));
Length = length(Filesname);
T_final=zeros(size(MY_LSmiddle,2),size(LTmiddle,2),size(ALTmiddle,2),size(LATmiddle,2),size(LONmiddle,2));
Terr_final=zeros(size(MY_LSmiddle,2),size(LTmiddle,2),size(ALTmiddle,2),size(LATmiddle,2),size(LONmiddle,2));
T_number=zeros(size(MY_LSmiddle,2),size(LTmiddle,2),size(ALTmiddle,2),size(LATmiddle,2),size(LONmiddle,2));

total_number_point=0;total_number_downlimit_point=0;total_number_downlimit_uplimit_point=0;
total_number_profile=0;total_number_downlimit_profile=0;total_number_downlimit_uplimit_profile=0;
for jj = 1:Length
    istes=0;
    
    folder=profilefolder;
    file=Filesname (jj).name;
    disp(['calculate ' file])
    name=file(1:end-4);
    
    data = cell2mat(struct2cell(load([folder file])));
    % kanyixia=data(1);
    a=size(data);
    %% TES 1*1 struct 
    if contains(file,'TES')
        istes=1;
        disp('find TES data and change it into proper mat...')
        for idata=1:size(data.lat,1)
           
            data1(idata).z=data.z(idata,:);
            data1(idata).lst=data.lst(idata,1);
            data1(idata).lat=data.lat(idata,1);
            data1(idata).lon=data.lon(idata,1);
            data1(idata).date=data.date(idata,:);
            data1(idata).ls=data.ls(idata,1);
            data1(idata).T=data.T(idata,:);
            data1(idata).Terr=data.Terr(idata,1);
        end
        data=data1;
        clear data1
    end
    a=size(data);
    disp('convert successfully!')
    %% get profile
    disp('get every profile...')
    for i=1:a(1)
        
        for j=1:a(2)
            
            
            
            if isfield(data,'time')
                timenow=data(i,j).time;
                if isempty(timenow)
                    continue;
                end
                timenow=[num2str(timenow(1)) '-' num2str(timenow(2)) '-' num2str(timenow(3))];
            else
                %                data=cell2mat(struct2cell(data));
                timenow=data(i,j).date;
                if size(timenow,2)==3
                    %timenow=[2011,11,1]
                    if isempty(timenow)
                        continue;
                    end
                    timenow=[num2str(timenow(1)) '-' num2str(timenow(2)) '-' num2str(timenow(3))];
                else
                    %timenow1='2011-11-1' 
                    if isempty(timenow)
                        continue;
                    end
                end
            end
            
            
            
          
            %% LS
            lsnow=data(i,j).ls;my_lsnow=lsnow;
            if ~isfield(data,'lst')
                time=data(i,j).time;
                lstnow=str2num(time(1:2));
            else
                lstnow=data(i,j).lst;
            end
            if isfield(data,'sza')
                szanow=data(i,j).sza;
            end
            %% -180~180
            lonnow=data(i,j).lon;
            if max(lonnow)>180
                lonnow=lonnow-180;
            end
            latnow=data(i,j).lat;
            %% 
            if ~isfield(data,'T')
                disp([file ' does not have the temperature data (T) .']);
                break
            end
            %%
            Tnow=data(i,j).T;
            Tnow(isnan(Tnow))=0;
           
            if ~sum(sum(Tnow))  
               
                continue;
            end
            %%
            if size(Tnow,1)>size(Tnow,2)
                Tnow=Tnow';latnow=latnow';lonnow=lonnow';lstnow=lstnow';my_lsnow=my_lsnow';
            end
            
            if isfield(data,'alt')
                altnow=data(i,j).alt;
            elseif isfield(data,'z')
                %% km
                altnow=data(i,j).z;
                if istes|max(altnow)>500
                    altnow=altnow/1000;
                end
            end
            if isempty(altnow)
                continue;
            end
            if size(altnow,1)>size(altnow,2)
                altnow=altnow';
            end
            %% quality control according to CO2
            %                 altnow=zeros(1,50);
            %                 altnow(:)=2
            if min(altnow)>100 | max(altnow)<0
                continue;
            end
            [CO2_condensation_T,upper_limit_T]=quality_control(altnow);
            %                 CO2_condensation_T
            %                 upper_limit_T
            %                 altnow
          
            
            
            %% get data
            if length(Tnow)~=length(altnow)&&length(altnow)>1
                disp('Tnow is unmatched with altnow, pass...')
                continue;
            end
           
            
            if isfield(data,'T_ut')
                Terrnow=data(i,j).T_ut;
            elseif isfield(data,'Terr')
                Terrnow=data(i,j).Terr;
            end
            
            %% number
            total_number_profile=total_number_profile+1;
            ifthisprofileok=0;
            
            %% cycle
            for profile=1:size(Tnow,2)
                %% quality control
                
                if isnan(Tnow(profile)) | Tnow(profile)==-9999 | Tnow(profile)<1
                    continue;
                end
                total_number_point=total_number_point+1;
                
                if Tnow(profile)<CO2_condensation_T(profile)
                    continue;
                end
                total_number_downlimit_point=total_number_downlimit_point+1;
                if Tnow(profile)>upper_limit_T(profile)
                    %                     disp(Tnow(profile))
                    %                     disp(upper_limit_T(profile))
                    continue;
                end
                total_number_downlimit_uplimit_point=total_number_downlimit_uplimit_point+1;
                
                for index_MY_LS=1:length(MY_LSmiddle)
                    if length(my_lsnow)>1
                        if abs(my_lsnow(profile)-MY_LSmiddle(index_MY_LS))>gapMY_LS
                            continue;
                        end
                    else
                        if abs(my_lsnow-MY_LSmiddle(index_MY_LS))>gapMY_LS
                            continue;
                        end
                    end
                    for index_LT=1:length(LTmiddle)
                        if length(lstnow)>1
                            if abs(lstnow(profile)-LTmiddle(index_LT))>gapLT
                                continue;
                            end
                        else
                            if abs(lstnow-LTmiddle(index_LT))>gapLT
                                continue;
                            end
                        end
                        
                        for index_ALT=1:length(ALTmiddle)
                            
                            
                            
                            if length(altnow)>1
                                if abs(altnow(profile)-ALTmiddle(index_ALT))>gapALT
                                    continue;
                                end
                            else
                                if abs(altnow-ALTmiddle(index_ALT))>gapALT
                                    continue;
                                end
                            end
                            
                            for index_LAT=1:length(LATmiddle)
                                if length(latnow)>1
                                    if abs(latnow(profile)-LATmiddle(index_LAT))>gapLAT
                                        continue;
                                    end
                                else
                                    if abs(latnow-LATmiddle(index_LAT))>gapLAT
                                        continue;
                                    end
                                end
                                
                                
                                for index_LON=1:length(LONmiddle)
                                    if length(lonnow)>1
                                        if abs(lonnow(profile)-LONmiddle(index_LON))>gapLON
                                            continue;
                                        end
                                    else
                                        if abs(lonnow-LONmiddle(index_LON))>gapLON
                                            continue;
                                        end
                                    end
                                    
                                   
                                    T_final(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)=T_final(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)+Tnow(profile);
                                   
                                    if exist('Terrnow','var')
                                        if length(Terrnow)>1
                                            Terr_final(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)=Terr_final(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)+Terrnow(profile);
                                        end
                                        if length(Terrnow)==1
                                            Terr_final(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)=Terr_final(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)+Terrnow;
                                        end
                                    end
                                    
                                    T_number(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)=T_number(index_MY_LS,index_LT,index_ALT,index_LAT,index_LON)+1;
                                    
                                    ifthisprofileok=1;
                                    
                                    
                                end
                            end
                        end
                    end
                end
                
            end
            if ifthisprofileok==1
                total_number_downlimit_uplimit_profile=total_number_downlimit_uplimit_profile+1;
            end
        end
    end
    
    clear Terrnow
    
end
%mean the data
T_number(T_number==0)=1;
T_final(T_final==0)=nan;
T_final=T_final./T_number;
if sum(Terr_final(:))~=0
    Terr_final=Terr_final./T_number;
else
    disp('there is no error information.')
end
% dust_number(dust_number==0)=1;waterice_number(waterice_number==0)=1;
% dust_final=dust_final./dust_number;dusterr_final=dusterr_final./dust_number;
% waterice_final=waterice_final./waterice_number;watericeerr_final=watericeerr_final./waterice_number;

%save
savedir='./72_12_100_36_36_middle_quality_control/';
if exist(savedir)==0 
    mkdir(savedir); 
end
disp(['save T_72_12_100_36_36_middle_quality_control'])
save([savedir 'T.mat'],'T_final');
if sum(Terr_final(:))~=0
    disp(['save Terr_72_12_100_36_36_middle_quality_control'])
    save([savedir 'Terr.mat'],'Terr_final');
end

total_number_point
total_number_downlimit_point
total_number_downlimit_uplimit_point
total_number_profile
total_number_downlimit_profile
total_number_downlimit_uplimit_profile

save('./number_72_12_100_36_36_middle_quality_control.mat','total_number_point','total_number_downlimit_point','total_number_downlimit_uplimit_point','total_number_profile','total_number_downlimit_profile','total_number_downlimit_uplimit_profile')













toc