import requests
import os
import python_comfy
import set_community_banner
import dropbox_image_uploader
import time
from lemmy import Lemmy

def read_last_known_post_id(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    return 0

def write_last_known_post_id(file_path, post_id):
    with open(file_path, 'w') as file:
        file.write(str(post_id))

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

def update_banner_if_new_post():
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

    python_comfy.create_new_banner(latest_post_title)
    # while not os.path.exists(banner_filepath):
    #     print("Waiting for banner to be created...")
    #     time.sleep(1)
    while True:
        
        files_after = os.listdir(output_dir)
        print("files_after_IF", str(len(files_after)))
        if len(files_after) > len(files_before):
            break
        time.sleep(1)  # Check every second

    #remove all files in files_after that are in files_before
    files_after = [x for x in files_after if x not in files_before]
    banner_filepath = os.path.join(output_dir, files_after[0])

    print("banner_filepath", banner_filepath)
    banner_url = dropbox_image_uploader.upload_image(banner_filepath)
    #wait for the image to be uploaded
    while not banner_url:
        print("Waiting for banner to be uploaded...")
        time.sleep(1)
    print("banner_url", banner_url)
    set_community_banner.update_banner(banner_url)
    #write_last_known_post_id(last_known_id_file_path, latest_post_id)
    print("Banner updated successfully!")
    # else:
    #     print("No new posts found.")


if __name__ == '__main__':
    update_banner_if_new_post()

