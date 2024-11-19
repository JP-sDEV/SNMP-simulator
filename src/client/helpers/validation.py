import re


def validate_OID(oid):
    oid_pattern = r"^\d+(\.\d+)+$"
    return bool(re.match(oid_pattern, oid))


def validate_host_ip(host_ip: str):
    host_ip = host_ip.strip()
    host_ip_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(host_ip_pattern, host_ip))


def validate_port(port: str):
    # Regex to ensure the port is a number and between 0 and 65535
    if re.match(r"^\d{1,5}$", port):
        port_number = int(port)
        return 0 <= port_number <= 65535
    return False
