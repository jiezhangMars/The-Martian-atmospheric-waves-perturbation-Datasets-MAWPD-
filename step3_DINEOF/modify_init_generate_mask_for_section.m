function modify_init_generate_mask_for_section(sectionname,sectiondata,dataname,initfolder)
%% set name 
% sectionname='asasa111';
filename = 'dineof.init';
newfilename=[initfolder dataname '_dineof_' sectionname '.init'];
str_data=['data = [''' dataname '_' sectionname '.data'']'];
str_filled=['results = [''' dataname '_' sectionname '.filled'']'];
str_mask=['mask = [''' dataname '_' sectionname '.mask'']'];
str_output=['Output = ''Output_jie/'''];
%% 替换含有特定字符的行
%并行时init重命名出错，单独执行可以，现在测试串行可否，问题在于最后一条output的把之前覆盖了
replace_the_line_contains_something(filename,newfilename,str_data,'data');
replace_the_line_contains_something(newfilename,newfilename,str_mask,'mask');
replace_the_line_contains_something(newfilename,newfilename,str_filled,'results');
replace_the_line_contains_something(newfilename,newfilename,str_output,'Output =');

datafile=['./' dataname '_' sectionname '.data'];maskfile=['./' dataname '_' sectionname '.mask'];
% disp(datafile);disp(maskfile);
% disp(211212);save('./sectiondata.mat','sectiondata');

%% create the mask and data file
file1=gwrite(datafile,sectiondata);
mask=squeeze(sectiondata(:,:,1));mask(:)=1;file2=gwrite(maskfile,mask);



end