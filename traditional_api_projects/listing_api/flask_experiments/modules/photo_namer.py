import os

dir_path = input("Enter the path to the directory: ")

# Create a text file to write errors to
error_file = open("errors.txt", "w")

# Get a list of all subdirectories in the directory
subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

# Create a list to store the subdirectories with errors
error_subdirs = []

# Loop through each subdirectory
for subdir in subdirs:
    subdir_path = os.path.join(dir_path, subdir)
    # Get a list of all files in the subdirectory
    files = os.listdir(subdir_path)
    # Check if the files have already been named after the subdirectory
    if all(file_name.startswith(subdir) for file_name in files):
        print(f"All files in {subdir} have already been named after the subdirectory.")
        continue
    # Rename each file with the subdirectory name and an integer
    for i, file_name in enumerate(files):
        # Get the file extension
        file_ext = os.path.splitext(file_name)[1]
        # Construct the new file name
        new_file_name = f"{subdir}{i}{file_ext}"
        try:
            # Rename the file
            os.rename(os.path.join(subdir_path, file_name), os.path.join(subdir_path, new_file_name))
        except Exception as e:
            # Write the error message to the error file
            error_file.write(f"Error renaming {file_name} in {subdir}: {e}\n")
            print(f"Error renaming {file_name} in {subdir}: {e}")
            # Add the subdir to the error_subdirs list
            error_subdirs.append(subdir)
            # Skip to the next subdirectory
            break

# Close the error file
error_file.close()

# Print the subdirectories with errors
if error_subdirs:
    print("Errors occurred in the following subdirectories:")
    for subdir in error_subdirs:
        print(subdir)
else:
    print("No errors occurred.")