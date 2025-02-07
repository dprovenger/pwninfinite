import subprocess
import sys
import os

def iac_scan(directory_path):
  """Runs checkov to scan an IaC directory for security issues."""
  if not os.path.isdir(directory_path):
      print(f"Error: {directory_path} is not a valid directory.")
      sys.exit(1)

  try:
      result = subprocess.run(["checkov", "-d", directory_path], capture_output=True, text=True)
      print(result.stdout)

  except Exception as e:
      print(f"Error running checkov: {e}")
      sys.exit(1)

def main():
    """Main function to scan all files within the specified"""
    directory_to_scan = "iacCodeReviewDir"

    if not os.path.exists(directory_to_scan):
        print(f"Error: The direcotry '{directory_to_scan}' does not exists.")
        sys.exit(1)

    iac_scan(directory_to_scan)

if __name__ == "__main__":
    main()