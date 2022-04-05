function [error]=dineof_jie(sectionname,sectiondata,dataname,savedir)

%% change dineof.init and create the .data and .mask for section
initfolder='./init/';
if exist(initfolder)==0 %判断文件夹是否存�?
    mkdir(initfolder);  %不存在时候，创建文件�?
end
modify_init_generate_mask_for_section(sectionname,sectiondata,dataname,initfolder);

%% set the output file of the validation parameters

if exist('./Output_jie/')==0 %%判断文件夹是否存�?
    mkdir('./Output_jie/');  %%不存在时候，创建文件�?
end
%% execute the dineof file
folder='./';
% ExeFileName='dineof-3.0-x64-linux';
ExeFileName='dineof.exe';
ExeFilePath=fullfile(folder,ExeFileName);
Param1=[' ',[initfolder dataname '_dineof_' sectionname '.init']];%第一个参数，�?��要有' '
% Param2=[' ','15'];
% Cmd=[ExeFilePath ,Param1 ,Param2];
Cmd=[ExeFilePath ,Param1];
system(Cmd);

%get error
% eof=gread('./Output_jie/outputEof.valc');
%% get the crossvalidationerror
eof=gread([folder 'Output_jie/valc.dat'])
eof=eof(2:end);eof(eof<=0)=[];eof=squeeze(eof);%剔除异常�?
crossvalidationerror=min(eof);numberofeigen=find(min(eof)==eof);
error=crossvalidationerror;
%% move the result into the savedir and delete the .data and .mask
file2move=['./' dataname '_' sectionname '.*'];
movefile(file2move,savedir);
end



