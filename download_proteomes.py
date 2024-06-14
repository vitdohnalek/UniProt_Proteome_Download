import requests
import glob
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_fasta(prot_ID):
    try:
        response = requests.get(f"https://rest.uniprot.org/uniprotkb/stream?query=proteome:{prot_ID}&format=fasta&compressed=false&includeIsoform=true")
        if response.status_code == 200 and response.text.startswith(">"):
            with open(f"./{prot_ID}.fasta", "w") as f:
                f.write(response.text)
            print(f"Download completed for {prot_ID}.. ")
        else:
            return prot_ID, "Error: Download failed or response format incorrect"
    except Exception as e:
        return prot_ID, f"Error: {str(e)}"

if __name__ == "__main__":
    IDs = []
    errors = []

    for file in glob.glob("*.list"):
        with open(file, "r") as f:
            for l in f:
                IDs.append(l.strip())

    # Concurrent download using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        futures = [executor.submit(download_fasta, prot_ID) for prot_ID in IDs]
        
        for future in as_completed(futures):
            result = future.result()
            if isinstance(result, tuple):
                errors.append(result[0])  # Append proteome ID to errors list
                print(result[1])  # Print error message
            elif isinstance(result, str):
                errors.append(result)  # Handle unexpected errors

    print("Download completed with errors for:")
    print(errors)
