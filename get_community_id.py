from lemmy import Lemmy

lemmy_instance = Lemmy("https://lemmy.world")  # Use your Lemmy instance URL
community_name = "digitalbioacoustics"  # Replace with your community's name

# Discover the community ID
community_id = lemmy_instance.discover_community(community_name)
print("Community ID:", community_id)
