import time
import random
import requests
from zlapi.models import Message, ThreadType
from datetime import datetime, timedelta
import pytz
import ffmpeg
import json

time_messages = {
    "06:00": "Chào buổi sáng! Hãy bắt đầu một ngày mới tràn đầy năng lượng.",
    "07:00": "Đã đến giờ uống cà phê! Thưởng thức một tách cà phê nhé.",
    "08:30": "Đi học thôi nào :3",
    "10:00": "Chúc bạn một buổi sáng hiệu quả! Đừng quên nghỉ ngơi.",
    "11:00": "Chỉ còn một giờ nữa là đến giờ nghỉ trưa. Hãy chuẩn bị nhé!",
    "12:00": "Giờ nghỉ trưa! Thời gian để nạp năng lượng.",
    "13:00": "Chúc bạn buổi chiều làm việc hiệu quả.",
    "13:15": "Chúc bạn đi làm việc vui vẻ",
    "14:00": "Đến giờ làm việc rồi",
    "15:00": "Một buổi chiều vui vẻ! Đừng quên đứng dậy và vận động.",
    "17:00": "Kết thúc một ngày làm việc! Hãy thư giãn.",
    "18:00": "Chào buổi tối! Thời gian để thư giãn sau một ngày dài.",
    "19:00": "Thời gian cho bữa tối! Hãy thưởng thức bữa ăn ngon miệng.",
    "21:00": "Một buổi tối tuyệt vời! Hãy tận hưởng thời gian bên gia đình.",
    "22:00": "Sắp đến giờ đi ngủ! Hãy chuẩn bị cho một giấc ngủ ngon.",
    "23:00": "Cất điện thoại đi ngủ thôi nào thức đêm không tốt đâu!",
    "00:00": "BOT MITAIZL(Nguyễn Đức Tài) chúc các cạu ngủ ngon nhó"
}

vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

def get_video_info(video_url):
    try:
        probe = ffmpeg.probe(video_url)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        if video_stream:
            duration = float(video_stream['duration']) * 1000
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            return duration, width, height
        else:
            raise Exception("Không tìm thấy luồng video trong URL")
    except Exception as e:
        raise Exception(f"Lỗi khi lấy thông tin video: {str(e)}")

def start_auto(client):
    try:
        with open("modules/cache/data/vdgai.json", "r") as video_file:
            video_urls = json.load(video_file)
        
        with open("modules/cache/data/anhgai.json", "r") as image_file:
            image_urls = json.load(image_file)
        
        all_group = client.fetchAllGroups()
        allowed_thread_ids = [gid for gid in all_group.gridVerMap.keys() if gid != '9034032228046851908']

        last_sent_time = None

        while True:
            video_url = random.choice(video_urls)
            image_url = random.choice(image_urls)

            duration, width, height = get_video_info(video_url)

            now = datetime.now(vn_tz)
            current_time_str = now.strftime("%H:%M")
            
            if current_time_str in time_messages and (last_sent_time is None or now - last_sent_time >= timedelta(minutes=1)):
                message = time_messages[current_time_str]
                for thread_id in allowed_thread_ids:
                    gui = Message(text=f"[ MITAI PROJECT AUTOSEND {current_time_str} ]\n> {message}")
                    try:
                        client.sendRemoteVideo(
                            video_url, 
                            image_url,
                            duration=duration,
                            message=gui,
                            thread_id=thread_id,
                            thread_type=ThreadType.GROUP,
                            width=width,
                            height=height
                        )
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"Error sending message to {thread_id}: {e}")
                last_sent_time = now
            
            time.sleep(30)

    except Exception as e:
        print(f"Error in start_auto: {e}")
