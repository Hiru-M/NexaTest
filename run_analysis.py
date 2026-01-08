import json
import os
import argparse
from engine.rule_engine import RuleEngine
from rules.naming_rule import NamingConventionRule
from rules.function_length_rule import FunctionLengthRule
from rules.duplicate_code_rule import DuplicateCodeRule
from rules.parameter_count_rule import ParameterCountRule
from rules.dead_code_rule import DeadCodeRule
from rules.complexity_rule import ComplexityRule
from rules.docstring_rule import DocstringRule

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config", "rules_config.json")

    with open(config_path, "r") as f:
        return json.load(f)
    print("Config path:", config_path)

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.file) as f:
        code = f.read()

    config = load_config()

    engine = RuleEngine(
        rules=[
            NamingConventionRule(),
            FunctionLengthRule(),
            DuplicateCodeRule(),
            ParameterCountRule(),
            DeadCodeRule(),
            ComplexityRule(),
            DocstringRule()
        ],
        config=config
    )

    findings = engine.analyze(code)

    report = {
        "file": args.file,
        "summary": {
            "total": len(findings),
            "errors": sum(1 for f in findings if f["severity"] == "error"),
            "warnings": sum(1 for f in findings if f["severity"] == "warning")
        },
        "issues": findings
    }

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
