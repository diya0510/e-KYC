import pandas as pd
from datetime import datetime
import json

def filter_lines(lines):
    start_index=None
    last_index=None

    for i,line in enumerate(lines):
        if "INCOME TAX DEPARTMENT" in line:
            start_index=i
        if "Signature" in line:
            last_index=i
            break 

        filtered_lines=[]
        if start_index is not None and last_index is not None:
            for line in lines[start_index:last_index+1]:
                if len(line.strip()) >2:
                    filtered_lines.append(line.strip())

        return filtered_lines

def create_dataframe(text):
    lines=filter_lines(text)
    print("="*20)
    print(lines)
    print("="*20)
    pan=name=father_name=dob=None 
    data=[]
    for i,line in enumerate(lines):
        line_upper=line.upper()
        if "PERMANENT ACCOUNT NUMBER" in line_upper:
            pan=lines[i+1].strip()
        elif "NAME" in line_upper:
            name=lines[i+1].strip()
        elif "FATHER" in line_upper:
            father_name=lines[i+1]
        elif "/" in line:
            try:
                dob=datetime.strptime(line.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                pass
    data.append({"ID":pan,"Name":name,"Father's Name":father_name,"DOB":dob})
    df=pd.DataFrame(data)
    return df

def extract_information(data_string):
    # Split the data string into a list of words based on "|"
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]

    # Initialize the dictionary to store the extracted information
    extracted_info = {
        "ID": "",
        "Name": "",
        "Father's Name": "",
        "DOB": "",
        "ID Type": "PAN"
    }

    try:
       for i, word in enumerate(words):
            if "PERMANENT ACCOUNT NUMBER" in word.upper() and i + 1 < len(words):
                extracted_info["ID"] = words[i + 1]
                break

        # Name
       for i, word in enumerate(words):
            if "name" in word.strip().lower()  and i + 1 < len(words):
                extracted_info["Name"] = words[i + 1]
                break

        # Father's Name
       for i, word in enumerate(words):
            if "father" in word.lower() and i + 1 < len(words):
                extracted_info["Father's Name"] = words[i + 1]
                break

        # Date of Birth
       for word in words:
            try:
                dob_obj = datetime.strptime(word, "%d/%m/%Y")
                extracted_info["DOB"] = dob_obj.strftime("%Y-%m-%d")
                break
            except ValueError:
                continue

        # Final check
       if not extracted_info["ID"]:
            return None
       return extracted_info

    except Exception as e:
        print(f"Error extracting PAN info: {e}")
        return None 

        

    

