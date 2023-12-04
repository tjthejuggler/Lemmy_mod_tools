import time
from lemmy import Lemmy
import os
import telegram_service

def read_last_known_post_id(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    return 0

def write_last_known_post_id(file_path, post_id):
    with open(file_path, 'w') as file:
        file.write(str(post_id))

def fetch_second_hottest_post_info(community_id, excluded_title="Bioacoustics Resources"):
    lemmy_instance = Lemmy("https://lemmy.world")

    # Fetch the hottest posts from the community
    posts_data = lemmy_instance.post.list(community_id=community_id, sort='Hot', page=1, limit=5)

    if 'posts' in posts_data:
        # Skip the first post and get the second post
        for i, post_data in enumerate(posts_data['posts']):
            if i == 1:
                post = post_data['post']
                if post['name'] != excluded_title:
                    return post['id'], post['name']  # Return the ID and title of the second hottest post
    else:
        print("Failed to fetch posts or no posts available.")

    return None, None

def start_post_checker():
    community_id = 78581  # Your community ID
    last_known_id_file_path = '/home/lunkwill/projects/Lemmy_mod_tools/last_post_id.txt'
    last_known_post_id = read_last_known_post_id(last_known_id_file_path)

    while True:
        second_hottest_post_id, second_hottest_post_title = fetch_second_hottest_post_info(community_id)
        #print("second_hottest_post_title:", second_hottest_post_title)
        if second_hottest_post_id and second_hottest_post_id != last_known_post_id:
            print("The second hottest post has changed.")
            telegram_service.send_telegram_text_as_me_to_bot("The second hottest post has changed.")
            telegram_service.send_telegram_text_as_me_to_bot("u")
            # Update the last known post ID
            write_last_known_post_id(last_known_id_file_path, second_hottest_post_id)
        time.sleep(60)  # Check every minute

if __name__ == '__main__':
    start_post_checker()