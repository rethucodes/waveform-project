#Importing all the packages
try:
    import customtkinter as ctk
    import os
    import requests
    from PIL import Image
    import threading
    import time
except:
    print('Install all the necessary packages to run this application.')
    time.sleep(5)
    exit()

#Creating main window
def create_root():
    root = ctk.CTk()
    root.title("WAVE FORM")
    ctk.set_appearance_mode("system")
    root.geometry("910x512")
    root.resizable(False, False)
    return root

#Loads image objects
def ctk_image(light, dark, width, height, file_path="Resources"):
    if dark is None:
        image = ctk.CTkImage(Image.open(os.path.join(file_path, light)), size=(width, height))
    else:
        image = ctk.CTkImage(
            light_image=Image.open(os.path.join(file_path, light)),
            dark_image=Image.open(os.path.join(file_path, dark)),
            size=(width, height)
        )
    return image

#Creating GUI elements in main window
def create_frame1(root):
    frame1 = ctk.CTkFrame(master=root)
    frame1.pack(fill=ctk.BOTH, expand=True)
   
    #Generates the image
    def start_generate():
        
        def generate():
            generate_button.configure(text='Generating...', state='disabled')
            user_prompt = prompt_entry.get("0.0", ctk.END).strip() + " "
            url = "https://api.prodia.com/v1/sdxl/generate"
            payload = {
                "prompt": user_prompt,
                "negative_prompt": "unrealistic, badly drawn",
                "steps": 25,
                "cfg_scale": 7,
                "seed": -1,
                "upscale": True,
                "aspect_ratio": "square",
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "X-Prodia-Key": prodia_api,
            }
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()
            jobid = response_data["job"]
            request_url = f"https://api.prodia.com/v1/job/{jobid}"
            while True:
                try:
                    response = requests.get(request_url, headers=headers)
                    response_data = response.json()
                    image_link = response_data["imageUrl"]
                    image_name = jobid + '.png'
                    break
                except:
                    pass
            print(image_link)
            generate_button.configure(text='Downloading...')
            filename = os.path.join("img_generator", image_name)
            img = Image.open(requests.get(image_link, stream = True).raw)
            img.save(filename)
            photo_image = ctk_image(filename, filename, 512, 512, file_path='')
            image_canvas_label.configure(image=photo_image)
            generate_button.configure(text='Generate', state='normal')

        download_thread = threading.Thread(target=generate)
        download_thread.start()

    waveform_logo = ctk_image("waveform_logo-light.png", "waveform_logo-dark.png", 209, 79)
    navigation_frame = ctk.CTkFrame(master=frame1)
    navigation_frame.grid(row=0, column=0, sticky="NSEW")
    logo_label = ctk.CTkLabel(master=navigation_frame, text="", image=waveform_logo)
    logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=40)
    prompt_label = ctk.CTkLabel(master=navigation_frame, text="Prompt", font=ctk.CTkFont("Verdana", 18, weight="bold"))
    prompt_label.grid(row=1, column=0, padx=30, pady=50)
    prompt_entry = ctk.CTkTextbox(master=navigation_frame, width= 215, height=70)    
    prompt_entry.grid(row=1, column=1, padx=30, pady=50)
    generate_button = ctk.CTkButton(
        master=navigation_frame,
        corner_radius=20,
        height=40,
        width=300,
        text="Generate",
        font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
        command=start_generate,
        cursor="hand2"
    )
    generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=40)
    image_canvas = ctk.CTkCanvas(master=frame1, height=512, width=512)
    image_canvas.grid(row=0, column=1)
    img = ctk_image("canvas_image-light.png", "canvas_image-dark.png", 512, 512)
    image_canvas_label = ctk.CTkLabel(master=image_canvas, text="",image=img)
    image_canvas_label.grid(row=0, column=0)

#Start function
def root():
    with open("Resources/api.txt") as file:
        global prodia_api
        prodia_api = file.read().strip()
    main = create_root()
    create_frame1(main)
    main.mainloop()

if __name__ == "__main__":
    root()