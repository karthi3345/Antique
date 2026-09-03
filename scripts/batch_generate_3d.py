import os
import time
import requests

API_KEY = "tsk_EGleCg_JHP2-PBFS8LBbrNKlr-L7aH4VoR8lcv7FEGU"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def generate_3d_for_object(object_id_str):
    image_path = f"static/img/objects/{object_id_str}/00.webp"
    output_path = f"static/img/objects/{object_id_str}/00.glb"
    
    if not os.path.exists(image_path):
        print(f"[-] Image not found: {image_path}")
        return

    print(f"[*] Processing {object_id_str}...")

    # 1. Upload Image
    with open(image_path, 'rb') as f:
        files = {'file': ('00.webp', f, 'image/webp')}
        r = requests.post('https://api.tripo3d.ai/v2/openapi/upload', headers=HEADERS, files=files)
        
    if r.status_code != 200 or r.json().get('code') != 0:
        print(f"[-] Upload failed: {r.json()}")
        return
        
    image_token = r.json()['data']['image_token']
    
    # 2. Create Task
    data = {'type': 'image_to_model', 'file': {'type': 'webp', 'file_token': image_token}}
    r = requests.post('https://api.tripo3d.ai/v2/openapi/task', headers=HEADERS, json=data)
    
    if r.json().get('code') != 0:
        print(f"[-] Task creation failed: {r.json().get('message')}")
        return
        
    task_id = r.json()['data']['task_id']
    print(f"    -> Task started: {task_id}")

    # 3. Poll for completion
    while True:
        r = requests.get(f'https://api.tripo3d.ai/v2/openapi/task/{task_id}', headers=HEADERS)
        status = r.json()['data']['status']
        
        if status == 'success':
            model_url = r.json()['data']['result']['model']['url']
            print("    -> Downloading 3D model...")
            model_data = requests.get(model_url).content
            with open(output_path, 'wb') as out_f:
                out_f.write(model_data)
            print(f"[+] Saved to {output_path}")
            break
        elif status in ['failed', 'cancelled', 'timeout']:
            print(f"[-] Task failed with status: {status}")
            break
            
        print("    -> Waiting...")
        time.sleep(5)

if __name__ == "__main__":
    # Example: Generate for object 043
    generate_3d_for_object("043")
    
    # To run for all objects, you would do:
    # for i in range(1, 57):
    #     generate_3d_for_object(f"{i:03d}")
