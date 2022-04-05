function fuyuan_horizontal(savefolder,filefolder,folder_T,matfile,type)
%% get the original mat file as the base file
 data=cell2mat(struct2cell(load([folder_T matfile])));
 disp([folder_T matfile])
 T=data;
 datasize=size(data)
 disp(['The data dimension:',num2str(datasize(1)),num2str(datasize(2)),num2str(datasize(3)),num2str(datasize(4)),num2str(datasize(5))])
%% create initialization dimensions
MY_LS=linspace(30,360,datasize(1));
LT=linspace(2,24,datasize(2));
ALT=linspace(1,100,datasize(3));
LAT=linspace(-90,90,datasize(4));
LON=linspace(-180,180,datasize(5));

if exist(savefolder)==0 %%判断文件夹是否存�?    
mkdir(savefolder);  %%不存在时候，创建文件�?
end
%% replace the original mat file with the filled result in each loop (LT 25,ALT 52) if there is the results of filled file in that loop
for j=1:size(LT,2)
    disp(['calculate to LT ' num2str(j)])
        
        for k=1:size(ALT,2)

            sectionname=[num2str(LT(1,j)) '_' num2str(ALT(1,k))];
            
            file=[filefolder type '_' sectionname '.filled'];
            if exist(file)
%             disp(file)

                dineofresult=gread(file);
                dineofresult=permute(dineofresult,[3,1,2]);
                T(:,j,k,:,:)=dineofresult;
            end
        end
end
%% save 
save([savefolder matfile],'T');


end