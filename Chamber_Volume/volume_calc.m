% Program to calculate the volume of leak test chambers
% created by Sam Penders (pende061@umn.edu)

%filename = '/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/row_1/ch0_0.1_0.8mL.txt';

%chamber rows to be analyzed

min_row = 6;
max_row = 10;

total_chmb = (max_row-min_row)*5; %total number of chambers

ppmMatrix = zeros(8,total_chmb); %matrix to hold averaged ppm level datapoints
ppmError = zeros(8,total_chmb); %statistical error on averaged ppm datapoints

for m = min_row:max_row 
    for k = 1:5 %5 straws per row
        transitions = zeros(4,1); %vector of index where co2 gets injected
        ppm_initial = zeros(8,1);
        for n = 1:8 %data file for 0.0-0.8 mL for each straw
         
            a = num2str(n);
            CO2_in = strcat('0.',a); %file for amount of CO2 injected
            filename = strcat('/home/sam/Mu2e-Factory/Chamber_Volume/row_',num2str(m),'/','ch',num2str(k-1+5*(m-1)),'_',CO2_in,'mL.txt');
            
            % if data files exist, analyze it
            if exist(filename,'file')
                d = readtable(filename); %read in all data from .txt file
                t = table2array(d(:,1)); %times, in epoch time
                ppm = table2array(d(:,3)); %temporary -- CO2 level in chamber
                ppm(:);
                
                % get initial co2 level of flushed chamber and 0.1-0.4 mL
                % data
                if(n < 5)
                   for i = 1:length(ppm)
                       if ppm(i+1) >= ppm(i)+70
                           transitions(n) = i; %point where co2 gets injected
                           %disp(transitions(n))
                           %disp(filename);
                           ppm_initial(n) = mean(ppm(1:transitions(n)-3));
                           ppm_initial(9-n) = ppm_initial(n);
                           ppmMatrix(n,(m-min_row)*5+k) = mean( ppm(transitions(n)+9:length(ppm)))-ppm_initial(n);
                           break;
                       end
                   end

                else
                    ppmMatrix(n,(m-min_row)*5+k) = mean(ppm)-ppm_initial(n)
                end

                co2 = 0.1:0.1:0.8;
                error = [0.03*ones(1,4) 0.03*sqrt(2)*ones(1,4) ]; 
                %errorbar(ppmMatrix(:,k+5*(m-7)),co2,error,'o');
            
            end
        end
    end
end

co2err = [ 0.03*ones(1,4)  0.03*sqrt(2)*ones(1,4)]; %estimated error in CO2 volume
fitParameters = zeros(total_chmb,2); %slope and its uncertainty
min_chmb = (min_row-1)*5;
max_chmb = max_row*5-1

for i = min_chmb:max_chmb %fit data and make plots 
    datafit = fit(ppmMatrix(:,i-min_chmb+1), co2.', 'poly1','Weights',co2err.^-1);
    coeff = coeffvalues(datafit);
    coeff_error = confint(datafit);
    
    fitParameters(i,1) = coeff(1); %slope from fit -> multiply by 10^6 mL for volume in CC
    fitParameters(i,2) = (abs(coeff(1)-coeff_error(1)))/2; %change 95% confidence interval into 1 sigma
    
    f = errorbar(ppmMatrix(:,i-min_chmb+1),co2, co2err,'o');
    hold on;
    fplot( @(x) coeff(1)*x + coeff(2) );
    plotname = strcat('/home/sam/Mu2e-Factory/Chamber_Volume/fits/ch',num2str(i-1+10),'_calibration.png');
    title(strcat('Chamber ',{' '},num2str(i),' Calibration'));
    ylabel('CO$_2$ Injected [mL]');
    xlabel('Change in CO$_2$ level [ppm]' );
    
    fiteqn = strcat('Volume = (', num2str(round(coeff(1)*10^6)),'\pm' ,num2str(round(fitParameters(i,2)*10^6)),') mL');
    %legend('data','Volume:','location','northwest');
    dim = [.2 .5 .3 .3];
    annotation('textbox',dim,'String',fiteqn,'FitBoxToText','on');
    saveas(f, plotname );
    hold off;
    close();  
end

volume_file = strcat('ch',num2str(min_chmb),'-ch',num2str(max_chmb),'_chambervolumes.csv');
datapoints_file = strcat('ch',num2str(min_chmb),'-ch',num2str(max_chmb),'_chamber_volumes_datapoints.csv')

csvwrite(datapoints_file,ppmMatrix) 
csvwrite(volume_file,round(10^6*fitParameters)); %file with volume and uncertainty in CC








