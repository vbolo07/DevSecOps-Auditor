def check_ports(executor, config):
    res = executor.run(["sudo", "ss", "-tulpn"])

    allowed_ports = set(config["linux"]["network"]["allowed_ports"])
    actual_ports = set()

    for line in res.stdout.splitlines():
        parts = line.split()
        
        if len(parts) < 5:
            continue
        if parts[0] not in ("tcp", "tcp6") or parts[1] != "LISTEN":
            continue
        local_address = parts[4]

        # IPv6: [::]:443
        if "]:" in local_address:
            port = local_address.rsplit(":", 1)[1]

        # IPv4: 0.0.0.0:22
        elif ":" in local_address:
            port = local_address.rsplit(":", 1)[1]

        else:
            continue

        if port.isdigit():
            actual_ports.add(int(port))

    unexpected_ports = actual_ports - allowed_ports

    if unexpected_ports:
        return {
                    "name": "allowed_ports",
                    "status": "FAIL",
                    "message": f"There are some unexpected open ports listening: {sorted(unexpected_ports)}"                 
                }
    return {
                "name": "allowed_ports",
                "status": "PASS",
                "message": f"There are NO unexpected open ports listening: {sorted(unexpected_ports)}"                 
            } 

