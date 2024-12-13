import os
import zipfile
import shutil

def process_fzpz_fzbz_file(file_path):
    """
    Processes a `.fzpz` or `.fzbz` file: extracts, modifies the `.fzp` files, and re-packages the `.fzpz` or `.fzbz` file
    only if changes are made. If no changes are made, the original file is kept.
    """
    # Create a temporary directory for extraction
    temp_dir = file_path + '_temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Extract the .fzpz or .fzbz file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Flag to track if any modification was made
    any_modification = False

    # Check the extracted files for `.fzp` files
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.fzp'):
                fzp_file_path = os.path.join(root, file)
                print(f"Processing: {fzp_file_path}")

                # Read the file content
                with open(fzp_file_path, 'rb') as f:
                    content = f.read()

                original_content = content

                # Remove <0x00> bytes (i.e., 0x00)
                content = content.replace(b'\x00', b'')

                # Ensure 'hybrid='yes'' is followed by a space if not already
                content_str = content.decode('utf-8', errors='ignore')
                content_str = content_str.replace("hybrid='yes'", "hybrid='yes' ")

                # Convert it back to bytes
                content = content_str.encode('utf-8')

                # If content was modified, write it back to the file
                if content != original_content:
                    any_modification = True
                    with open(fzp_file_path, 'wb') as f:
                        f.write(content)

    # If any modification was made, re-package the files into the original `.fzpz` or `.fzbz` file
    if any_modification:
        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_ref.write(file_path, os.path.relpath(file_path, temp_dir))

        print(f"Original file overwritten: {file_path}")
    else:
        print("No modifications were made, skipping repackaging.")

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

def find_and_process_fzpz_fzbz_files(directory):
    """
    Traverses the specified folder, finds all `.fzpz` and `.fzbz` files, and processes them.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.fzpz') or file.endswith('.fzbz'):
                file_path = os.path.join(root, file)
                print(f"Found file: {file_path}")
                process_fzpz_fzbz_file(file_path)

if __name__ == "__main__":
    directory_to_scan = "./"  # Specify the folder path to scan
    find_and_process_fzpz_fzbz_files(directory_to_scan)
