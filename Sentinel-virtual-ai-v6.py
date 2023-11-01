import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import time
import sys

def type(text, cursor_speed=0.05, cursor_char='_'):
    for char in text:
        sys.stdout.write(char + cursor_char)  # Print the character and the cursor
        sys.stdout.flush()
        time.sleep(cursor_speed)  # Control the typing speed
        sys.stdout.write('\b \b')  # Move the cursor back
        sys.stdout.flush()
        time.sleep(cursor_speed)  # Control the blinking speed

    # sys.stdout.write("\n")  # Add a newline character at the end

def create_dataset():
    # Initialize the DataFrame
    data = {
        'time': [],
        'disk_usage_MB': []
    }

    # Initial values
    initial_disk_usage = 500
    current_disk_usage = initial_disk_usage
    time = datetime(2023, 1, 1, 0, 0)  # Starting at midnight

    # Generate data for a day (24 hours)
    for _ in range(48 * 60):
        data['time'].append(time.strftime('%d:%m:%H:%M'))
        
        if time.time() < datetime(2023, 1, 1, 10, 0).time():
            # Disk usage increases by .005 MB per minute
            current_disk_usage += 0.005
        elif time.time() >= datetime(2023, 1, 1, 10, 0).time() and time.time() < datetime(2023, 1, 1, 10, 30).time():
            # Disk usage increases by 2 MB per minute from 10:00 to 10:30 AM
            current_disk_usage += 2
        elif time.time() >= datetime(2023, 1, 1, 10, 30).time() and time.time() < datetime(2023, 1, 1, 11, 0).time():
            # Disk usage decreases by 2 MB per minute from 10:30 to 11:00 AM
            current_disk_usage -= 2
        elif time.time() >= datetime(2023, 1, 1, 11, 0).time() and time.time() < datetime(2023, 1, 1, 17, 0).time():
            # Disk usage increases by .005 MB per minute from 11:00 to 17:00
            current_disk_usage += 0.005
        else:
            # Disk usage remains constant after 17:00
            current_disk_usage = current_disk_usage
        
        data['disk_usage_MB'].append(current_disk_usage)
        
        time += timedelta(minutes=1)

    # Create the DataFrame
    df = pd.DataFrame(data)
    return df

# Print the first few rows of the generated dataset
# print(df.head())

def add_percentages(df):
    total_available_disk = 600  # MB
    df['disk_usage_percentage'] = (df['disk_usage_MB'] / total_available_disk) * 100

    # High threshold is at 90% disk usage 
    high_threshold = total_available_disk * 0.9

    # Create a plot for the percentage of disk usage used
    plt.figure(figsize=(15, 6))
    plt.plot(df['time'], df['disk_usage_MB'], label='Disk Usage', color='blue')

    # Set labels and title
    plt.xlabel('Time (DD:MM:HH:MM)')
    plt.ylabel('Disk Usage  (%)')
    plt.title('Disk Usage  Over Time')
    # plt.ylim(0, 100)  # Set the y-axis limits to 0-100%

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add a horizontal line at 100% (full disk)
    plt.axhline(high_threshold, color='red', linestyle='--', label='90%')

    # Display the legend
    plt.legend()

    # Set x-axis labels at hourly intervals
    hourly_labels = [time for time in df['time'] if time.endswith('00')]
    plt.xticks(hourly_labels, rotation=45)

    # Show the plot
    plt.tight_layout()
    plt.show()
    return df





# Define a function to detect anomalies in disk usage data
def detect_anomalies(df, threshold=0.95):
    # Calculate the rate of disk usage change per minute
    df['usage_rate'] = df['disk_usage_MB'].diff().fillna(0)

    # Fit an Isolation Forest model to the usage rate data
    model = IsolationForest(contamination=1 - threshold, random_state=42)
    df['anomaly'] = model.fit_predict(df['usage_rate'].values.reshape(-1, 1))

    return df



