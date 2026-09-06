import socket
from concurrent.futures import ThreadPoolExecutor

# Define target host and port range
TARGET = "127.0.0.1"  # Replace with the IP address or hostname you want to scan
PORT_START = 1
PORT_END = 1024       # Common well-known ports
THREADS = 100         # Number of concurrent threads for speed

def scan_port(host, port):
    """
    Attempts to connect to a specific port on the target host.
    Returns the port number if open, otherwise None.
    """
    # Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Set a short timeout so the script doesn't hang on closed ports
        sock.settimeout(1.0)
        
        # connect_ex returns 0 if the connection was successful
        result = sock.connect_ex((host, port))
        if result == 0:
            return port
    return None

def main():
    print(f"Scanning target: {TARGET}")
    print(f"Scanning ports from {PORT_START} to {PORT_END}...")
    
    open_ports = []
    
    # Use ThreadPoolExecutor to run scans concurrently
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        # Map the scan function across our range of ports
        ports_to_scan = range(PORT_START, PORT_END + 1)
        results = executor.map(lambda p: scan_port(TARGET, p), ports_to_scan)
        
        # Filter and collect open ports
        for port in results:
            if port is not None:
                open_ports.append(port)
                print(f"[+] Port {port} is OPEN")

    print("\n--- Scan Complete ---")
    if open_ports:
        print(f"Open ports found: {sorted(open_ports)}")
    else:
        print("No open ports found in the specified range.")

if __name__ == "__main__":
    main()