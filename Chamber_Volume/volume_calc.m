% Program to calculate the volume of leak test chambers
% created by Sam Penders (pende061@umn.edu)

% for instructions on measuring the chamber volumes, see the document
% in the "Instruction documents" folder on the Mu2e-Factory GitHub.
% Following that procedure, this program may be used to easily calculate
% the volume for any rows.

% chamber rows to be analyzed
% change this to whatever chambers need to be done
% save location must be changed though
min_row = 6;
max_row = 10;

total_chmb = (max_row-min_row)*5; %total number of chambers

ppmMatrix = zeros(8,total_chmb); %matrix to hold averaged ppm level change datapoints
ppmError = zeros(8,total_chmb); %statistical error on averaged ppm datapoints

for m = min_row:max_row 
    for k = 1:5 %5 straws per row
        transitions = zeros(4,1); %vector of index where co2 gets injected
        ppm_initial = zeros(8,1); % initial co2 level in each chamber
        for n = 1:8 %data file for 0.0-0.8 mL for each straw
         
            a = num2str(n);
            CO2_in = strcat('0.',a); %file for amount of CO2 injected
            
            % looking for a file name like this:
            %filename = '/home/sam/Mu2e-Factory/leak_chmb_0-24_calibration/row_1/ch0_0.1_0.8mL.txt';
            filename = strcat('/home/sam/Mu2e-Factory/Chamber_Volume/row_',num2str(m),'/','ch',num2str(k-1+5*(m-1)),'_',CO2_in,'mL.txt');
            
            % if data files exist, analyze it
            if exist(filename,'file')
                d = readtable(filename); %read in all data from .txt file
                t = table2array(d(:,1)); %times, in epoch time
                ppm_raw = table2array(d(:,3)); %temporary -- CO2 level in chamber
                
%get rid of ppm = -1.00 data points that signify co2 sensor not getting power
                ppm = [];
                for i = 1:length(ppm_raw)
                    if ppm_raw(i) > 10
                        ppm = [ppm; ppm_raw(i)];
                    end
                end
                  
                transitions(n) = 0; % vector for holding index of injection in ppm
                
%get initial co2 level, and level after injection, 0.1-0.4 mL injections
                if(n < 5)
                       injection = false;
                       i = 1;
                       while injection == false && i < length(ppm)-3 %true before transition happens
                            if ppm(i+3) >= ppm(i)+100 
                                transitions(n) = i; %point where co2 gets injected
                                ppm_initial(n) = mean(ppm(1:transitions(n)));
                                ppm_initial(9-n) = ppm_initial(n);
                                ppmMatrix(n,(m-min_row)*5+k) = mean( ppm(transitions(n)+9:length(ppm)))-ppm_initial(n);
                                injection = true;
                            end
                            i = i+1;                             
                       end

% get avg co2 level for 0.5-0.8 mL injection
                else
                    ppmMatrix(n,(m-min_row)*5+k) = mean(ppm)-ppm_initial(n);
                end            
            end
        end
    end
end

co2 = 0.1:0.1:0.8; % amounts of co2 injected
co2err = [ 0.03*ones(1,4)  0.03*sqrt(2)*ones(1,4)]; %estimated error in CO2 injections
fitParameters = zeros(total_chmb,2); %slope and its uncertainty
min_chmb = (min_row-1)*5; % lowest chamber used
max_chmb = max_row*5-1;

%fit data and make plots 
for i = min_chmb:max_chmb 
    x = ppmMatrix(:,i-min_chmb+1);
    
    % fit data to line through origin
    datafit = fit(x(~isnan(x)), co2.', 'x.*a','Weights',co2err.^-2);
    coeff = coeffvalues(datafit);
    coeff_error = confint(datafit);
    
    fitParameters(i,1) = coeff(1); %slope from fit -> multiply by 10^6 mL for volume in CC
    fitParameters(i,2) = (abs(coeff(1)-coeff_error(1)))/2; %change 95% confidence interval into 1 sigma
    
    f = errorbar(x,co2, co2err,'o');S
    hold on;
    fplot( @(x) coeff(1)*x );
    plotname = strcat('/home/sam/Mu2e-Factory/Chamber_Volume/fits/ch',num2str(i),'_calibration.png');
    title(strcat('Chamber ',{' '},num2str(i),' Calibration'));
    ylabel('CO$_2$ Injected [mL]');
    xlabel('Change in CO$_2$ level [ppm]' );
    xlim([0 x(8)+100]);
    
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

csvwrite(datapoints_file,ppmMatrix) ;
csvwrite(volume_file,round(10^6*fitParameters)); %file with volume and uncertainty in CC








