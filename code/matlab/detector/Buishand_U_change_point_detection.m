function [I,Skk] = Buishand_U_change_point_detection(inputdata)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
    inputdata_mean = mean(inputdata);
    n  = length(inputdata);
    Sk=zeros(n,1);
    for i=0:n-1
        Sk(i+1)=sum(inputdata(1:i+1) - inputdata_mean);
    end
    sigma = sqrt(sum((inputdata-mean(inputdata)).^2)/(n-1));
    U = sum((Sk(1:(n - 1))/sigma).^2)/(n * (n + 1));
    Ska = abs(Sk);
    [~,I] = max(Ska);
    Skk = (Sk/sigma);
end

