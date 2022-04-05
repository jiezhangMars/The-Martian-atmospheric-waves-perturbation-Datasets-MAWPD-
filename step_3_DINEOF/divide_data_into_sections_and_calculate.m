function divide_data_into_sections_and_calculate(savedir,folder,cal_information_folder,file)

%
% CoreNum=55; %设定机器CPU核心数量
% if isempty(gcp('nocreate')) %如果并行未开�?
%     parpool(CoreNum);
% end
%% load the data and get the dataname (like T or dust)
dataname=file(1:end-4);
disp(['loading ' file '...'])
data=cell2mat(struct2cell(load([folder file])));

disp(['cal ' file])% CoreNum=55; %设定机器CPU核心数量
% if isempty(gcp('nocreate')) %如果并行未开�?
%     parpool(CoreNum);
% end


%% create the initialization data
if exist(savedir)==0 %%判断文件夹是否存�?
    mkdir(savedir);  %%不存在时候，创建文件�?
end
datasize=size(data);
disp(['The data dimension:',num2str(datasize(1)),num2str(datasize(2)),num2str(datasize(3)),num2str(datasize(4)),num2str(datasize(5))])
error=zeros(datasize(2),datasize(3));
original_data_number=zeros(datasize(2),datasize(3));
now_data_number=zeros(datasize(2),datasize(3));
jmax=datasize(2);kmax=datasize(3);
%% create initialization dimensions
MY_LS=linspace(30,360,datasize(1));
LT=linspace(2,24,datasize(2));
% ALT=load('altitude.txt');ALT=ALT';
ALT=linspace(1,100,datasize(3));
LAT=linspace(-90,90,datasize(4));
LON=linspace(-180,180,datasize(5));


%% do dineof in each loop (LT 25,ALT 52)
% for i=1:datasize(1)
%     disp(['cal the ' dataname ' of ' num2str(MY_LS(i))])
parfor j=1:jmax
    
    
    for k=1:kmax
        %              [MY,LS]=MY_LS_2_MYANDLS(MY_LS(1,i));
        sectiondata1=squeeze(data(:,j,k,:,:));
        sectiondata=permute(sectiondata1,[2,3,1]);
        sectiondata(sectiondata==0)=nan;
        sectionname=[num2str(LT(1,j)) '_' num2str(ALT(1,k))];
        
        %cal the data number ori
        nan_number=numel(sectiondata(isnan(sectiondata)));
        nonan_number=size(LON,2)*datasize(4)*datasize(1)-nan_number;
        original_data_number(j,k)=nonan_number;
        %缺测99.1%以上的跳过，交叉验证�?��至少8085/894529�?.9%）的数据�?
        %             disp(nonan_number)
        %             if nonan_number<datasize(1)*datasize(4)*datasize(5)*0.009
        %                 continue;
        %             end
        disp(nonan_number)
        %use the dineof.exe
        error(j,k)=dineof_jie(sectionname,sectiondata,dataname,savedir);
        
        if exist([savedir dataname '_' sectionname '.filled'],'file')==0 %%判断文件是否存在
            continue;  %%不存在时�? pass
        end
        
        %cal the data number after
        now_data=gread([savedir dataname '_' sectionname '.filled']);
        nan_number_after=numel(now_data(isnan(now_data)));
        nonan_number_after=size(LON,2)*datasize(4)*datasize(1)-nan_number_after;
        now_data_number(j,k)=nonan_number_after;
    end
end
% end
%%

if exist(cal_information_folder)==0 %%判断文件夹是否存�?
    mkdir(cal_information_folder);  %%不存在时候，创建文件�?
end
disp(['save ' dataname '_error.mat'])
errorfile=[cal_information_folder dataname '_error.mat'];save(errorfile,'error');
disp(['save ' dataname '_original_data_number.mat'])
original_data_numberfile=[cal_information_folder dataname '_original_data_number.mat'];save(original_data_numberfile,'original_data_number');
disp(['save ' dataname '_now_data_number.mat'])
now_data_numberfile=[cal_information_folder dataname '_now_data_number.mat'];save(now_data_numberfile,'now_data_number');



end
