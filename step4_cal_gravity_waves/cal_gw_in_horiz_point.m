function [pc_dt,E]=cal_gw_in_horiz_point(z,T)
%calculate the whole vertical profile gw in the single horizontal point(lat,lon) 

% z=1:100;
% T=1:100;

% loc=find(~isnan(T));locd=find(isnan(T));
% z(isnan(T))=[];T(isnan(T))=[];

T(isnan(T))=nanmean(T);

P_t=polyfit(z,T,7);
T1=polyval(P_t,z);
dt=T-T1;
fs=1;
f1 =1/3;f2 =1/10;
MinWn=  f2/(fs/2);
MaxWn =f1/(fs/2);
[b,a]= butter(6,[MinWn,MaxWn]);
dt_gw=filter(b,a,dt);
pc_dt=dt_gw./T1;
%N2
g=3.711;  % m/s^2 =N/kg
cp=0.844; % KJ/kg*K
aa=length(T1);
%%
z1=z*10^3; % m
N2=g./T1(1:aa-1).*(diff(T1)./diff(z1)+g/(cp*10^3));
N2(aa)=N2(aa-1);
E=1/2*(g^2./N2).*(dt_gw./T).^2;

E(pc_dt>5000)=nan;E(pc_dt<0)=nan;
pc_dt(pc_dt>5000)=nan;pc_dt(pc_dt<0)=nan;


end
%GW energy     E
%GW            pc_dt