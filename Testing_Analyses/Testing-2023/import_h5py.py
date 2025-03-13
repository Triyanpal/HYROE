import h5py
import numpy as np
import os
import matplotlib.pyplot as plt

# Function to explore the HDF5 file structure
def explore_hdf5(obj, indent=0):
    spacing = ' ' * indent
    if isinstance(obj, h5py.Group):
        print(f'{spacing}Group: {obj.name}')
        for key, item in obj.items():
            explore_hdf5(item, indent + 4)
    elif isinstance(obj, h5py.Dataset):
        print(f'{spacing}Dataset: {obj.name}, Shape: {obj.shape}, Type: {obj.dtype}, Compression: {obj.compression}, Checksum: {obj.fletcher32}')

# Function to extract, filter, and save channel data to a text file
def extract_and_save_channel_data_to_text_and_plot(h5file, output_file_path):
    channels_group = h5file.get('/channels')
    if channels_group is None:
        print("The 'channels' group is not found in the HDF5 file.")
        return

    with open(output_file_path, 'w') as file:
        for channel_name, group in channels_group.items():
            if isinstance(group, h5py.Group):
                time_dataset = group.get('time')
                data_dataset = group.get('data')
                
                if time_dataset is not None and data_dataset is not None:
                    time_data = time_dataset[:]
                    sensor_data = data_dataset[:]

                    # Debugging: print dataset content and shapes
                    print(f'Channel: {channel_name}, Time Data Shape: {time_data.shape}, Sensor Data Shape: {sensor_data.shape}')

                    # Check if sensor_data is entirely NaN
                    if np.isnan(sensor_data).all():
                        print(f'Channel {channel_name} contains only NaN values, skipping.')
                        continue

                    # Filter out rows where data is NaN
                    valid_indices = ~np.isnan(sensor_data)
                    filtered_time_data = time_data[valid_indices]
                    filtered_sensor_data = sensor_data[valid_indices]

                    # Now, filter out leading zeros
                    non_zero_indices = np.nonzero(filtered_sensor_data)[0]
                    if len(non_zero_indices) == 0:
                        print(f'Channel {channel_name} contains only zero values after NaN removal, skipping.')
                        continue

                    # Start from the first non-zero value
                    first_non_zero_index = non_zero_indices[0]
                    filtered_time_data = filtered_time_data[first_non_zero_index:]
                    filtered_sensor_data = filtered_sensor_data[first_non_zero_index:]

                    # Write the filtered data to file
                    file.write(f'Channel: {channel_name}\n')
                    file.write('Time,Data\n')
                    for time, data in zip(filtered_time_data, filtered_sensor_data):
                        file.write(f'{time},{data}\n')
                    file.write('\n')  # Add a blank line between channels
                    print(f'Extracted and filtered data for channel {channel_name}, Time Shape: {filtered_time_data.shape}, Data Shape: {filtered_sensor_data.shape}')

                    # Plot the filtered data
                    plt.figure(figsize=(10, 6))
                    plt.plot(filtered_time_data, filtered_sensor_data, label=f'Channel: {channel_name}')
                    plt.xlabel('Time')
                    plt.ylabel('Data')
                    plt.title(f'Data vs Time for Channel: {channel_name}')
                    plt.legend()
                    plt.grid(True)
                    plot_filename = os.path.join(output_file_path + f'_{channel_name.replace(" ", "_")}.png')
                    plt.savefig(plot_filename)
                    plt.close()

                else:
                    print(f'Missing time or data dataset for channel {channel_name}')
            else:
                print(f'Channel {channel_name} is not a group.')
    print(f"Data has been saved to {output_file_path}")

# Main script
file_path = r'C:\Users\TriyanPal.Arora\OneDrive - Cranfield University\EASN\HRMTS testing\cranfield-firing.h5'
output_file_path = r'C:\Users\TriyanPal.Arora\OneDrive - Cranfield University\EASN\HRMTS testing\extracted_data3.txt'

try:
    h5file = h5py.File(file_path, 'r')

    # Explore the file structure
    print("Exploring file structure:")
    explore_hdf5(h5file)

    # Extract, filter, save channel data to a text file, and plot the data
    print("\nExtracting, filtering, saving channel data to text file, and plotting data:")
    extract_and_save_channel_data_to_text_and_plot(h5file, output_file_path)

    # Close the HDF5 file
    h5file.close()
except Exception as e:
    print(f"An error occurred: {e}")
