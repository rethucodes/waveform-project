import subprocess
package_list = ["customtkinter", "Pillow", "requests"]
for package in package_list:
    try:
        __import__(package)
        print(f"Package already exists: {package}")
    except ImportError:
        print(f"Package {package} not found. Installing...")
        subprocess.check_call(["pip", "install", package])