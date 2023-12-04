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
            system_prompt = "You are an information parser. You follow directions exactly. You only ever say a single animal name with no special characters or punctuation. You receive the title of an article. You respond with a type of animal that the article is about."
            #LMstudio_is_already_running = LMstudio_RPA.is_server_running()
            # if LMstudio_is_already_running == False:
            #     print("starting server")
            #     LMstudio_RPA.start_server()
            title_subject = ask_local_llm.send_prompt_to_llm(post_title, system_prompt)
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
            gpt_prompt = ("Respond with a single type on animal and no punctuation. What animal might an article with the title '"+post_title+"' be about?")
            title_subject = ask_chatGPT.send_request(gpt_prompt)
            title_subject = title_subject.strip()
            print("title_subject from chatGPT", title_subject)
        #add post_title and title_subject to post_title_animal_history.json
        post_title_animal_history[post_title] = title_subject
        with open('/home/lunkwill/projects/Lemmy_mod_tools/post_title_animal_history.json', 'w') as f:
            json.dump(post_title_animal_history, f)
        return title_subject


def update_icon_if_new_post(force_animal=None):
    community_id = 78581  # Your community ID
    # last_known_id_file_path = '/home/lunkwill/projects/Lemmy_mod_tools/last_post_id.txt'
    # last_known_post_id = read_last_known_post_id(last_known_id_file_path)

    latest_post_id, latest_post_title = fetch_latest_post_info(community_id)
    # print("Latest post ID:", latest_post_id)
    # print("Latest post title:", latest_post_title)
    # print("Last known post ID:", last_known_post_id)
    # if latest_post_id and latest_post_id != last_known_post_id:
    output_dir = "/home/lunkwill/projects/ComfyUI/output"
    files_before = os.listdir(output_dir)
    print("files_before_IF", str(len(files_before)))
    title_animal = get_animal_from_post_title(latest_post_title, force_animal)
    python_comfy.create_new_icon(title_animal)

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


if __name__ == '__main__':
    update_icon_if_new_post()

