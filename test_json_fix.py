#!/usr/bin/env python3
"""Test script to verify JSON parsing fix"""
import json

def clean_json(response):
    """Improved JSON cleanup logic"""
    response = response.strip()
    if response.startswith('```'):
        first_newline = response.find('\n')
        if first_newline != -1:
            response = response[first_newline + 1:]
        if response.rstrip().endswith('```'):
            last_backticks = response.rstrip().rfind('```')
            response = response[:last_backticks]
    return response.strip()

# Test cases
test_cases = [
    ('Wrapped with ```json', '```json\n{"title": "Test", "value": "Has ``` inside"}\n```'),
    ('Wrapped with ```', '```\n{"title": "Test"}\n```'),
    ('No markers', '{"title": "No markers"}'),
    ('Extra whitespace', '  ```json  \n{"title": "Test"}  \n```  '),
]

print("Testing JSON cleanup logic:\n")
passed = 0
failed = 0

for name, test in test_cases:
    cleaned = clean_json(test)
    try:
        result = json.loads(cleaned)
        print(f"✓ PASSED: {name}")
        print(f"  Result: {result}")
        passed += 1
    except json.JSONDecodeError as e:
        print(f"✗ FAILED: {name}")
        print(f"  Error: {e}")
        print(f"  Cleaned: {repr(cleaned[:100])}")
        failed += 1
    print()

print(f"\nSummary: {passed} passed, {failed} failed")
exit(0 if failed == 0 else 1)
