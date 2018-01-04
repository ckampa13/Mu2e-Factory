% Program to calculate the volume of leak test chambers
% created by Sam Penders (pende061@umn.edu)

%filename = '/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/row_1/ch0_0.1_0.8mL.txt';

ppmMatrix = zeros(9,15); %matrix to hold averaged ppm level datapoints
ppmError = zeros(9,15); %statistical error on averaged ppm datapoints %where the highest number chamber (4) switches from the first injected level to second
% times CO2 level changed from 0 to 0.1; 0.1 to 0.8; 0.2 to 0.7; 0.3 to 0.6; 0.4 to
% 0.5 on last chamber

for m = 3:5 %row 3-5 data folders
    for k = 1:5 %5 straws per row
        for n = 0:8 %data file for 0.0-0.8 mL for each straw
            
            %if n == 0
               % CO2 = '0.0';
           % else
                %C02 = strcat('0.',num2str(n));
                %disp(CO2);
            %end
            a = num2str(n);
            %disp(co2_in);
            CO2_in = strcat('0.',a);
            
            filename = strcat('/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/row_',num2str(m),'/','ch',num2str(k-1+5*(m-1)),'_',CO2_in,'mL.txt');
            d = readtable(filename);
            t = table2array(d(:,1)); %times, in epoch time
            ppm = table2array(d(:,3)); %temporary -- CO2 level in chamber in each time interval
            
            ppmMatrix(n+1,k+5*(m-3)) = mean(ppm);
            
            co2 = 0:0.1:0.8;
            error = [0.01 0.03*ones(1,4) 0.03*sqrt(2)*ones(1,4) ];
            
            errorbar(ppmMatrix(:,k+5*(m-3)),co2,error);
            
            
        end
    end
end

co2 = 0:0.1:0.8;
co2err =[ [0.01] 0.03*ones(1,4)  0.03*sqrt(2)*ones(1,4)] %estimated error in CO2 volume
fitParameters = zeros(15,2); %slope and its uncertainty

for i = 1:15 %fit data and make plots 
    datafit = fit(ppmMatrix(:,i), co2.', 'poly1','Weights',co2err.^-1)
    coeff = coeffvalues(datafit);
    coeff_error = confint(datafit);
    
    fitParameters(i,1) = coeff(1); %slope from fit -> multiply by 10^6 mL for volume in CC
    fitParameters(i,2) = (abs(coeff(1)-coeff_error(1)))/3; %change 95% confidence interval into 1 sigma
    
    f = errorbar(ppmMatrix(:,i),co2, co2err,'o');
    hold on;
    fplot( @(x) coeff(1)*x + coeff(2) );
    plotname = strcat('/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/fits/ch',num2str(i-1+10),'_calibration.png');
    title(strcat('Chamber ',{' '},num2str(i-1+10),' Calibration'));
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

csvwrite('ch10-ch24_chamber_volumes_datapoints.csv',ppmMatrix) 
csvwrite('ch10-ch24_chambervolumes.csv',round(10^6*fitParameters)); %file with volume and uncertainty in CC








