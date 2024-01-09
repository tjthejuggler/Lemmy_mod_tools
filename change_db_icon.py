import requests
import os
import python_comfy
import set_community_icon
import dropbox_image_uploader
import time
from lemmy import Lemmy
import json
import ask_local_llm
import ask_chatGPT
import subprocess

#import LMstudio_RPA

# def read_last_known_post_id(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as file:
#             return int(file.read().strip())
#     return 0

# def write_last_known_post_id(file_path, post_id):
#     with open(file_path, 'w') as file:
#         file.write(str(post_id))

def fetch_latest_post_info(community_id, excluded_title="Bioacoustics Resources"):
    lemmy_instance = Lemmy("https://lemmy.world")

    # Fetch the latest posts from the community
    posts_data = lemmy_instance.post.list(community_id=community_id, sort='Hot', page=1, limit=5)

    if 'posts' in posts_data:
        for post_data in posts_data['posts']:
            post = post_data['post']
            if post['name'] != excluded_title:
                return post['id'], post['name']  # Return the ID and title of the latest post
    else:
        print("Failed to fetch posts or no posts available.")

    return None, None

def get_animal_from_post_title(post_title, force_animal=None):
    #look in post_title_animal_history.json for post_title
    #if it exists, return the animal
    with open('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history.json', 'r') as f:
        post_title_animal_history = json.load(f)
    if force_animal:
        #put force_animal in post_title_animal_history.json at post_title
        post_title_animal_history[post_title] = force_animal
        with open('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history.json', 'w') as f:
            json.dump(post_title_animal_history, f)
        title_subject = force_animal
        print("title_subject from force_animal", title_subject)
        return title_subject
    if post_title in post_title_animal_history:
        title_subject = post_title_animal_history[post_title]
        print("title_subject from json", title_subject)
        return title_subject        
    else:
        title_subject = "Nothing has been attempted to be made yet"
        local_failed = False
        try:
            print('trying')
            system_prompt = "You are an information parser. You only ever respond with a single animal name with no special characters or punctuation. You receive the title of an article. You respond with a type of animal that the article is about. You follow directions precisely."
            #LMstudio_is_already_running = LMstudio_RPA.is_server_running()
            # if LMstudio_is_already_running == False:
            #     print("starting server")
            #     LMstudio_RPA.start_server()
            ask_local_llm.connect_to_llm()
            llm_prompt = ("Respond with a single type on animal and no punctuation. What animal might an article with the title '"+post_title+"' be about? Respond only with the name of the animal.")
            title_subject = ask_local_llm.send_prompt_to_llm(llm_prompt, system_prompt)
            orca_mini = subprocess.Popen(["ollama", "run", "orca-mini:3b"], preexec_fn=os.setsid)
            time.sleep(5)
            orca_mini.kill()

            #LMstudio_RPA.stop_server()
            #remove whitespace from before and after the title_subject
            title_subject = title_subject.strip()
            print("title_subject from local llm", title_subject)
            #get the number of words in the title_subject
        except:
            title_subject = "Local LLM failed to make anything"
            local_failed = True
        #title_subject_num_words = len(title_subject.split(" "))
        if (local_failed == True):
            gpt_prompt = ("Respond with a single type on animal and no punctuation. What animal might an article with the title '"+post_title+"' be about? Respond only with the name of the animal.")
            title_subject = ask_chatGPT.send_request(gpt_prompt)
            title_subject = title_subject.strip()
            print("title_subject from chatGPT", title_subject)
        #add post_title and title_subject to post_title_animal_history.json
        post_title_animal_history[post_title] = title_subject
        with open('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history.json', 'w') as f:
            json.dump(post_title_animal_history, f)
        return title_subject

