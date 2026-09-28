
def check_password_authentication(config, sshd_config):
    
    passwordauthentication = sshd_config.get("passwordauthentication")
    
    # compare with expected value
    expected = config['linux']['ssh']['password_authentication']
    actual=False
    if passwordauthentication=="no":
        actual = False
    elif passwordauthentication=="yes":
        actual = True
    
    status="PASS"
    if expected!=actual and actual==True:
        status="FAIL"
        return {
                    "name": "ssh_password_authentication",
                    "status": status,
                    "message": "Password authentication is enabled"
                }
    else:
        return {
            "name": "ssh_password_authentication",
            "status": status,
            "message": "Password authentication is disabled"
        }
        


def check_root_login(config, sshd_config):
    
    permitrootlogin = sshd_config.get("permitrootlogin")
    
    expected = config['linux']['ssh']['permit_root_login']
    actual=False
    if permitrootlogin=="no":
        actual=False
    elif permitrootlogin=="yes" or permitrootlogin=="without-password":
        actual=True

    status="PASS"
    if expected!=actual and actual==True:
        status="FAIL"
        mess="Root login is enabled with password"
        if permitrootlogin=="without-password":
            mess="Root login is enabled with ssh-key"
        return {
                    "name": "permit_root_login",
                    "status": status,
                    "message": mess
                }
    else:
        return {
            "name": "permit_root_login",
            "status": status,
            "message": "Root login is disabled"
        }

def check_empty_passwords(config, sshd_config):

    permit_empty_pwd = sshd_config.get("permitemptypasswords")
    
    expected = config['linux']['ssh']['permit_empty_passwords']
    actual=False
    if permit_empty_pwd=="no":
        actual=False
    elif permit_empty_pwd=="yes":
        actual=True

    status="PASS"
    if expected!=actual and actual==True:
        status="FAIL"
        mess="Empty passwords are enabled"
        return {
                    "name": "permit_empty_passwords",
                    "status": status,
                    "message": mess
                }
    else:
        return {
            "name": "permit_empty_passwords",
            "status": status,
            "message": "Empty passwords are disabled"
        }

def check_x11forwarding(config, sshd_config):

    x11_forwarding=sshd_config.get("x11forwarding")
    
    expected = config['linux']['ssh']['x11_forwarding']
    actual=False
    if x11_forwarding=="no":
        actual=False
    elif x11_forwarding=="yes":
        actual=True

    if expected!=actual and actual==True:
        return {
                    "name": "x11_forwarding",
                    "status": "FAIL",
                    "message": "X11 Forwarding is enabled"
                }
    else:
        return {
            "name": "x11_forwarding",
            "status": "PASS",
            "message": "X11 Forwarding is disabled"
        }

def check_maxauthtries(config, sshd_config):

    max_auth_tries=int(sshd_config.get("maxauthtries"))
    expected = int(config['linux']['ssh']['max_auth_tries'])
    if expected<max_auth_tries:
        return {
                    "name": "max_auth_tries",
                    "status": "FAIL",
                    "message": "More Auth Tries than expected!"
                }
    else:
        return {
            "name": "x11_forwarding",
            "status": "PASS",
            "message": "Auth Tries are in range"
        }
    
def check_ssh_protocol(sshd_config):
    protocol = sshd_config.get("protocol")

    if protocol is None:
        return {
            "name": "SSH Protocol",
            "status": "PASS",
            "message": "SSH protocol 1 is not supported by this OpenSSH version.",
        }

    if protocol == "2":
        return {
            "name": "SSH Protocol",
            "status": "PASS",
            "message": "SSH protocol 2 is enabled.",
        }

    return {
        "name": "SSH Protocol",
        "status": "FAIL",
        "message": f"Unsupported SSH protocol configuration: {protocol}",
    }
