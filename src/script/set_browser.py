#!/usr/bin/env python3

import argparse
import os

from set_user_number import WORKFLOW_BUNDLE_ID, set_alfred_workflow_variable


def parse_browser(value: str) -> str:
    browser = value.strip()
    if not browser:
        raise argparse.ArgumentTypeError("target_browser cannot be empty")
    return browser


def main() -> None:
    parser = argparse.ArgumentParser(description='Set workflow variable "target_browser"')
    parser.add_argument("browser", type=parse_browser, help="Browser name")
    args = parser.parse_args()

    workflow_bundle_id = os.environ.get("alfred_workflow_bundleid", WORKFLOW_BUNDLE_ID)
    set_alfred_workflow_variable("target_browser", args.browser, workflow_bundle_id)

    os.environ["target_browser"] = args.browser
    print(f"target_browser={args.browser}")


if __name__ == "__main__":
    main()
