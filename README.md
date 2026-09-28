# DevSecOps Linux Auditor

A Python-based security and system-health auditing tool for Linux hosts.

The project is designed to automate repeatable security and configuration checks across local and remote Linux systems. It supports both local execution and remote auditing over SSH and produces human-readable CLI reports or machine-readable JSON output.

The project was built as a practical DevSecOps automation project combining Python, Linux administration, SSH, security hardening, configuration management and CI/CD-oriented reporting.

## Features

* Audit local Linux hosts
* Audit remote Linux hosts over SSH
* YAML-based configuration and security policies
* Modular and reusable audit checks
* Separate command execution layer for local and remote execution
* SSH security configuration checks
* Firewall and network configuration checks
* Listening-port auditing
* User and UID checks
* File-permission checks
* Sudo configuration checks
* Service and system-update checks
* System-health checks
* Human-readable terminal reports
* JSON output for automation and CI/CD integration
* Multiple target hosts
* SSH connectivity validation before running audits

## Architecture

The application separates audit logic from command execution and reporting.

```text
                    ┌──────────────────┐
                    │      CLI         │
                    │    argparse      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Runner       │
                    │  orchestration   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │   Linux    │ │  Network   │ │   System   │
       │   Checks   │ │   Checks   │ │   Checks   │
       └────────────┘ └────────────┘ └────────────┘
              │
              ▼
       ┌─────────────────────┐
       │      Executor       │
       ├─────────────────────┤
       │ LocalExecutor       │
       │ SSHExecutor         │
       └──────────┬──────────┘
                  │
          ┌───────┴────────┐
          ▼                ▼
      Local host       Remote host
                         via SSH

                  │
                  ▼
          ┌─────────────────┐
          │    Reporting    │
          ├─────────────────┤
          │ CLI             │
          │ JSON            │
          └─────────────────┘
```

### Executor abstraction

Audit checks do not need to know whether commands are executed locally or remotely.

The executor layer provides a common interface:

```python
output = executor.run(command)
```

The same checks can therefore be executed through either:

* `LocalExecutor`
* `SSHExecutor`

This keeps the audit logic independent from the connection method and makes the application easier to extend.

## Project Structure

```text
devsecops-linux-auditor/
├── auditor/
│   ├── __init__.py
│   ├── config.py
│   ├── executor.py
│   ├── context.py
│   ├── runner.py
│   │
│   ├── checks/
│   │   ├── __init__.py
│   │   ├── linux/
│   │   │   ├── __init__.py
│   │   │   ├── ssh.py
|   |   |   ├── disk_health.py
│   │   │   ├── firewall.py
│   │   │   ├── users.py
│   │   │   ├── permissions.py
│   │   │   └── services.py
│   │   │
│   │   ├── network/
│   │   │   ├── __init__.py
│   │   │   └── ports.py
│   │   │
│   │
│   └── reporting/
│       ├── __init__.py
│       └── gen_report.py
│
├── tests/
├── config.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## Configuration

Security policies and thresholds are stored in `config.yaml` rather than being hard-coded into individual checks.

Example:

```yaml
ssh:
  password_authentication: false
  root_login: false
  empty_passwords: false
  x11_forwarding: false
  max_auth_tries: 4

allowed_ports:
  - 22
  - 80
  - 443

disk_usage_threshold: 80
```

This allows the audit logic to remain reusable across different environments.

Not every audit is configuration-driven. Some checks validate an intrinsic system state, such as whether failed systemd services are present.

## Requirements

* Python 3.10+
* Linux target system
* SSH client for remote auditing
* `sudo` access on audited hosts
* PyYAML

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Local audit

Run the auditor against the local machine:

```bash
python3 -m auditor.runner --local
```

### Remote audit

Audit a configured target:

```bash
python3 -m auditor.runner --host node1
```

### Audit all configured targets

```bash
python3 -m auditor.runner --all
```

### JSON output

Generate machine-readable JSON output:

```bash
python3 -m auditor.runner --host node1 --json
```

Save the output to a file:

```bash
python3 -m auditor.runner --host node1 --json > json_output.json
```

The JSON output contains the target, summary and individual check results:

```json
{
  "target": "node1",
  "summary": {
    "pass": 8,
    "fail": 3
  },
  "checks": [
    {
      "name": "SSH password authentication",
      "status": "PASS",
      "message": "Password authentication is disabled"
    }
  ]
}
```

The JSON format makes the auditor suitable for integration with other automation or CI/CD tooling.

## Audit Result Format

Each check returns a consistent result structure:

```python
{
    "name": "SSH password authentication",
    "status": "PASS",
    "message": "Password authentication is disabled"
}
```

Possible statuses are:

* `PASS`
* `FAIL`

This keeps checks independent from the presentation layer and allows the same results to be consumed by both the CLI and JSON reporters.

## Security Considerations

This project is intended for systems that you own or are authorized to audit.

Remote auditing requires SSH access and appropriate privileges on the target system.

The repository should not contain:

* SSH private keys
* passwords
* API tokens
* production credentials
* secrets
* sensitive infrastructure information

Configuration files containing environment-specific credentials or sensitive information should be excluded using `.gitignore`.

## Design Goals

The project focuses on several practical DevSecOps principles:

### Automation

Security and system-health checks should be repeatable rather than manually performed on every server.

### Configuration over hard-coding

Environment-specific policies and thresholds are stored in YAML configuration.

### Separation of concerns

Audit logic, command execution, orchestration and reporting are separated into different components.

### Local and remote execution

The same audit checks can operate against the local system or remote Linux hosts through the executor abstraction.

### Machine-readable results

JSON output allows audit results to be consumed by automation and potentially used as a CI/CD security gate.

## Future Improvements

Potential future extensions include:

* CI/CD integration as a security gate
* Additional Kubernetes security checks
* Automated severity levels
* HTML reporting
* Unit and integration test coverage
* Centralized audit result storage
* Prometheus/Grafana integration
