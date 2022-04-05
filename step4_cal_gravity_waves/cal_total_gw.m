function cal_total_gw(path,label)
disp(['cal gw of ',label])
addpath .\npy-matlab-master\npy-matlab
% temp=readNPY([path,'temp.npy']);
% temp_p=permute(temp,[5,4,3,2,1]);
disp([path,'T.mat'])
temp=cell2mat(struct2cell(load([path,'T.mat'])));
% disp(size(temp))));
% size(pc_dt)
pc_dt=zeros(size(temp));E=zeros(size(temp));
z=1:100;
for i=1:size(temp,1)
    disp(i)
    for j=1:size(temp,2)
        for k=1:size(temp,4)
            for l=1:size(temp,5)
                T=squeeze(temp(i,j,:,k,l))';
                [pc_dt1,E1]=cal_gw_in_horiz_point(z,T);
                pc_dt(i,j,:,k,l)=pc_dt1;
                E(i,j,:,k,l)=E1;
            end
        end
    end
end
savepath=['./dataset_',label,'/'];
if ~exist(savepath)
    mkdir(savepath)
end
save([savepath,'pc_dt.mat'],'pc_dt');
save([savepath,'E.mat'],'E');
end

