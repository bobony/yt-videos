from django.shortcuts import render_to_response,RequestContext

from cfe.views import playlist_items

from .models import ListItems

def plist_items(request,id):
	try:
		p_list=ListItems.objects.get(list_id=id)
		lis=True
	except Exception:
		print "Playlist items are not available!"
		pass
	if lis:
		list_videos=playlist_items(p_list)
	else:
		pass	

	return render_to_response('videos.html',locals(),context_instance=RequestContext(request))
