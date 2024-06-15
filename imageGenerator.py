from openai import OpenAI
import urllib.request

client = OpenAI(api_key = 'sk-YOUR KEY') # Get your own by signing up for OpenAI's website

def AIGenerator(object, AIfilename):
  text = f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: {object}. The most simple 2D cartoon depiction of {object}, but still resembling real. Very little detail colored clipart."
  
  # calling the custom function "generate"
  # saving the output in the file "result.jpg"
  url = generate(text)
  urllib.request.urlretrieve(url, AIfilename)

# function for text-to-image generation
# using create endpoint of DALL-E API
# function takes in a string argument
def generate(text):
    res = client.images.generate(
        model="dall-e-3",
        prompt=text,
        n=1,
        size="1024x1024",
    )
    # returning the URL of one image as we are generating only one image
    return res.data[0].url