function [] = fetch_idx(dp,out4origin)
%FETCH_IDX 此处显示有关此函数的摘要
%   此处显示详细说明
addpath('./detector')
[t,x]=loadGnssTs(dp);
[~,Skk] = Buishand_U_change_point_detection(x);
[~,~,~,U] = pettitt_change(x);
[~,~,~,Tk] = SNHT(x);
[~,~,~,z] = z_test(x);
l=min([length(Skk),length(U),length(Tk),length(z)]);
out=[t(1:l),Skk(1:l),U(1:l),Tk(1:l),z(1:l)];
save(out4origin,'out');
end

