def check_users(executor, config):
    res = executor.run(["sudo", "awk", "-F:", "$3 == 0 {print $1}","/etc/passwd"])
    expected_user = config['linux']['users']['allowed_uid_zero']
    
    if res.stdout.strip() == expected_user[0]:
        return {
                "name": "allowed_uid_zero",
                "status": "PASS",
                "message": "Root has UID 0, All good!"
            }
    return {
            "name": "allowed_uid_zero",
            "status": "FAIL",
            "message": "Unexpected user has UID 0, BAD!"
        }
  
