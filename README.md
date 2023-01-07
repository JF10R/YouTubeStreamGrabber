# YouTubeStreamGrabber

Fetch information about YouTube channels and their live streams.  

![Example output with John Hammond and DrLupo channels](https://user-images.githubusercontent.com/2191497/211171113-60009f93-6bfc-4774-9a12-a18814cdaff0.png)

The main motivation behind it was to have a small script to grab a list of livestream URLs in a online tournament setting. I am not sure how this would work with *unlisted* YouTube streams as I doubt the API will list those.

## Requirements

- Python 3
- [google-auth](https://pypi.org/project/google-auth/)
- [google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)
- [google-api-python-client](https://pypi.org/project/google-api-python-client/)

## Setup

Once you cloned the repository, you can fetch the required Google libraries with requirements.txt:

```bash
pip install -r requirements.txt
```

### Google Cloud Console project

You will need to create a Google Cloud Console project though the [GCP Developer Console](https://console.cloud.google.com/) which has access to the YouTube Data API v3.  
You will then need to create a OAuth 2.0 Client in the project and enter its `Client ID`, `Client Secret` and the `Project ID` in the `client_secret.json` file.

You can use the helper script, `getRefreshToken.py`, by calling it as-is without parameters, after you filled the fields mentioned above to grab the refresh_token from the callback url. This is the last field you need to fill in the `client_secret.json` file.

The scripts uses two methods from YouTube's Data API:  

- `youtube.api.v3.V3DataChannelService.List`
  - To grab the livestream information (is the livestream on? If so, what is the `videoid`?)
- `youtube.api.v3.V3DataSearchService.List`
  - To grab the channel name for verbosity.

## Usage

```bash
python youtube_stream_grabber.py -c CHANNELS [-o OUTPUT]
```

### Parameters

- `-c CHANNELS`:  Required. A string or file containing a list of YouTube channel IDs.  
- `-o OUTPUT`:    Optional. Output file for the live stream information. If this parameter is not provided, the live stream information will only be printed and not written to a file on disk.

## Example
```bash
python youtube_stream_grabber.py -c channels.txt -o livestreams.txt

# Checking if DrLupo is live, and getting the stream URL
python youtube_stream_grabber.py -c UCVeW9qkBjo3zosnqUbG7CFw
```

## Credits

- Jeff Noel (https://github.com/JF10R)
- OpenAI ChatGPT
