Function.prototype.bindExecutionScope = function(scope) {
  var _function = this;

  return function() {
    return _function.apply(scope, arguments);
  }
}

$(document).ready(function(){
    $('.video-thumbnail').each(function() {
	var url = $(this).attr("href");
	var success = function(image) {
	    $(this).find("img").attr('src', image);
	};
	success = success.bindExecutionScope(this);
	processURL(url, success);
    });
   $('.video-thumbnail-img').each(function() {
	var url = $(this).attr("data-url");
	var success = function(image) {
	    $(this).attr('src', image);
	};
	success = success.bindExecutionScope(this);
	processURL(url, success);
    });
});

function processURL(url, success){
    var video = parseVideoURL(url);
    if (video.provider == 'failure') {
	window.console.warn('Unrecognised video URL');
    }
    else if (video.provider == 'youtube') {
	if (!video.id) {
	    window.console.warn('Unsupported YouTube URL');
	} else {
	    success('http://img.youtube.com/vi/' + video.id + '/mqdefault.jpg');
	}
    } else if (video.provider == 'vimeo') {
	$.ajax({
            url: 'http://vimeo.com/api/v2/video/' + video.id + '.json',
            dataType: 'jsonp',
            success: function(data) {
		success(data[0].thumbnail_medium);
            }
	});
    } else { // dailymotion
	if (!video.id) {
	    window.console.warn('Unsupported Dailymotion URL');
	} else {
	    success('http://dailymotion.com/thumbnail/video/' + video.id + '?fields=thumbnail_medium_url');
	}
    }

    function parseVideoURL(url) {
	// Try youtube first:
	var match = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/i.exec(url);
	if (match && match[7].length==11) {
	    return {
		provider : 'youtube',
		id : match[7]
	    }
	}
	// Now try vimeo:
	match = /vimeo.*\/(\d+)/i.exec(url);
	if (match) {
	    return {
		provider : 'vimeo',
		id : match[1]
	    }
	}
	// Finally try dailymotion:
	match = /^.+dailymotion.com\/(video|hub)\/([^_]+)[^#]*(#video=([^_&]+))?/i.exec(url);
	if (match) {
	    return {
		provider : 'dailymotion',
		id : match[4] ? match[4] : match[2]
	    }
	}
	// Couldn't match anything:
	return {
	    provider : 'failure',
	    id : 0
	}
    }
}
