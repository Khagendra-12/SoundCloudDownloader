import requests
import re
import subprocess

def get_client_id(soundcloud_track_url):
    try:
        response = requests.get(soundcloud_track_url)
        response.raise_for_status()
        html = response.text

        js_urls = re.findall(r'https://a-v2\.sndcdn\.com/assets/.*?\.js', html)
        if not js_urls:
            print("Could not find JS assets URL.")
            return None

        js_url = js_urls[-1]
        js_response = requests.get(js_url)
        js_response.raise_for_status()
        js_content = js_response.text

        match = re.search(r'client_id\s*:\s*"([a-zA-Z0-9]{32})"', js_content)
        if match:
            return match.group(1)

        match_alt = re.search(r'client_id\s*=\s*"([a-zA-Z0-9]{32})"', js_content)
        if match_alt:
            return match_alt.group(1)

        print("client_id not found in JS file.")
        return None

    except Exception as e:
        print("Error fetching client_id:", e)
        return None


def download_soundcloud_track(url, client_id):
    try:
        command = f'scdl -l "{url}" --client-id {client_id}'
        print("Running command:", command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        print("stdout:\n", result.stdout)
        print("stderr:\n", result.stderr)

    except Exception as e:
        print("An error occurred:", e)


track_url = "https://soundcloud.com/ARTISTNAME/SONGNAME"       #Insert https link from soundcloud.
client_id = get_client_id(track_url)
print("Extracted client_id:", client_id)
download_soundcloud_track(track_url, client_id)                #Download in the same file you are running the code.