import os
import subprocess

def check_and_add_dvc(file_path):
    """
    Check if the .dvc file exists. If not, add the file to DVC tracking.
    """
    dvc_file = f"{file_path}.dvc"
    if os.path.exists(dvc_file):
        print(f"{dvc_file} is already tracked by DVC.")
    else:
        print(f"Adding {file_path} to DVC...")
        subprocess.run(["dvc", "add", file_path], check=True)

def commit_and_push_to_git(files, commit_message):
    """
    Stage files, commit them, and push to the remote repository.
    """
    try:
        # Stage changes for Git
        for file in files:
            print(f"Staging {file}...")
            subprocess.run(["git", "add", file], check=True)
        
        # Commit the changes
        print(f"Committing changes: {commit_message}")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push changes to the remote repository
        print("Pushing changes to GitHub...")
        subprocess.run(["git", "push"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")

def main():
    # Files to track with DVC
    files_to_check = [
        "Data/bitcoin_prices.csv",
        "Data/bitcoin_prices_cleaned.csv",
        "Model/bitcoin_lstm_model.h5",
        "Model/bitcoin_scaler.pkl"
    ]
    
    # Check and add files to DVC
    for file_path in files_to_check:
        check_and_add_dvc(file_path)
    
    # List of .dvc files to commit and push
    dvc_files = [f"{file}.dvc" for file in files_to_check]
    commit_message = "Track and push updated DVC files for bitcoin project"

    # Commit and push to GitHub
    commit_and_push_to_git(dvc_files + [".gitignore"], commit_message)

if __name__ == "__main__":
    main()
