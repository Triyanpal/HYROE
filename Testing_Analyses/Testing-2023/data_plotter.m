% MATLAB Script to process a two-column text file, calculate thrust, and plot data

% Step 1: Read the data from the text file
filename = 'Cranfield PT_1 data.txt';
data = readmatrix(filename); % Read the data from the file

% Step 2: Extract the columns
timestamps = data(:, 1); % First column - Timestamps
pressure = data(:, 2); % Second column - Pressure readings in bars

% Step 3: Convert pressure from bars to Pascals
pressure_pa = pressure * 1e5; % 1 bar = 10^5 Pa

% Step 4: Filter data between timestamps 9040 and 9090
start_time = 9058; % Start timestamp
end_time = 9076; % End timestamp

% Logical indexing to filter data within the specified range
time_filter = (timestamps >= start_time) & (timestamps <= end_time);
filtered_timestamps = timestamps(time_filter);
filtered_pressure_pa = pressure_pa(time_filter);

% Step 5: Thrust calculation
% Given system parameters
exit_diameter = 22.31e-3; % Exit diameter in meters (22.31 mm)
exit_area = pi * (exit_diameter / 2)^2; % Exit area in square meters

% Ambient pressure
P_ambient = 1.01325e5; % Ambient pressure in Pascals

% Calculate thrust at each timestamp
thrust = (filtered_pressure_pa - P_ambient) .* (exit_area*298.4/1100.05); % Thrust in Newtons

% Step 6: Plot the filtered pressure and thrust data

figure;
% Plot Pressure vs Time
plot(filtered_pressure_pa / 1e5, 'LineWidth', 2); % Convert pressure back to bar for display
%xlabel('Timestamp from T0 (seconds)', 'FontSize', 30); % Increased font size
ylabel('Pressure (bar)', 'FontSize', 20); % Increased font size
title('Pressure distribution', 'FontSize', 20);
grid on;
set(gca,  'XTickLabel', []); % Remove x-axis tick labels

% Plot Thrust vs Time
figure
plot(thrust, 'LineWidth', 2);
%xlabel('Timestamp from T0 (seconds)', 'FontSize', 30); % Increased font size
ylabel('Thrust (N)', 'FontSize', 20); % Increased font size
title('Thrust distribution', 'FontSize', 20);
grid on;

% Step 7: Customize the plot (optional)
set(gca,  'XTickLabel', []); % Remove x-axis tick labels

