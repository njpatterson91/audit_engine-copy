Audit Engine Project Documentation

Author: njpatterson91
Repository: audit_engine-copy
Date: April 6, 2025

⸻

Table of Contents
	1.	Introduction
	2.	Project Structure Overview
	3.	Module Documentation
	•	Loader Module
	•	Validator Module
	•	Auditor Module
	•	Calendar Module
	•	Reporter Module
	4.	Scripts Overview
	•	run_audit.py
	•	generate_fake_data.py
	•	streamlit_app.py
	5.	Data Files and Directories
	6.	Dependencies
	7.	Conclusion

⸻

Introduction

The Audit Engine project is a Python-based tool designed to perform audits on log data using a set of predefined audit rules. The engine validates data, processes audit logs, and generates reports that can be viewed either on the command line or via a web interface built with Streamlit.

⸻

Project Structure Overview

The repository is organized into the following key directories:
	•	data/
Contains input files and directories:
	•	audit_rules.json: Defines the rules used for auditing.
	•	raw_logs/: Directory containing unprocessed audit logs.
	•	audit_results/: Where the generated audit reports are stored.
	•	engine/
Contains the core modules of the audit engine:
	•	loader.py
	•	validator.py
	•	auditor.py
	•	calendar.py
	•	reporter.py
	•	scripts/
Contains various utility and interface scripts:
	•	run_audit.py: Main script to run the audit process.
	•	generate_fake_data.py: Generates synthetic audit logs for testing.
	•	streamlit_app.py: Provides a web interface to interact with the audit engine.
	•	requirements.txt
Lists the Python dependencies required for the project.

⸻

Module Documentation

Loader Module

File: engine/loader.py

Purpose:
Handles loading of data into the audit engine. It typically includes functions to:
	•	Read audit rules from a JSON file (e.g., audit_rules.json).
	•	Load raw audit log data from the specified directory (data/raw_logs).

Key Functions (Inferred):
	•	load_audit_rules(filepath):
Reads and parses the audit rules from a JSON file.
Input: File path to audit_rules.json
Output: A dictionary or object representing the audit rules.
	•	load_raw_logs(directory):
Scans the specified directory for log files and loads them for processing.
Input: Path to the raw logs directory
Output: A list or collection of log entries.

⸻

Validator Module

File: engine/validator.py

Purpose:
Ensures that the loaded audit logs and rules meet required formats and criteria before processing. This helps catch errors early in the audit process.

Key Functions (Inferred):
	•	validate_log_entry(log_entry):
Checks if a single log entry meets the expected format (e.g., required fields, valid timestamp formats).
Input: A log entry
Output: Boolean indicating validity (and possibly error messages).
	•	validate_rules(rules):
Verifies that the audit rules loaded from the JSON file are structured correctly and contain necessary parameters.
Input: The audit rules object
Output: Boolean or list of validation issues.

⸻

Auditor Module

File: engine/auditor.py

Purpose:
The central component that applies the audit rules to the validated log data. This module processes the logs, filters entries, and identifies any anomalies based on the defined rules.

Key Functions (Inferred):
	•	run_audit(logs, rules):
Main function that accepts validated logs and audit rules to perform the audit.
Input: Validated log entries and audit rules
Output: Audit results, which may include a summary of anomalies, passed checks, and any errors detected.
	•	process_entry(log_entry, rules):
Processes a single log entry against the rules to determine if it complies or violates any criteria.
Input: A log entry and the audit rules
Output: Result of the audit check for that entry.

⸻

Calendar Module

File: engine/calendar.py

Purpose:
Handles date and time operations that are crucial for auditing tasks, such as timestamp parsing and scheduling of audit jobs.

Key Functions (Inferred):
	•	parse_timestamp(timestamp_string):
Converts a string timestamp from a log entry into a Python datetime object, considering time zones.
Input: Timestamp as string
Output: Python datetime object.
	•	get_current_period():
Determines the current time period or audit window, which might be used to filter logs for a specific time range.
Input: None
Output: Time period or date range.

⸻

Reporter Module

File: engine/reporter.py

Purpose:
Generates and formats the final audit report based on the results produced by the Auditor module.

Key Functions (Inferred):
	•	generate_report(audit_results):
Formats the audit results into a human-readable report, possibly including summary statistics and details on anomalies.
Input: Audit results from the auditor
Output: A formatted string or file output.
	•	save_report(report, filepath):
Saves the generated report to a specified file (e.g., in the data/audit_results directory).
Input: Report content and file path
Output: Confirmation of successful write operation.

⸻

Scripts Overview

run_audit.py

Location: scripts/run_audit.py

Purpose:
This script acts as the main entry point to the audit engine. It coordinates the overall workflow:
	1.	Loads audit rules and raw logs using the Loader module.
	2.	Validates the data using the Validator module.
	3.	Runs the audit process using the Auditor module.
	4.	Generates and saves the final report using the Reporter module.

Flow:
	•	Import modules: loader, validator, auditor, and reporter.
	•	Execute data loading.
	•	Validate the loaded data.
	•	Process the logs to produce audit results.
	•	Generate and output the report.

⸻

generate_fake_data.py

Location: scripts/generate_fake_data.py

Purpose:
Generates synthetic audit log data to facilitate testing and development of the audit engine.
Usage:
Run this script to create fake log entries, which are then stored in the data/raw_logs directory for subsequent auditing.

⸻

streamlit_app.py

Location: scripts/streamlit_app.py

Purpose:
Provides a web-based user interface for interacting with the audit engine.
Features (Inferred):
	•	Visual display of audit reports.
	•	Options to upload log files or view generated results.
	•	Interactive elements to filter or search through audit data.

Usage:
Run the script with Streamlit (e.g., streamlit run streamlit_app.py) to launch the interactive dashboard.

⸻

Data Files and Directories
	•	audit_rules.json:
Contains the definitions and criteria for the audit checks. This file guides the logic in the Auditor module.
	•	raw_logs:
Directory for storing incoming audit logs. These logs are read and processed by the engine.
	•	audit_results:
Directory where the final audit reports are stored. The Reporter module writes the formatted report to this location.
	•	.DS_Store:
A macOS-specific file that can be ignored.

⸻

Dependencies

The project requires the following Python libraries as specified in requirements.txt:
	•	numpy==2.2.4
	•	pandas==2.2.3
	•	python-dateutil==2.9.0.post0
	•	pytz==2025.2
	•	six==1.17.0
	•	tzdata==2025.2

These libraries are used for numerical operations, data manipulation, and handling date/time functions.

⸻

Conclusion

The Audit Engine project is a modular, Python-based tool designed for processing and auditing log data. It includes a clear separation of concerns through distinct modules for loading data, validating it, running the audit checks, handling date/time functions, and reporting the results. The provided scripts further enable users to run the audit process, generate test data, and interact with the results via a web interface.

This documentation should serve as a comprehensive guide for understanding and extending the project. For further details or to contribute, please refer to the repository on GitHub.
