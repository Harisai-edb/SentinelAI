import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import time,sys
from colorama import Fore, Back, Style

# Function to type text with a blinking cursor
def type(text, cursor_speed=0.05, cursor_char=' '):
    for char in text:
        sys.stdout.write(char )
        sys.stdout.flush()
        time.sleep(cursor_speed)
        # sys.stdout.write('\b \b')  # Move the cursor back and erase the cursor
        sys.stdout.flush()
        time.sleep(cursor_speed)

def create_dataset1():
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
    for _ in range(24 * 60):
        data['time'].append(time.strftime('%H:%M'))

        # Calculate the current time within the 2-hour cycle
        cycle_time = (time.hour * 3600 + time.minute * 60 + time.second) % (2 * 60 * 60)

        if cycle_time < 60 * 60:
            # Disk usage increases by 0.005 MB per minute for the first hour of the cycle
            current_disk_usage += 0.05
        elif cycle_time >= 60 * 60 and cycle_time < 2 * 60 * 60:
            # Disk usage decreases by 0.005 MB per minute for the second hour of the cycle
            current_disk_usage -= 0.05
        current_disk_usage += 0.05
        data['disk_usage_MB'].append(current_disk_usage)
        time += timedelta(minutes=1)

    # Create the DataFrame
    df = pd.DataFrame(data)
    # Calculate the percentage of disk usage used
    total_available_disk = 600  # MB
    df['disk_usage_percentage'] = (df['disk_usage_MB'] / total_available_disk) * 100
    return df

def create_dataset2():
    data = {
        'time': [],
        'disk_usage_MB': []
    }
    
    # Initialize values
    initial_disk_usage = 500
    current_disk_usage = initial_disk_usage
    time = datetime(2023, 1, 1, 0, 0)  # Starting at midnight

    # Generate data for a day (24 hours)
    for _ in range(24 * 60):
        data['time'].append(time.strftime('%H:%M'))

        if time.time() < datetime(2023, 1, 1, 10, 0).time():
            current_disk_usage += 0.005  # Disk usage increases by 0.005 MB per minute
        elif datetime(2023, 1, 1, 10, 0).time() <= time.time() < datetime(2023, 1, 1, 10, 30).time():
            current_disk_usage += 2  # Disk usage increases by 2 MB per minute from 10:00 to 10:30 AM
        elif datetime(2023, 1, 1, 10, 30).time() <= time.time() < datetime(2023, 1, 1, 11, 0).time():
            current_disk_usage -= 2  # Disk usage decreases by 2 MB per minute from 10:30 to 11:00 AM
        elif datetime(2023, 1, 1, 11, 0).time() <= time.time() < datetime(2023, 1, 1, 17, 0).time():
            current_disk_usage += 0.005  # Disk usage increases by 0.005 MB per minute from 11:00 to 17:00
        else:
            current_disk_usage = current_disk_usage  # Disk usage remains constant after 17:00

        data['disk_usage_MB'].append(current_disk_usage)
        time += timedelta(minutes=1)

    df = pd.DataFrame(data)
    total_available_disk = 600  # MB
    df['disk_usage_percentage'] = (df['disk_usage_MB'] / total_available_disk) * 100
    return df


# Function to monitor disk usage
def monitor_disk_usage(dataframe, threshold):
    total_available_disk = 600  # MB
    for i in range(len(dataframe)):
        if dataframe['disk_usage_percentage'][i] >= threshold:
            end_index = i
            start_index = max(0, end_index - 6 * 60)
            
            start_disk_usage = dataframe['disk_usage_MB'][start_index]
            end_disk_usage = dataframe['disk_usage_MB'][end_index]
            rate_of_increase = (end_disk_usage - start_disk_usage) / 360.0  # 6 hours in minutes
            
            output_text = f"Event details: \033[1;31m High severity event, "
            output_text += f"\033[0m  Disk usage at {threshold}%, {round(end_disk_usage, 2)} MB of {total_available_disk} MB Used,"
            remaining_capacity = total_available_disk - end_disk_usage
            output_text += f" Remaining Capacity: {round(remaining_capacity, 2)} MB\n"
            type(output_text)
            time.sleep(3)
            output_text=""
            output_text += "Calculating disk usage increase rate in last 6 hours . . . . . . . \n"
            type(output_text)
            time.sleep(5)

            # Create and display the graph
            plt.figure(figsize=(8, 4))
            plt.plot(dataframe['time'][start_index:end_index + 1], dataframe['disk_usage_percentage'][start_index:end_index + 1], label='Disk Usage Percentage', color='blue')
            plt.xlabel('Time (HH:MM)')
            plt.ylabel('Disk Usage Percentage (%)')
            plt.title(f'Disk Usage Percentage Over Last 6 Hours (Rate of Increase: {rate_of_increase:.2f} MB/min)')
            plt.ylim(0, 100)
            plt.axhline(threshold, color='red', linestyle='--', label='Threshold')
            plt.legend()
            plt.tight_layout()
            # Set x-axis labels at 60-minute intervals
            hourly_labels = [time for time in dataframe['time'] if time.endswith('00')]
            plt.xticks(hourly_labels, rotation=0)
            plt.show()

            output_text = f"   Average increase rate: {rate_of_increase:.2f} MB/min\n"
            time_to_full_capacity = remaining_capacity / rate_of_increase
            output_text += f"   Time to reach 100%: {pd.to_timedelta(np.round(time_to_full_capacity, 0), unit='m')} if the current rate sustains\n"
            type(output_text)
            
            if time_to_full_capacity > 1000:
                output_text = f"This is not a real high severity event, as the disk is not going to fill up any time soon.\nSuggestion: Adjust thresholds to avoid furter false positive alerts.\n"
            else :
                output_text = f"You should treat this Event as critical, and notify customer immediately. \nSuggestion: Troubleshoot database, identify root cause for disk increase. Look at wal size, db size, log size\n"
            type(output_text)
            time.sleep(30)
            break


def main():
    # Ask for the event ID
    welcome_txt = "Sentinel Assistant - Please provide an event ID for analysis: "
    type(welcome_txt,cursor_speed=0.01)

    event_id = int(input(""))
    if event_id == 10051:
        df = create_dataset1()

    elif event_id == 10052:
        df = create_dataset2()
    
    else : 
        print(f"The event was not found") 
        quit()

    monitor_threshold = 90
    monitor_disk_usage(df, monitor_threshold)

if __name__ == "__main__":
    main()
