from auditor.checks.linux.firewall import check_firewall
from auditor.checks.linux.ssh import check_root_login,check_password_authentication,check_empty_passwords,check_x11forwarding,check_maxauthtries,check_ssh_protocol
from auditor.checks.network.ports import check_ports
from auditor.checks.linux.permissions import check_file_permissions,check_nopasswd
from auditor.checks.linux.services import check_forbidden_services,check_unattended_upgrades,check_failed_services
from auditor.checks.linux.users import check_users
from auditor.checks.linux.disk_health import check_disk_usage
from auditor.config import load_config,load_inventory
from auditor.executor import LocalExecutor,SSHExecutor
from auditor.context import get_sshd_config,get_enabled_services,is_service_enabled,parse_args,get_failed_services
from auditor.reporting.gen_report import print_audit_results
import sys
def run_checks(executor):
    config = load_config()
    #we run data gathering scripts which are needed only one time for multiple checks
    sshd_config=get_sshd_config(executor)
    enabled_services=get_enabled_services(executor)
    failed_services=get_failed_services(executor)
    upgrade_service=is_service_enabled(executor, "unattended-upgrades")
    
    results = []
    #we add results to array
    results.append(check_password_authentication(config, sshd_config))
    results.append(check_root_login(config, sshd_config))
    results.append(check_empty_passwords(config, sshd_config))
    results.append(check_x11forwarding(config, sshd_config))
    results.append(check_maxauthtries(config, sshd_config))
    results.append(check_ssh_protocol(sshd_config))
    results.append(check_firewall(executor, config))
    results.append(check_ports(executor, config))
    results.append(check_forbidden_services(enabled_services, config))
    results.append(check_failed_services(failed_services))
    results.append(check_file_permissions(executor, config))
    results.append(check_nopasswd(executor, config))
    results.append(check_unattended_upgrades(upgrade_service, config))
    results.append(check_users(executor, config))
    results.append(check_disk_usage(executor, config))

    return results
    

def run_target(name, target, args):
    #this function is used to run the audit on remote hosts
    args=args
    #initialize a SSHExecutor for remote hosts audit
    executor = SSHExecutor(
        host=target["host"],
        user=target["user"],
    )
    print(f"\nStarting checks for {name}...\n", file=sys.stderr)
    connection = executor.check_connection()
    #we check if we can reach and connect to remote host
    if not connection["reachable"]:
        print(f"[SKIP] {connection['message']}\n", file=sys.stderr)
        return

    if not connection["connectable"]:
        print(f"[SKIP] {connection['message']}\n", file=sys.stderr)
        return

    print("[OK] SSH connection established\n", file=sys.stderr)

    res=run_checks(executor)
    print_audit_results(name,res,args.json)


def main():
    args=parse_args() #we get the argument of the run command
    inventory = load_inventory() #loads the inventory from yaml file
    if args.local:
        executor = LocalExecutor() #if --local in command we initialize a local executor
        res=run_checks(executor)
        print_audit_results("locahost",res, args.json)

    elif args.host:
        if args.host not in inventory["targets"]:
            print(
                f"Error: target '{args.host}' is not present "
                "in the inventory."
            )
            return 1
        #runs the audit on a single target if exists in the inventory
        run_target(args.host,inventory["targets"][args.host],args)
        

    elif args.all:
        #runs the audit on all targets from the inventory
        for name, target in inventory["targets"].items():
            run_target(name,target,args)

    return 0

main()