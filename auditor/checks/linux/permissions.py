import subprocess

def check_file_permissions(executor, config):
    res = executor.run(["sudo", "find", "/etc","-type", "f","-perm", "-002"])
    temp=res.stdout.split()
    
    expected= config['linux']['permissions']['world_writable_files']
    if len(temp)==0 and expected==False:
        return {
                    "name": "world_writable_files",
                    "status": "PASS",
                    "message": "No vulnerable writable files"
                }
    
    return {
                "name": "world_writable_files",
                "status": "FAIL",
                "message": "There are vulnerable writable files"
            }


def check_nopasswd(executor,config):

    res = executor.run(
            [
                "sudo",
                "grep",
                "-R",
                "NOPASSWD",
                "/etc/sudoers",
                "/etc/sudoers.d",
            ],
            check=False
        )
    #print(res.stdout)
    if res.returncode not in (0, 1):
        res.check_returncode()
    allow_nopasswd = (
        config
        .get("linux", {})
        .get("sudo", {})
        .get("allow_nopasswd", False)
    )

    rules = res.stdout.splitlines()

    if not rules:
        return {
                "name": "allow_nopasswd",
                "status": "PASS",
                "message": "NO NOPASSWD rules detected"
            }

    if allow_nopasswd:
        return {
                "name": "allow_nopasswd",
                "status": "PASS",
                "message": "NOPASSWD rules detected and allowed by policy"
            }

    return {
            "name": "allow_nopasswd",
            "status": "FAIL",
            "message": f"NOPASSWD rules detected, check them:{rules}"
        }


