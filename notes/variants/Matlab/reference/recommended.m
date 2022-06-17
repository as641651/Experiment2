function [res, time] = recommended(M1, M2, M3, M4, M5)
    tic;
    Y = (M1*transpose(M2)+M3*transpose(M3)+transpose(M4)+transpose(M5));    
    time = toc;
    res = {Y};
end