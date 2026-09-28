import argparse

#this is a helper file for data gathering scripts
#the name of the functions already say what they are doing
def get_sshd_config(executor):
    output = executor.run(["sudo", "sshd", "-T"])

    return {
        parts[0]: parts[1]
        for line in output.stdout.splitlines()
        if (parts := line.split(maxsplit=1))
    }

def get_enabled_services(executor):
    res = executor.run(
        [
            "systemctl",
            "list-unit-files",
            "--type=service",
            "--state=enabled",
            "--no-legend",
            "--no-pager",
        ]
    )

    return {
        line.split()[0]
        for line in res.stdout.splitlines()
        if line.strip()
    }

def get_failed_services(executor):
    res = executor.run(
        [
            "systemctl",
            "--failed",
            "--type=service",
            "--no-legend",
            "--no-pager",
        ]
    )

    return {
        line.split()[0]
        for line in res.stdout.splitlines()
        if line.strip()
    }

def is_service_enabled(executor, service):
    res = executor.run(
        ["systemctl", "is-enabled", service],
        check=False,
    )

    return res.returncode == 0

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run system auditing checks."
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--local",
        action="store_true",
        help="Run checks against the local machine.",
    )

    mode.add_argument(
        "--host",
        metavar="HOST",
        help="Run checks against one inventory target.",
    )

    mode.add_argument(
        "--all",
        action="store_true",
        help="Run checks against all inventory targets.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the audit in JSON format.",
    )

    return parser.parse_args()
