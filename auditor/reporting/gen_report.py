import json
#generating results for both CLI and JSON depending on the argument
def get_summary(results):
    passed = sum(1 for res in results if res["status"] == "PASS")
    failed = sum(1 for res in results if res["status"] == "FAIL")

    return {
        "pass": passed,
        "fail": failed
    }
def print_audit_results(node, results, json_output=False):
    summary=get_summary(results)
    
    if json_output:
        output = {
            "target": node,
            "summary": summary,
            "checks": results
        }

        print(json.dumps(output, indent=2))
        return

    # Normal CLI output
    width = 50

    print("=" * width)
    print(f"Security Audit: {node}")
    print("=" * width)
    print()

    for res in results:
        print(f"{res['status']:<6}{res['name']:<27}{res['message']}")

    print()
    print("-" * width)
    print(f"Result: {summary['pass']} PASS / {summary['fail']} FAIL")
    print("-" * width)