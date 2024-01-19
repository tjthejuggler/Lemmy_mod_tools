import openai # openai v1.0.0+
client = openai.OpenAI(api_key="anything",base_url="http://0.0.0.0:8000") # set proxy to base_url
# request sent to model set on litellm proxy, `litellm --model`
response = client.chat.completions.create(model="gpt-3.5-turbo", messages = [
    {
        "role": "user",
        "content": "this is a test request, write a short poem"
    }
])

print(response)

# [Here](https://youtu.be/loZ1fv9_j9k?si=M8Jj5vATi7jePacV&t=1230) is the video where i heard about the study. It's a good video, but the relevant part is towards the end, 20:30. It would be interesting if to know if they asked any followup questions afterwards to find out if the jerky had occured to them when they were judging the minds in the questions.