import urllib2
import json

from django.shortcuts import render_to_response, HttpResponse,HttpResponseRedirect,RequestContext

from playlist.models import ListItems

USERNAME = 'your-username'
API_KEY = 'your API_KEY'
CHANNEL_ID = 'Youtube Channel ID'

def cfevideos(request):
        play_lists = get_videos()
        url='https://www.googleapis.com/youtube/v3/playlists?key=%s&channelId=%s&part=snippet%%2CcontentDetails&maxResults=50' % (API_KEY, CHANNEL_ID)
   
        res = urllib2.urlopen(url).read()

        data = json.loads(res)
        for i in data['items']:
            list_id=i['id']

            new_id,created=ListItems.objects.get_or_create(list_id=list_id)
            if created:
                print "done!"
  
	return render_to_response('playlist.html',locals(),context_instance=RequestContext(request))

def get_videos():
    url='https://www.googleapis.com/youtube/v3/playlists?key=%s&channelId=%s&part=snippet%%2CcontentDetails&maxResults=50' % (API_KEY, CHANNEL_ID)
   
    res = urllib2.urlopen(url).read()

    play_lists = []
    data = json.loads(res)
    for i in data['items']:
        plist = {}

        plist['pid']=i['id']
        plist['title'] = i['snippet']['title']
        plist['count']=i['contentDetails']['itemCount']
        plist['thumb']=i['snippet']['thumbnails']['default']['url']

        play_lists.append(plist)

    return play_lists
   
def playlist_items(list_id):

    PLAYLIST_ID = list_id
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?key=%s&playlistId=%s&maxResults=50&part=snippet' % (API_KEY, PLAYLIST_ID)
    res = urllib2.urlopen(url).read()

    youtubePrefix = 'http://www.youtube.com/watch?v='
    videos = []
    data = json.loads(res)
    for i in data['items']:
        plitems = {}
        plitems['title'] = i['snippet']['title']
        plitems['desc'] = i['snippet']['description']
        plitems['pub'] = i['snippet']['publishedAt']
        plitems['id'] = i['snippet']['resourceId']['videoId']
        videos.append(plitems)

    # get info of videos
    videoIds = [i['id'] for i in videos]
    url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails&id=%s&key=%s' % (','.join(videoIds), API_KEY)
    res = urllib2.urlopen(url).read()
    data = json.loads(res)

    
    for video in videos:
        for i in data['items']:
            if i['id'] == video['id']:
                plitems = i['contentDetails']['duration']
                #format: PT1M30S for a 1:30 video, PT30S for a 0:30 video
                # parse duration without regex
                plitems = plitems.strip('PT').strip('S')
                duration = ''
                if 'M' in plitems:
                    plitems = plitems.split('M')
                    duration = '%s:%s' % (plitems[0].zfill(2), plitems[1].zfill(2))
                else:
                    duration = '00:%s' % plitemsDuration.zfill(2)

                video['duration'] = duration
                video['views'] = i['statistics']['viewCount']
                video['likes'] = i['statistics']['likeCount']
                video['dislikes'] = i['statistics']['dislikeCount']
                break

    return videos