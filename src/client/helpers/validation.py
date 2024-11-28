import re


def validate_OID(oid):
    oid_pattern = r"^\d+(\.\d+)+$"
    return bool(re.match(oid_pattern, oid))


def validate_host_ip(host_ip: str):
    host_ip = host_ip.strip()
    host_ip_pattern = r"""
    ^                             # Start of string
    (25[0-5]                      # 25 followed by 0-5 (for values 250-255)
    | 2[0-4][0-9]                 # 2 followed by 0-4 and then any digit
                                  #(for 200-249)
    | [01]?[0-9][0-9]?)           # Single digit or two digits (for 0-199)
    \.                            # Literal dot
    (25[0-5]                      # Same pattern for the second octet
    | 2[0-4][0-9]
    | [01]?[0-9][0-9]?)
    \.                            # Literal dot
    (25[0-5]                      # Same pattern for the third octet
    | 2[0-4][0-9]
    | [01]?[0-9][0-9]?)
    \.                            # Literal dot
    (25[0-5]                      # Same pattern for the fourth octet
    | 2[0-4][0-9]
    | [01]?[0-9][0-9]?)
    $                            # End of string
    """
    return bool(re.match(host_ip_pattern, host_ip, re.VERBOSE))


def validate_port(port: str):
    # Regex to ensure the port is a number and between 0 and 65535
    if re.match(r"^\d{1,5}$", port):
        port_number = int(port)
        return 0 <= port_number <= 65535
    return False
