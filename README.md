# YouTubeStreamGrabber

Fetch information about YouTube channels and their live streams.

## Requirements

- Python 3
- [google-auth](https://pypi.org/project/google-auth/)
- [google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)
- [google-api-python-client](https://pypi.org/project/google-api-python-client/)

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
