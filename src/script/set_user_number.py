#!/usr/bin/env python3

import argparse
import os


def parse_account(value: str) -> str:
    try:
        account = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("userNumber must be an integer from 0 to 9") from exc

    if account < 0 or account > 9:
        raise argparse.ArgumentTypeError("userNumber must be between 0 and 9")

    return str(account)


def main() -> None:
    parser = argparse.ArgumentParser(description='Set environment variable "userNumber"')
    parser.add_argument("account", type=parse_account, help="Account number (0-9)")
    args = parser.parse_args()

    os.environ["userNumber"] = args.account
    print(f'userNumber={args.account}')


if __name__ == "__main__":
    main()
