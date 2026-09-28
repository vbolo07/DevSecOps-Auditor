def check_firewall(executor, config):
    res = executor.run(["sudo", "ufw", "status"])
        
    fw_status=res.stdout.split()[1]
    expected=config['linux']['firewall']['enabled']
    #print(fw_status)
    if fw_status=="active":
        return {
                "name": "firewall",
                "status": "PASS",
                "message": "Firewall is enabled"
            }
    elif fw_status=="inactive":
        return {
                "name": "firewall",
                "status": "FAIL",
                "message": "Firewall is disabled"
            }
    
