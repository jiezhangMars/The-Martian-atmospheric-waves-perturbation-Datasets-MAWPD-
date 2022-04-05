

%% 判断上一步是否做�?
foldertarget='F:\dataset\step2_gridding_gw_T\72_12_100_36_36_middle_quality_control\';
% for i=1:10000
%     
%     disp('see if gridding ok?')
%     
%     if size(dir(foldertarget),1)==4
%         disp('gridding ok!')
%         break;
%     else
%         disp('still gridding...')
%     end
%     pause(60*10);
% end

%% beginning set
addpath './Scripts/IO'
tic
myCluster = parcluster('local');
delete(myCluster.Jobs);

%% dineof_horizontal
folder_T=foldertarget;%注意单独运行时别被后面覆盖了
filled_folder_horizontal='./dineof_72_12_100_37_37_filledresult/';
mat_folder_horizontal='./dineof_72_12_100_37_37_matresult/';
cal_information_folder='./cal_information_72_12_100_37_37/';
disp('dineof_72_12_100_37_37 calculation begins!');
divide_data_into_sections_and_calculate(filled_folder_horizontal,folder_T,cal_information_folder,'E.mat');
divide_data_into_sections_and_calculate(filled_folder_horizontal,folder_T,cal_information_folder,'GW_perturbation.mat');
% divide_data_into_sections_and_calculate(filled_folder_horizontal,folder_T,cal_information_folder,'number_72_12_100_36_36_middle_quality_control_1.mat');
divide_data_into_sections_and_calculate(filled_folder_horizontal,folder_T,cal_information_folder,'T.mat');
disp('converting dineof_72_12_100_37_37 calculation results to mat file...');
fuyuan_horizontal(mat_folder_horizontal,filled_folder_horizontal,folder_T,'E.mat','E');
fuyuan_horizontal(mat_folder_horizontal,filled_folder_horizontal,folder_T,'GW_perturbation.mat','GW_perturbation');
% fuyuan_horizontal(mat_folder_horizontal,filled_folder_horizontal,folder_T,'number_72_12_100_36_36_middle_quality_control_1.mat');
fuyuan_horizontal(mat_folder_horizontal,filled_folder_horizontal,folder_T,'T.mat','T');
%% dineof_alt_lat
% tic
% folder_T='./grid_result_iuvs_ngims_mpl_odyssey_mcs_spicam/';%注意单独运行时别被后面覆盖了
% filled_folder_alt_lat='./dineof_alt_lat_filledresult/';
% mat_folder_alt_lat='./dineof_alt_lat_matresult/';
% disp('dineof_vertical calculation begins!');
% divide_data_into_sections_and_calculate_alt_lat(filled_folder_alt_lat,folder_T,'T.mat');
% divide_data_into_sections_and_calculate_alt_lat(filled_folder_alt_lat,folder_T,'Terr.mat');
% disp('converting dineof_vertical calculation results to mat file...');
% fuyuan_alt_lat(mat_folder_alt_lat,filled_folder_alt_lat,folder_T,'T.mat');
% fuyuan_alt_lat(mat_folder_alt_lat,filled_folder_alt_lat,folder_T,'Terr.mat');
% toc
%% dineof_vertical
% tic
% folder_T='./dineof_horizontal_matresult/';
% filled_folder_vertical='./dineof_vertical_filledresult/';
% mat_folder_vertical='./dineof_vertical_matresult/';
% disp('dineof_vertical calculation begins!');
% divide_data_into_sections_and_calculate_vertical(filled_folder_vertical,folder_T,'T.mat');
% divide_data_into_sections_and_calculate_vertical(filled_folder_vertical,folder_T,'Terr.mat');
% disp('converting dineof_vertical calculation results to mat file...');
% fuyuan_vertical(mat_folder_vertical,filled_folder_vertical,folder_T,'T.mat');
% fuyuan_vertical(mat_folder_vertical,filled_folder_vertical,folder_T,'Terr.mat');
% toc
%% dineof_3rd
% tic
% folder_T='./dineof_vertical_matresult/';
% filled_folder_3rd='./dineof_3rd_filledresult/';
% mat_folder_3rd='./dineof_3rd_matresult/';
% disp('dineof_3rd calculation begins!');
% divide_data_into_sections_and_calculate(filled_folder_3rd,folder_T,'T.mat');
% divide_data_into_sections_and_calculate(filled_folder_3rd,folder_T,'Terr.mat');
% disp('converting dineof_vertical calculation results to mat file...');
% fuyuan_horizontal(mat_folder_3rd,filled_folder_3rd,folder_T,'T.mat');
% fuyuan_horizontal(mat_folder_3rd,filled_folder_3rd,folder_T,'Terr.mat');
% toc
%% other elements
% 
% folder_dust='/home/gw/C/zj_now/data/MCS_read/step2_gridding/grid_result_dust/';
% divide_data_into_sections_and_calculate(folder_dust,'dust.mat');
% divide_data_into_sections_and_calculate(folder_dust,'dusterr.mat');

% folder_waterice='/home/gw/C/zj_now/data/MCS_read/step2_gridding/grid_result_waterice/';
% divide_data_into_sections_and_calculate(folder_waterice,'waterice.mat');
% divide_data_into_sections_and_calculate(folder_waterice,'watericeerr.mat');

%% time calculation

toc


