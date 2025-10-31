import os
from ultralytics import YOLO
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
from appwrite.id import ID


model = YOLO("yolov8n.pt")


client = Client()
client.set_endpoint('https://your-appwrite-endpoint/v1')
client.set_project('project_id')
client.set_key('API key')


storage = Storage(client)
bucket_id = 'bucket_id'



def detect_bird(image_path):
    if not os.path.isfile(image_path):
        print("Image not found: ",image_path)
        return
    results = model(image_path,conf=0.6)
    bird_found = any(int(box.cls[0])== 14 for r in results for box in r.boxes)

    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", "detected_bird.jpg")

    results[0].save(filename=output_path)
    print("Output saved to ",output_path)

    if bird_found:
        print("Bird detected!")
        try:
            result = storage.create_file(
                bucket_id=bucket_id,
                file_id=ID.unique(),
                file=InputFile.from_path(output_path)
            )
            print("File uploaded successfully:", result)
        except Exception as e:
            print("Error uploading file:", e)
    else:
        print("No bird detected.")


if __name__ == "__main__":
    image_path = "image_path.jpg"
    detect_bird(image_path)

    