def get_funny_phrase_from_post_title(post_title, force_animal=None):
    #look in post_title_animal_history_funny_phrase.json for post_title
    #if it exists, return the animal
    with open('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history_funny_phrase.json', 'r') as f:
        post_title_animal_history_funny_phrase = json.load(f)
    if force_animal:
        #put force_animal in post_title_animal_history_funny_phrase.json at post_title
        post_title_animal_history_funny_phrase[post_title] = force_animal
        with open('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history_funny_phrase.json', 'w') as f:
            json.dump(post_title_animal_history_funny_phrase, f)
        funny_phrase = force_animal
        print("funny_phrase from force_animal", funny_phrase)
        return funny_phrase
    if post_title in post_title_animal_history_funny_phrase:
        funny_phrase = post_title_animal_history_funny_phrase[post_title]
        print("funny_phrase from json", funny_phrase)
        return funny_phrase        
    else:
        funny_phrase = "Nothing has been attempted to be made yet"
        local_failed = False
        try:
            print('trying')
            system_prompt = "You are graphic designer. Your specialty is creating comedic icons from headlines. As a part of your process you first create a description of the icon based on the headline that you receive. The images you create expertly utilize your intelligence to make mockery of the article. Your comedic descriptions are very detailed. Your comedic descriptions are a single sentence of less than 20 words. Your comedic descriptions are specifically designed to be seen as a small image. You separate the different aspects of the comedic description with commas. You only ever respond with a single sentence. Always provide your comedic descriptions without any additional comments or introductory statements. Do not include the headline in your response. Follow directions precisely."
            #LMstudio_is_already_running = LMstudio_RPA.is_server_running()
            # if LMstudio_is_already_running == False:
            #     print("starting server")
            #     LMstudio_RPA.start_server()
            ask_local_llm.connect_to_llm()
            llm_prompt = ("Write a comedic icon description for an article with the title: \n'"+post_title+"'")
            funny_phrase = ask_local_llm.send_prompt_to_llm(llm_prompt, system_prompt)
            if post_title.lower() in funny_phrase.lower():
                funny_phrase = funny_phrase.lower().replace(post_title.lower(), "")
            if ":" in funny_phrase:
                funny_phrase = funny_phrase.replace(":", "")
            print("funny_phrase", funny_phrase)
            orca_mini = subprocess.Popen(["ollama", "run", "orca-mini:3b"], preexec_fn=os.setsid)
            time.sleep(5)
            orca_mini.kill()

            #LMstudio_RPA.stop_server()
            #remove whitespace from before and after the funny_phrase
            funny_phrase = funny_phrase.strip()
            print("funny_phrase from local llm", funny_phrase)
            #get the number of words in the funny_phrase
        except:
            funny_phrase = "Local LLM failed to make anything"
            local_failed = True
        #funny_phrase_num_words = len(funny_phrase.split(" "))
        if (local_failed == True):
            gpt_prompt = ("Write an icon description fot an article with the title '"+post_title+"' . If you do a good job you will get a $1,000 commision.")
            funny_phrase = ask_chatGPT.send_request(gpt_prompt)
            funny_phrase = funny_phrase.strip()
            print("funny_phrase from chatGPT", funny_phrase)
        #add post_title and funny_phrase to post_title_animal_history_funny_phrase.json
        post_title_animal_history_funny_phrase[post_title] = funny_phrase
        with open('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history_funny_phrase.json', 'w') as f:
            json.dump(post_title_animal_history_funny_phrase, f)
        return funny_phrase

def update_icon_if_new_post(force_animal=None):
    community_id = 78581  # Your community ID
    # last_known_id_file_path = '/home/lunkwill/projects/Lemmy_mod_tools/last_post_id.txt'
    # last_known_post_id = read_last_known_post_id(last_known_id_file_path)

    latest_post_id, latest_post_title = fetch_latest_post_info(community_id)

    if force_animal:
        print("force_animal", force_animal)
        if force_animal.lower() == "replace":
            force_animal = None

            json_history = {}
            with open ('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history_funny_phrase.json', 'w') as f:
                json.dump(json_history, f)
            #remove the latest_post_title item from json_history
            json_history.pop(latest_post_title, None)

            with open ('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history_funny_phrase.json', 'w') as f:
                json.dump(json_history, f) 
    else:
        print("no force_animal")


    # print("Latest post ID:", latest_post_id)
    # print("Latest post title:", latest_post_title)
    # print("Last known post ID:", last_known_post_id)
    # if latest_post_id and latest_post_id != last_known_post_id:
    output_dir = "/home/lunkwill/projects/ComfyUI/output"
    files_before = os.listdir(output_dir)
    print("files_before_IF", str(len(files_before)))

    #original lemmy style icon
    # title_animal = get_animal_from_post_title(latest_post_title, force_animal)
    # python_comfy.create_new_icon(title_animal)

    funny_phrase = get_funny_phrase_from_post_title(latest_post_title, force_animal)
    python_comfy.create_new_icon_funny(funny_phrase)

    while True:        
        files_after = os.listdir(output_dir)
        print("files_after_IF", str(len(files_after)))
        if len(files_after) > len(files_before):
            break
        time.sleep(1)  # Check every second

    files_after = [x for x in files_after if x not in files_before]
    icon_filepath = os.path.join(output_dir, files_after[0])

    print("icon_filepath", icon_filepath)


    icon_url = dropbox_image_uploader.upload_image(icon_filepath)
    #wait for the image to be uploaded
    while not icon_url:
        print("Waiting for icon to be uploaded...")
        time.sleep(1)
    print("icon_url", icon_url)
    set_community_icon.update_icon(icon_url)
    #write_last_known_post_id(last_known_id_file_path, latest_post_id)


    print("icon updated successfully!")
    # else:
    #     print("No new posts found.")
    return funny_phrase


if __name__ == '__main__':
    update_icon_if_new_post()

