import datetime

def parse_log_file_to_array(file):
    log_data = []

    for line in file:
        # Split the line by ":INFO:"
        parts = line.strip().split(":INFO:")
        if len(parts) == 2:
            timestamp_str = parts[0].strip()
            info_str = parts[1].strip()
            
            timestamp = timestamp_str.split(',')[0]
            
            # Store the timestamp and other information in a tuple
            log_data.append((timestamp, info_str))
    
    return log_data
            
