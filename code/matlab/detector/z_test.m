function [means,stds,ipt,z] = z_test(data)
%SNHT 此处显示有关此函数的摘要
%   此处显示详细说明
    n  = length(data);
    z =zeros(n-1,1);
    for i=1:n-1
        seg0=data(1:i);
        seg1=data(i+1:n);
        mean0=mean(seg0);
        mean1=mean(seg1);
        std0=std(seg0);
        std1=std(seg1);
        z(i)=(mean1-mean0)/sqrt(std0^2/i+std1^2/(n-i));
    end
    [~,ipt] = max(z);
    means=[mean(data(1:ipt-1));mean(data(ipt:end))];
    stds=[std(data(1:ipt-1));std(data(ipt:end))];
end

