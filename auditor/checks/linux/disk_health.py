def check_disk_usage(executor, config):
    result=executor.run(["df","-P","/"])
    line = result.stdout.strip().splitlines()[-1]
    capacity = int(line.split()[4].rstrip("%"))
    expected=config['linux']['disk_health']['disk_usage_threshold']
    if capacity<=expected:
        return {
                "name": "dish_usage_threshold",
                "status": "PASS",
                "message": f"Disk usage is {capacity} and in the limit."
            }
    return {
            "name": "dish_usage_threshold",
            "status": "FAIL",
            "message": f"Disk usage is {capacity} -> so over the limit, check space!"
        }

