def save_file(filename: str, data: str):
    # Write the CSV data to a file
    with open(filename, "w", newline="") as file:
        file.write(data.strip())
