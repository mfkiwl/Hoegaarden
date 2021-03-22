function [means,stds,ipt,Tk] = SNHT(data)
%SNHT 此处显示有关此函数的摘要
%   此处显示详细说明
    inputdata_mean = mean(data);
    n  = length(data);
    sigma = sqrt(sum((data-mean(data)).^2)/(n-1));
    Tk=zeros(n,1);
    for i=1:n
        Tk(i)=i*(sum((data(1:i)-inputdata_mean)/sigma)/i).^2 + (n-i)*(sum((data(i+1:n)-inputdata_mean)/sigma)/(n-i)).^2;
    end
    [~,ipt] = max(Tk);
    means=[mean(data(1:ipt));mean(data(ipt+1:end))];
    stds=[std(data(1:ipt));std(data(ipt+1:end))];
end

