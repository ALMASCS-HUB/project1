import configparser

# Create the ConfigParser object
config = configparser.ConfigParser()

# Read the client.cfg file
config.read('Client.cfg')

# Access values from the DEFAULT section
connection_type = config['DEFAULT']['ConnectionType']
socket_host = config['DEFAULT']['SocketConnectHost']
socket_port = config['DEFAULT']['SocketConnectPort']
begin_string = config['DEFAULT']['BeginString']
file_store_path = config['DEFAULT']['FileStorePath']
file_log_path = config['DEFAULT']['FileLogPath']

# Access values from the SESSION section
sender_comp_id = config['SESSION']['SenderCompID']
target_comp_id = config['SESSION']['TargetCompID']

# Print the values
print(f"ConnectionType: {connection_type}")
print(f"SocketConnectHost: {socket_host}")
print(f"SocketConnectPort: {socket_port}")
print(f"BeginString: {begin_string}")
print(f"FileStorePath: {file_store_path}")
print(f"FileLogPath: {file_log_path}")
print(f"SenderCompID: {sender_comp_id}")
print(f"TargetCompID: {target_comp_id}")
