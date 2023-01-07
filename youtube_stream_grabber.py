#!/usr/bin/env python3
import argparse
import google.auth
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import os

print()
print("YouTube Stream Grabber: Fetch information about YouTube channels and their live streams")
print("Made by Jeff Noel ( https://github.com/JF10R/YouTubeStreamGrabber/ )")
print()

if os.geteuid() == 0:
    print("This script should not be run as sudo. Arguments are not sanitized yet.")
    exit()

# Set up the command-line argument parser
parser = argparse.ArgumentParser(description='Fetch information about YouTube channels and their live streams')
parser.add_argument('-c', '--channels', required=True, help='a string or file containing a list of YouTube channel IDs')
parser.add_argument('-o', '--output', help='output file for the live stream information')
args = parser.parse_args()

# Read the list of channel IDs from the specified file or string
if os.path.exists(args.channels):
    # Read the list of channel IDs from the file
    with open(args.channels, 'r') as f:
        channels = f.read().splitlines()
else:
    # Treat the specified string as a single channel ID
    channels = [args.channels]

if args.output is not None:
    if not os.path.exists(args.output):
        open(args.output, 'w').close()

# Set up the API client and retrieve channel information
def get_channel_info(channel_id):
    # Get the API credentials and create the API client
    creds, service = get_authenticated_service()

    # Call the API's channels().list() method to retrieve the channel information
    results = service.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    ).execute()

    # Get the first item in the list (should be the only item, since we're searching by channel ID)
    channel = results['items'][0]
    return channel

# Get the video ID of the current live stream
def get_live_stream_video_id(channel_id, channel_name):
    # Get the API credentials and create the API client
    creds, service = get_authenticated_service()

    # Call the API's search().list() method to retrieve live streams for the channel
    results = service.search().list(
        part='id',
        type='video',
        eventType='live',
        channelId=channel_id
    ).execute()

    if len(results['items']) > 0:
        video_id = results['items'][0]['id']['videoId']
        channel_name = get_channel_info(channel_id)['snippet']['title']
        print(f'\033[92m[+] {channel_name}:\033[0m is currently streaming a live video. URL: https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&rel=0&disablekb=1&controls=1&cc_load_policy=0&modestbranding=1')
        return video_id
    else:
        print(f'\033[31m\033[1m[!] {channel_name}:\033[0m is not currently streaming a live video.')
        return False


# Output the live stream information to a file
def output_live_stream_info(channel_name, video_id, output_filename):
    # Read the current contents of the output file
    if output_filename:
        with open(output_filename, 'r') as f:
            lines = f.read().splitlines()

        # Check if the channel name is already in the file
        found = False
        for i, line in enumerate(lines):
            if line.startswith(channel_name):
                # Update the stream URL if the channel name is found
                lines[i] = f'{channel_name}: https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&rel=0&disablekb=1&controls=1&cc_load_policy=0&modestbranding=1'
                found = True
                break

        # Append the live stream information to the file if the channel name is not found
        if not found:
            lines.append(f'{channel_name}: https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&rel=0&disablekb=1&controls=1&cc_load_policy=0&modestbranding=1')
        else:
            print(f'\033[1m{channel_name}:\033[0m live stream URL updated.')

        # Write the updated contents to the output file
        with open(output_filename, 'w') as f:
            f.write('\n'.join(lines))

# Retrieve the API credentials and create the API client
def get_authenticated_service():
    # Check for the API credentials file
    if not os.path.exists('client_secret.json'):
        print("Error: API credentials file not found.")
        exit()

    # Get the API credentials and create the API client
    creds = google.oauth2.credentials.Credentials.from_authorized_user_file('client_secret.json', ['https://www.googleapis.com/auth/youtube'])
    service = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)
    return creds, service

# Iterate through the list of channels and check for live streams
for channel_id in channels:
    # Get the channel information
    channel = get_channel_info(channel_id)
    channel_name = channel['snippet']['title']

    video_id = get_live_stream_video_id(channel_id, channel_name)
    # Check if the channel is currently streaming a live video
    if video_id:
        # Output the live stream information to a file
        output_live_stream_info(channel_name, video_id, args.output)

# Output the contents of the output file
if (args.output):
    print()
    with open(args.output, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            print(line)
