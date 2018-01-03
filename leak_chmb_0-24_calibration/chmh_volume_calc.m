% Program to calculate the volume of leak test chambers

%filename = '/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/row_1/ch0_0.1_0.8mL.txt';

ppmMatrix = zeros(9,10);
ppmError = zeros(9,10);
transitions = [1514917008.0849, 1514917591.98222, 1514925969.34006, 1514928576.9107, 1514930780.71907
];

% times CO2 level changed from 0 to 0.1; 0.1 to 0.8; 0.2 to 0.7; 0.3 to 0.6; 0.4 to
% 0.5 on last chamber


for n = 1:4 %read in all four files
    filename = strcat('/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/row_1/','ch0_',num2str(n/10), '_',num2str(0.8-n/10+0.1),'mL.txt');

    d = readtable(filename);
    t = table2array(d(:,1)); %times, in epoch time
    ppm = table2array(d(:,3)); %CO2 level in chamber


    %get initial CO2 level--only do in n=1 case
    if n ==1
        tempInitial = zeros(10,1);
        for i = 1:20
            tempInitial(i) = ppm(i);
        end
        ppmMatrix(1,1) = mean(tempInitial);
        ppmError(1,1) = std(tempInitial);
    end
  
    
% For the n = 1 case only
    if n == 1
        for j = 1:2
            ppmAvg = [];

            for i = 1:length(t)
                if (t(i) > transitions(j)) && (t(i) < transitions(j+1)-300)
                    ppmAvg = [ppmAvg ppm(i)];
                    %disp(ppmAvg)
                end
            end

            if j ==1
                ppmMatrix(2,1) = mean(ppmAvg);
                ppmError(2,1) = std(ppmAvg);
            else
                ppmMatrix(9,1) = mean(ppmAvg);
                ppmError(9,1) = std(ppmAvg);
            end
        end
    
    
    % if n != 1:
    else
        for j = 1:2
            ppmAvg = [];

            if j == 1
                for i = 1:length(t)
                    if (t(i) > t(1) +60) && ( t(i) < transitions(n+1)-270 )
                        ppmAvg = [ppmAvg ppm(i)];
                    end
                end
                ppmMatrix(n+1,1) = mean(ppmAvg);
                ppmError(n+1,1) = std(ppmAvg);

            else
                for i = 1:length(t)
                    if (t(i) > transitions(n+1) )
                        ppmAvg = [ppmAvg ppm(i)];
                    end
                end
                ppmMatrix(9-n+1,1) = mean(ppmAvg);
                ppmError(9-n+1,1) = std(ppmAvg);
            end
        end        
    end
    
end






