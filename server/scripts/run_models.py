import sys
import os
import requests
import tempfile
import subprocess

IP = "localhost"
PORT = "5000"

def get_file(element):
    parent_uuid = element["parent_uuid"]
    model_uuid = element["model_uuid"]
    option_name = element["option"]

    file_url = f"http://{IP}:{PORT}/{model_uuid}/file"

    r = requests.get(file_url)
    if r.status_code == 200:
        return r.text

    return None

def abort(reason):
    print(reason)
    sys.exit(1)

def execute_command(model, flags):
    args = ["tamarin-prover", model]
    for flag in flags.split(","):
        if flag != "":
            args.append(f"-D{flag}")

    args.append("--auto-sources")
    args.append("--prove")
    output = subprocess.check_output(args, stderr=subprocess.STDOUT)
    print("Model executed")
    return output

def upload_results(element, tmp_path):
    files = {'file': open(tmp_path,'rb')}
    values = {"model": element["parent_uuid"], "submodel": element["model_uuid"], "option": element["option"]}
    r = requests.post(f"http://{IP}:{PORT}/result", files=files, data=values)
    if r.status_code != 200:
        print("Error uploading the results")
        print(r.text)

def main():
    r = requests.get(f"http://{IP}:{PORT}/api/pending")
    if r.status_code != 200:
        abort("Impossible to retrieve Pending jobs")

    content = r.json()
    print(f"There are {len(content)} jobs")

    for element in content:
        print(f"Try to process {element}")
        file_content = get_file(element)
        fp, tmp_path = tempfile.mkstemp(suffix=".spthy")
        os.close(fp)

        with open(tmp_path, "w") as fp:
            fp.write(file_content)

        try:
            data = execute_command(tmp_path, element["flags"])
            os.remove(tmp_path)

            fp, tmp_path = tempfile.mkstemp()
            os.close(fp)

            with open(tmp_path, "wb") as fp:
                fp.write(data)
            
            upload_results(element, tmp_path)
            os.remove(tmp_path)
            print(f"Successfully ran {element}")

        except subprocess.CalledProcessError as e:
            os.remove(tmp_path)
            print("Problems with a model:")
            print(e.stdout)

if __name__ == "__main__":
    main()

