import json

def get_service_status(service_name):
    # Return True if the service is enabled, False if not.
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        service_status = config[service_name]['status']
    except:
        config = { 
                service_name: { "status": False,
                                "sync_period": 360
                               }
            }
        service_status = False

    return service_status, config

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
            
