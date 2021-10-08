import traceback
import TikTokApi
import re
import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import os
tt = TikTokApi.TikTokApi.get_instance(custom_verifyFp=str(os.environ.get("TT-TOKEN")))

token = str(os.environ.get("VK-TOKEN"))

vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api( )
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api( )
VkUpload = VkUpload(vk)
while True:
	try:
		
		for event in longpoll.listen( ):
			if event.type == VkEventType.MESSAGE_NEW and event.from_me:
				if event.text.startswith(("https://vm.", "https://www.tiktok.com", "https://tiktok.com")):
					link = list(filter(lambda x: 'tiktok.com/' in x, event.text.split(" ")))[0]
					res = requests.get(link).history[0].headers["location"].split("?")[0]
					v_id = re.sub("\D", "", res)
					down_url = tt.get_tiktok_by_id(v_id)["itemInfo"]["itemStruct"]["video"]["downloadAddr"]
					c = tt.get_video_by_download_url(down_url)
					with open("video.mp4", "wb") as f:
						f.write(c)
					video_link = VkUpload.video("video.mp4")
					vk.messages.send(
						peer_id=event.peer_id, random_id=random.randint(-100000000, 10000000),
						attachment=f"video{video_link['owner_id']}_{video_link['video_id']}"
						)
	except Exception:
		print(traceback.format_exc( ))
