import zipfile
import os
import argparse

def check_zip_contents(zip_path):
    expected_files = {
        'run_llama.py',
        'base_llama.py',
        'llama.py',
        'rope.py',
        'classifier.py',
        'config.py',
        'optimizer.py',
        'sanity_check.py',
        'tokenizer.py',
        'utils.py',
        'README.md',
        'structure.md',
        'sanity_check.data',
        'generated-sentence-temp-0.txt',
        'generated-sentence-temp-1.txt',
        'sst-dev-prompting-output.txt',
        'sst-test-prompting-output.txt',
        'sst-dev-finetuning-output.txt',
        'sst-test-finetuning-output.txt',
        'cfimdb-dev-prompting-output.txt',
        'cfimdb-test-prompting-output.txt',
        'cfimdb-dev-finetuning-output.txt',
        'cfimdb-test-finetuning-output.txt',
        'setup.sh'
    }

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extracting the directory prefix (student_id_name) from the first file path
        first_file = zip_ref.namelist()[0]
        directory_prefix = os.path.dirname(first_file)
        
        if not directory_prefix or not all(name.startswith(directory_prefix + '/') for name in zip_ref.namelist()):
            print("All files must be under a single directory at the root of the ZIP file.")
            return False
        
        # Normalize file paths to ensure we only get the relative path after the directory
        normalized_paths = {os.path.relpath(name, directory_prefix) for name in zip_ref.namelist()}
        
        # Checking if there are extra or missing files
        extra_files = normalized_paths - expected_files
        missing_files = expected_files - normalized_paths

        if extra_files:
            print("Extra files found:", extra_files)
        if missing_files:
            print("Missing files:", missing_files)

        return not extra_files and not missing_files

def main():
    parser = argparse.ArgumentParser(description='Check if a zip file contains all and only specific files.')
    parser.add_argument('zip_path', type=str, help='The path to the zip file to check.')
    args = parser.parse_args()

    if check_zip_contents(args.zip_path):
        print("The zip file contains all and only the expected files.")
    else:
        print("The zip file does not meet the requirements.")

if __name__ == '__main__':
    main()
