% Program to calculate the volume of leak test chambers
% created by Sam Penders (pende061@umn.edu)

%filename = '/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/row_1/ch0_0.1_0.8mL.txt';

ppmMatrix = zeros(9,10); %matrix to hold averaged ppm level datapoints
ppmError = zeros(9,10); %statistical error on averaged ppm datapoints %where the highest number chamber (4) switches from the first injected level to second
% times CO2 level changed from 0 to 0.1; 0.1 to 0.8; 0.2 to 0.7; 0.3 to 0.6; 0.4 to
% 0.5 on last chamber

for m = 1:2 %row 1 and row 2 data
    for k = 1:5
        for n = 1:4 %read in all four files
            filename = strcat('/home/sam/Mu2e-Factory/Chamber_Volume/row_',num2str(m),'/','ch',num2str(k-1+5*(m-1)),'_',num2str(n/10), '_',num2str(0.8-n/10+0.1),'mL.txt');

            d = readtable(filename);
            t = table2array(d(:,1)); %times, in epoch time
            ppm = table2array(d(:,3)); %temporary -- CO2 level in chamber in each time interval

            if m ==1
                transitions = [1514917008.0849, 1514917591.98222, 1514925969.34006, 1514928576.9107, 1514930780.71907];
            else
                transitions = [1514917398.41982 1514917997.38311 1514926061.61034 1514928669.92289 1514930812.94912];

            end
            
            %get initial CO2 level--only do in n=1 case
            if n ==1
                tempInitial = [];
                for i = 2:14
                    if ppm(i) ~= -1.00
                        tempInitial = [tempInitial ppm(i)];
                        %disp(ppm(i))
                    end
                end
                %disp('END');
                ppmMatrix(1,k+5*(m-1)) = mean(tempInitial);
                %disp(mean(tempInitial));
                ppmError(1,k+5*(m-1)) = std(tempInitial);
            end


        % For the n = 1 case only -- get the 0.1 mL and 0.8 mL ppm level
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
                        ppmMatrix(2,k+5*(m-1)) = mean(ppmAvg);
                        ppmError(2,k+5*(m-1)) = std(ppmAvg);
                    else
                        ppmMatrix(9,k+5*(m-1)) = mean(ppmAvg);
                        ppmError(9,k+5*(m-1)) = std(ppmAvg);
                    end
                end


            % if n != 1: calculate the ppm CO2 level
            else
                for j = 1:2
                    ppmAvg = [];

                    if j == 1
                        for i = 2:15
                            ppmAvg = [ppmAvg ppm(i)];
                        end
                        ppmMatrix(n+1,k+5*(m-1)) = mean(ppmAvg);
                        ppmError(n+1,k+5*(m-1)) = std(ppmAvg);

                    else
                        for i = 1:length(t)
                            if (t(i) > transitions(n+1) )
                                ppmAvg = [ppmAvg ppm(i)];
                            end
                        end
                        ppmMatrix(9-n+1,k+5*(m-1)) = mean(ppmAvg);
                        ppmError(9-n+1,k+5*(m-1)) = std(ppmAvg);
                    end
                end        
            end
        end
    end
end
co2 = 0:0.1:0.8;
co2err =[ [0.01] 0.03*ones(1,4)  0.03*sqrt(2)*ones(1,4)] %estimated error in CO2 volume
fitParameters = zeros(10,2); %slope and its uncertainty

%fixing incorrect data for 0.0, 0.1 mL for ch7--reran test for those, and manually
%entering data
ppmMatrix(1,8) = 81.0769;
ppmMatrix(2,8) = 274.5;
ppmMatrix(9,8) = 1431.667;

%fixing  Incorrect 0.7 mL data for ch5
ppmMatrix(8,6) = 1365.208;

%fixing incorrect data for ch0, ch3: 0.0, 0.1, 0.8 mL
ppmMatrix(1,1) = 94.47;
ppmMatrix(2,1) = 304.227;
ppmMatrix(9,1) = 1480.05;

ppmMatrix(1,4) = 114.13;
ppmMatrix(2,4) = 290.25;
ppmMatrix(9,4) = 1442.118;


for i = 1:10 %fit data and make plots 
    datafit = fit(ppmMatrix(:,i), co2.', 'poly1','Weights',co2err.^-1)
    coeff = coeffvalues(datafit);
    coeff_error = confint(datafit);
    
    fitParameters(i,1) = coeff(1); %slope from fit -> multiply by 10^6 mL for volume in CC
    fitParameters(i,2) = (abs(coeff(1)-coeff_error(1)))/2; %change 95% confidence interval into 1 sigma
    
    f = errorbar(ppmMatrix(:,i),co2, co2err,'o');
    hold on;
    fplot( @(x) coeff(1)*x + coeff(2) );
    plotname = strcat('/home/sam/Mu2e-Factory/Chamber_Volume/fits/ch',num2str(i-1),'_calibration.png');
    title(strcat('Chamber ',{' '},num2str(i-1),' Calibration'));
    ylabel('CO$_2$ Injected [mL]');
    xlabel('CO$_2$ detected [ppm]' );
    
    fiteqn = strcat('Volume = (', num2str(round(coeff(1)*10^6)),'\pm' ,num2str(round(fitParameters(i,2)*10^6)),') mL');
    %legend('data','Volume:','location','northwest');
    dim = [.2 .5 .3 .3];
    annotation('textbox',dim,'String',fiteqn,'FitBoxToText','on');
    saveas(f, plotname );
    hold off;
    close();  
end

csvwrite('ch0-ch9_chamber_volumes_datapoints.csv',ppmMatrix) 
csvwrite('ch0-ch9_chambervolumes.csv',round(10^6*fitParameters)); %file with volume and uncertainty in CC
