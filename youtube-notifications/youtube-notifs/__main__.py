import urllib.request
import json, time
from selenium import webdriver

# IMPORTANT: ON LINE 44, YOU NEED TO CHANGE THE BROWSER PYTHON OPENS ACCORDING TO YOUR PREFERENCE
# 
# IMPROTANT: YOU NEED TO EDIT THE SETTINGS.JSON FILE IN THE YOUTUBE-NOTIFICATIONS FOLDER 
#            TO YOUR SETTINGS IN ORDER FOR THIS TO WORK, BELOW YOU HAVE INSTRUCTIONS
# 
# instructions for the settings.json file:
# 
#   you can get the API KEY from:
#   https://console.developers.google.com
#   if you need support go to: https://developers.google.com/identity/protocols/OAuth2?hl=en_US
# 
#   the channel ID is in the URL of the channel you open after the /channel/. for example:
# 
#   https://www.youtube.com/user/PewDiePie
#   has the channel id of: PewDiePie - its an exception
# 
#   an average user, though would have this url:
#   https://www.youtube.com/channel/UCU_W0oE_ock8bWKjALiGs8Q
#   and the channel id is: UCU_W0oE_ock8bWKjALiGs8Q

def get_settings():
    return json.load(open("settings.json", "r"))

def search_for_video():
    api_key = settings["api_key"]
    channel_id = settings["channel_id"]

    base_video_url = "https://www.youtube.com/watch?v="
    base_search_url = "https://www.googleapis.com/youtube/v3/search?"

    # example url: 
    # https://www.googleapis.com/youtube/v3/search?key=AIzaSyBky6H0GBhnLBGJAC1alN5RSVCknTJryZt&channelId=UCS4c5bpra5blCUsHKPFSkih&part=snippet,id&order=date&maxResults=1
    url = base_search_url + \
        "key={}&channelId={}&part=snippet,id&order=date&maxResults=1".format(api_key, channel_id)
    result = urllib.request.urlopen(url)
    # example response: https://pastebin.com/H7kQkx0m
    resp = json.load(result)

    video_id = resp["items"][0]["id"]["videoId"]
    video_exists = True
    
    if video_exists:
        with open("video_id.json", "w") as file:
            data = {
                "videoId": video_id
            }
            json.dump(data, file)

    with open("video_id.json", "r") as file:
        data = json.load(file)
        if data["videoId"] != video_id:
            # webdriver.Chrome opens chrome, if u use firefox change it to Firefox etc.
            browser = webdriver.Chrome()
            browser.get(base_video_url + video_id)
            video_exists = True


settings = get_settings()["youtube"]

try:
    while True:
        search_for_video()
        # sleep for 1 second, you can change it to more, or less but beware that it can lag your computer if its too fast.
        # also, if you reach your quota limit, it wont work, you'll need to wait till it resets.
        time.sleep(12) 
except KeyboardInterrupt:
    print("quitting..")

