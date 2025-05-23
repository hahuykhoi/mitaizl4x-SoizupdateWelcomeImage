from zlapi.models import Message
import requests
import random
import os

des = {
    'version': "1.0.7",
    'credits': "Nguyễn Đức Tài",
    'description': "Gửi ảnh gái"
}

a = ["1", "2", "3", "4", "6", "9", "12"]

def handle_anhgai_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        image_list_url = "https://raw.githubusercontent.com/nguyenductai206/list/refs/heads/main/listimg.json"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(image_list_url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        rd = random.choice(a)

        if isinstance(json_data, dict) and 'url' in json_data:
            image_urls = [json_data['url']]
        elif isinstance(json_data, list):
            image_urls = random.sample(json_data, min(int(rd), len(json_data)))
        else:
            raise ValueError("Dữ liệu trả về không hợp lệ")

        image_paths = []
        for index, image_url in enumerate(image_urls):
            image_response = requests.get(image_url, headers=headers)
            image_path = f'modules/cache/temp_image{index + 1}.jpeg'
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
            image_paths.append(image_path)

        if all(os.path.exists(path) for path in image_paths):
            total_images = len(image_paths)
            t = Message(text=f"Đã gửi: {total_images} ảnh")

            client.sendMultiLocalImage(
                imagePathList=image_paths,
                message=t,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=1600
            )

            for path in image_paths:
                os.remove(path)
        else:
            raise FileNotFoundError("Không thể lưu ảnh")

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'anhgai': handle_anhgai_command
    }
