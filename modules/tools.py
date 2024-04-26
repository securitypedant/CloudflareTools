import json

def save_config(config):
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
    except:
        raise

def get_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        raise        

    return config

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
            
