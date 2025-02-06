import subprocess
import sys

def iac_scan(file_path):
  """Runs checkov to scan an IaC file for security issues."""
  try:
      result = subprocess.run(["checkov", "-f", file_path], capture_output=True, text=True)
      print(result.stdout)

  except Exception as e:
      print(f"Error running checkov: {e}")
      sys.exit(1)

def main():
    """Main function to handle user input and run the IaC scan"""
    if len(sys.argv) < 2:
        print("Usage: python3 iac_scanner.py <IaC file>")
        sys.exit(1)

    file_to_scan = sys.argv[1]
    iac_scan(file_to_scan)

if __name__ == "__main__":
    main()