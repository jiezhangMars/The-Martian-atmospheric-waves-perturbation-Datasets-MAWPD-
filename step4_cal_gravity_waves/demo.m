% ���ڹ�����ļ�������2GB�ı�������Ҫʹ��MAT-file�汾7.3����߰汾��
% ����������£�
% % ����matlab����ҳ�������Ԥ�衱��ť��ѡ�񡰳��桱�����MAT-File��ѡ���һ��ѡ�����
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


