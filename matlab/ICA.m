clear, clc
load('CV_CVT_data.mat');
[V, K] = eig(CV \ CVT);
K = K * ones(length(K),1);
G = CV * V; 
del_t = 100; % 100 nanoseconds
% Get the trace for calculation of contributions
G2 = sum(G .^2, 1);
TrC = sum(G2);
contri = G2 / TrC;
[contri_sorted, Index] = sort(contri, 'descend');
K_sorted = K(Index);
contri_cumsum = cumsum(contri_sorted);

% Comparison with PCA
[pcV, pcK] = eig(CV);
pcK = pcK * ones(length(pcK), 1);
pcTrC = trace(CV);
pcContri = pcK / pcTrC;
[pcContri_sorted, pcIndex] = sort(pcContri, 'descend');
pcK_sorted = pcK(pcIndex);pcContri_cumsum = cumsum(pcContri_sorted);
