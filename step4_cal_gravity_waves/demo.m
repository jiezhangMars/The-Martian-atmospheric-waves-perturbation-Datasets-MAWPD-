% 对于过大的文件，大于2GB的变量，需要使用MAT-file版本7.3或更高版本。
% 解决方法如下：
% % 进入matlab“主页”点击“预设”按钮，选择“常规”，点击MAT-File，选择第一个选项，如下
% warning('off')
% folder=dir('F:\paper\GRL_TIDE_DUST\work\LMDZ_extract_temp_zmU\nc2npy\');folder=folder(4:end);
% for i=1:length(folder)
% %     i=length(folder)-i;
%     if folder(i).isdir==1
%         tic
%         label=folder(i).name;
%         path=[folder(i).folder,'\',label,'\'];
%         cal_total_gw(path,label);
%         toc
%     end
% end
warning('off');
path='E:\dataset\72_12_100_36_36_middle_quality_control\';
label='72_12_100_36_36_middle_quality_control';
cal_total_gw(path,label);


