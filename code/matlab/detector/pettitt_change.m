function [means,stds,ipt,U] = pettitt_change(data)
% This code is used to find the change point in a univariate continuous time series

% using Pettitt Test.

%

%

% The test here assumed is two-tailed test. The hypothesis are as follow:

%  H (Null Hypothesis): There is no change point in the series

%  H(Alternative Hypothesis): There is a change point in the series

% 

% Input: univariate data series

% Output:

% The output of the answer in row wise respectively,

% loc: location of the change point in the series, index value in

% the data set

% K: Pettitt Test Statistic for two tail test

% pvalue: p-value of the test

%

%Reference: Pohlert, Thorsten. "Non-Parametric Trend Tests and Change-Point Detection." (2016).

% 
n=length(data);
s=0;
U=zeros(n-1,0);
for i=1:n-1
    for j=i+1:n
      s=s+sign(data(i)-data(j));
    end
    U(i)=s;
end

ipt=find(abs(U)==max(abs(U)));

K=max(abs(U));
pvalue=2*exp((-6*K^2)/(n^3+n^2));
if length(ipt)>1
    ipt=floor(mean(ipt));
end
means=[mean(data(1:ipt-1));mean(data(ipt:end))];
stds=[std(data(1:ipt-1));std(data(ipt:end))];

U=U';
end

