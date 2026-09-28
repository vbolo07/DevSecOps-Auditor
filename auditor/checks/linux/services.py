def check_forbidden_services(services, config):
    forbidden = config['linux']['services']['forbidden']

    enabled_services = services
    enabled_forbidden = []

    for service in forbidden:
        service_name = (
            service
            if service.endswith(".service")
            else f"{service}.service"
        )

        if service_name in enabled_services:
            enabled_forbidden.append(service)

    if not enabled_forbidden:
        return {
                "name": "forbidden_services",
                "status": "PASS",
                "message": "NO forbidden services enabled"
            }

    return {
            "name": "forbidden_services",
            "status": "FAIL",
            "message": f"These forbidden services are enabled:{enabled_forbidden}"
        }


def check_unattended_upgrades(is_enabled, config):
    required = config.get("linux", {}).get("updates", {}).get(
        "unattended_upgrades", False
    )
    
    if not required:
        return {
                "name": "unattended_upgrades",
                "status": "PASS",
                "message": "Unattended upgrades not required by policy"
            }

    if is_enabled:
        return {
                "name": "unattended_upgrades",
                "status": "PASS",
                "message": "Unattended upgrades enabled"
            }

    return {
            "name": "unattended_upgrades",
            "status": "FAIL",
            "message": "Unattended upgrades are NOT enabled"
        }

def check_failed_services(services):
    failed=services
    if not failed:
        return {
            "name": "Failed Services",
            "status": "PASS",
            "message": "No failed services found.",
        }

    return {
        "name": "Failed Services",
        "status": "FAIL",
        "message": f"Failed services: {', '.join(sorted(failed))}",
    }

