import os

def list_files(directory):
    """Lists all files in the specified directory."""
    if not os.path.exists(directory):
        print(f"⚠ Directory '{directory}' not found. Creating it now...")
        os.makedirs(directory)  # Create 'data/' directory if it doesn't exist
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files

def get_user_choice(files):
    """Prompts the user to select a file from the list."""
    print("\n📂 Available case files in 'data/':")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    while True:
        try:
            choice = int(input("\n🔹 Enter the number of the file you want to open: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("❌ Invalid choice. Please enter a valid number.")
        except ValueError:
            print("❌ Please enter a valid number.")

def select_case_file():
    """Lists files in the 'data/' directory and allows user selection."""
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")  # Change to 'data/' directory
    files = list_files(directory)

    if not files:
        print("⚠ No case files found in the 'data/' directory.")
        return None

    selected_file = get_user_choice(files)
    return os.path.join(directory, selected_file)
