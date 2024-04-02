#!/usr/bin/env python3
import argparse
import json
import os
import tarfile


# Step 1: Extract json submission file
def extract_file(path_to_submission):
    if not os.path.exists(path_to_submission):
        raise FileNotFoundError(f"The file {path_to_submission} does not exist.")
    try:
        with tarfile.open(path_to_submission, "r:xz") as t:
            json_file = t.extractfile("submission.json")
            data = json.load(json_file)
    except tarfile.TarError as error:
        print(f"Error extracting file from tar archive: {error}.")
    except json.JSONDecodeError as error:
        print(f"Error decoding JSON data: {error}.")

    return data


# Step 2: Text Test Report
def calculate_outcome(test_cases):

    total_run_time = sum(test["duration"] for test in test_cases)

    pass_count = sum(1 for test in test_cases if test["status"] == "pass")
    fail_count = sum(1 for test in test_cases if test["status"] == "fail")
    skip_count = sum(1 for test in test_cases if test["status"] == "skip")

    fail_test_cases = [test["id"] for test in test_cases if test["status"] == "fail"]

    return total_run_time, fail_test_cases, pass_count, fail_count, skip_count


def calculate_percentage(pass_count, fail_count, total_test_cases):
    pass_percentage = round((pass_count / total_test_cases) * 100)
    fail_percentage = round((fail_count / total_test_cases) * 100)
    skip_percentage = 100 - (pass_percentage + fail_percentage)

    return pass_percentage, fail_percentage, skip_percentage


def text_report(data):

    version = data["distribution"]["description"]

    test_cases = data["results"]

    total_test_cases = len(test_cases)

    total_run_time, fail_test_cases, pass_count, fail_count, skip_count = calculate_outcome(test_cases)

    fail_percentage, pass_percentage, skip_percentage = calculate_percentage(pass_count, fail_count, total_test_cases)

    print(f"Version tested: {version}")
    print(f"Number of tests run: {total_test_cases}")
    print("Outcome:")
    print(f"- skip: {skip_count} ({skip_percentage}%)")
    print(f"- fail: {fail_count} ({fail_percentage}%)")
    print(f"- pass: {pass_count} ({pass_percentage}%)")
    print(f"Total run duration: {round(total_run_time)} seconds")
    print("List of failed tests:")
    for failed_id in fail_test_cases:
        print(f"- {failed_id}")


# Step 3: Json Test Report
def json_report(data):

    version = data["distribution"]["description"]

    test_cases = data["results"]

    total_test_cases = len(test_cases)

    total_run_time, fail_test_cases, pass_count, fail_count, skip_count = calculate_outcome(test_cases)

    json_data = {
        "version": version,
        "nb_skip": skip_count,
        "nb_fail": fail_count,
        "nb_pass": pass_count,
        "total_duration": round(total_run_time),
        "failed_tests": fail_test_cases
    }

    return json.dumps(json_data)


# Step 4: Parse command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Generate reports based on Checkbox test submissions")
    parser.add_argument("path_to_submission", help="Path to the archive file")
    parser.add_argument("--type", choices=['json', 'text'], default='text', help="Json and text report type")
    arg = parser.parse_args()
    data = extract_file(arg.path_to_submission)

    if arg.type == "text":
        text_report(data)
    elif arg.type == "json":
        json_report_file = json_report(data)
        print(json_report_file)


if __name__ == "__main__":
    main()