# Monitoring function
def monitor_disk_usage(dataframe, anomalies,threshold=90):
    total_available_disk = 600  # MB
    for i in range(len(dataframe)):
        if dataframe['disk_usage_percentage'][i] >= threshold:
            # Check if the time is within the anomalies time range (HH:MM format)
            

            # Display the last 6 hours graph
            end_index = i
            start_index = max(0, end_index - 6 * 60)
            
            # Calculate the rate of increase for the last 6 hours
            start_disk_usage = dataframe['disk_usage_MB'][start_index]
            end_disk_usage = dataframe['disk_usage_MB'][end_index]
            rate_of_increase = (end_disk_usage - start_disk_usage) / 360.0  # 6 hours in minutes
            
            # Create and display the graph
            plt.figure(figsize=(12, 6))
            plt.plot(dataframe['time'][start_index:end_index + 1], dataframe['disk_usage_percentage'][start_index:end_index + 1], label='Disk Usage Percentage', color='blue')
            plt.xlabel('Time (DD:MM:HH:MM)')
            plt.ylabel('Disk Usage Percentage (%)')
            plt.title(f'Disk Usage Percentage Over Last 6 Hours (Rate of Increase: {rate_of_increase:.2f} MB/min)')
            plt.ylim(0, 100)
            plt.xticks(rotation=45)
            plt.axhline(100, color='red', linestyle='--', label='Disk Full')
            plt.legend()
            plt.tight_layout()
            # Set x-axis labels at hourly intervals
            hourly_labels = [time for time in df['time'] if time.endswith('00')]
            plt.xticks(hourly_labels, rotation=45)
            plt.show()

            # Predict when the disk will reach 100% at the current rate
            output_text = ""
            output_text += f"The event details are as follows: \n"
            output_text += f"The disk usage at {threshold} % {round(end_disk_usage,2)} MB of {total_available_disk}MB Used\n"
            # print(f"The disk usage at",threshold,"%",round(end_disk_usage,2),"MB of",total_available_disk,"MB Used")
            remaining_capacity = total_available_disk - end_disk_usage
            # print(f"Remaining Capacity of disk is ",round(remaining_capacity,2),"MB")
            output_text += f"Remaining Capacity of disk is {round(remaining_capacity,2)}MB\n"
            # print(f"Sentinel Virtual Assistant is analyzing disk usage for last 6 hours\n    Rate of increase for the last 6 hours: {rate_of_increase:.2f} MB/min")
            # Simulate typing
            type(output_text)

            output_text = ""
            output_text += f"Sentinel Virtual Assistant is analyzing disk usage for last 6 hours . . . . . . . \n"
            type(output_text)
            time.sleep(5)
            output_text = ""
            output_text += f"   Rate of increase for the last 6 hours: {rate_of_increase:.2f} MB/min\n"
            time_to_full_capacity = remaining_capacity / rate_of_increase # in mins
            # print(f"    Time to reach to 100% is ",round(time_to_full_capacity,2),"mins", "which is",pd.to_timedelta(np.round(time_to_full_capacity, 0), unit='m'),"if current rate sustains\n")
            output_text += f"    Time to reach to 100% is {round(time_to_full_capacity,2)}mins, which is {pd.to_timedelta(np.round(time_to_full_capacity, 0), unit='m')} if current rate sustains\n"
            # print(pd.to_timedelta(np.round(time_to_full_capacity, 0), unit='m')) # working 0 days 08:55:00

            # Simulate typing
            type(output_text)

            timedelta_to_add = pd.Timedelta(pd.to_timedelta(np.round(time_to_full_capacity, 0), unit='m'))
            time_datetime = pd.to_datetime(dataframe['time'][end_index], format='%d:%m:%H:%M')
            # Add the Timedelta to the time
            resulting_datetime = time_datetime + timedelta_to_add

            # Convert the resulting datetime back to the 'DD:MM:HH:MM' format
            resulting_time_str = resulting_datetime.strftime('%d:%m:%H:%M')
            

            # print(f"Disk usage reached {threshold}% at {dataframe['time'][i]} (DD:MM:HH:MM)")
            
            # print(f"Disk will reach 100% at: {resulting_time_str}")
            
            current_time = dataframe['time'][i][-5:]
            anomalies_times = set(anomalies['time'].str[-5:])
            if current_time in anomalies_times:
                # Disk usage is part of the daily pattern, no need to raise an alert
                # print(f"Disk usage reached {threshold}% at {dataframe['time'][i]} (DD:MM:HH:MM)")
                output_text = ""
                output_text += "Sentinel Virtual Assistant is checking the old trend and possible regression patterns . . . . . . . .\n"
                type(output_text)
                time.sleep(5)
                output_text = ""
                output_text += f"    Sentinel Virtual Assistant found that current disk usage is part of the daily pattern. No alert raised.\n"
                wait_til = anomalies['time'].iloc[-1]
                output_text += f"    Sentinel Virtual Assistant suggest ack the alert  till {wait_til[-5:]}\n"
                # print("Sentinel Virtual Assistant is checking the old trend and possible regression patterns")
                # print(f"    Sentinel Virtual Assistant found that current disk usage is part of the daily pattern. No alert raised.")
                
                # print(f"    Sentinel Virtual Assistant suggest ack the alert  till {wait_til[-5:]}")
                # break
                type(output_text)
            break


welcome_txt = "Hello, I am the Sentinel Virtual Assistant. I can help you with Sentinel event analysis\nPlease provide the event ID: "
type(welcome_txt,cursor_speed=0.01)
event_id = input("")
# Create a dataset 
df = create_dataset()

df = add_percentages(df)

# Set a threshold for anomaly detection
anomaly_threshold = 0.90

# Detect anomalies in the disk usage data
df = detect_anomalies(df, threshold=anomaly_threshold)

# Filter anomalies and alerts
anomalies = df[df['anomaly'] == -1]

# Display the anomalies
# print("Anomalies:")
# print(anomalies)

# Define the threshold for monitoring (e.g., 90%)
monitor_threshold = 90

# Monitor disk usage
monitor_disk_usage(df, anomalies, monitor_threshold)

