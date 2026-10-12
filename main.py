import heapq

def parse_log_line(line: str):
    words = line.split()
    if len(words) != 5:
        return None

    timestamp, http_method, endpoint, status_code, latency = words

    try:
        status_code = int(status_code)
        latency = int(latency)
    except ValueError:
        return None
  
  
    if status_code > 599 or status_code < 100:
        return None

    if latency < 0:
        return None

    return {
        "timestamp": timestamp,
        "http_method": http_method,
        "endpoint": endpoint,
        "status_code": status_code,
        "latency": latency
    }
    
def get_top_k_endpoints(endpoint_errors: dict, k: int):
    heap = [(count, method, endpoint) for (method, endpoint), count in endpoint_errors.items()]
    return heapq.heapify(heap)

def analyze_logs(file_path: str):
    total_requests = 0
    successful_requests = 0
    redirect_requests = 0
    client_errors = 0
    server_errors = 0
    malformed_lines = 0
    total_latency = 0
    server_error_rate = 0.0
    average_latency = 0.0
    
    endpoint_errors = {}
    
  
    with open(file_path, 'r') as log_file:
      for line in log_file:
        parsed_line = parse_log_line(line.strip())
        if parsed_line is None:
            malformed_lines += 1
            continue
        
        total_requests += 1
        status_code = parsed_line["status_code"]
        if 200 <= status_code < 300:
            successful_requests += 1
        elif 300 <= status_code < 400:
            redirect_requests += 1
        elif 400 <= status_code < 500:
            client_errors += 1
        elif 500 <= status_code < 600:
            server_errors += 1
            path = (parsed_line["http_method"], parsed_line["endpoint"])
            endpoint_errors[path] = endpoint_errors.get(path, 0) + 1

        total_latency += parsed_line["latency"]
            
    if total_requests > 0:
        server_error_rate = (server_errors / total_requests) * 100
        average_latency = total_latency / total_requests
            
    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "redirect_requests": redirect_requests,
        "client_errors": client_errors,
        "server_errors": server_errors,
        "malformed_lines": malformed_lines,
        "server_errors_rate": server_error_rate,
        "average_latency": average_latency,
        "endpoint_errors": endpoint_errors
    }  