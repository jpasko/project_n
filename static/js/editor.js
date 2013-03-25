$(document).ready(function(){
    $("#trigger-editable-about").on("click", function() {
	if ($("#valid-about").length) {
	    $("#valid-about").hide();
	    $("#about-textarea").val(formattedText($("#valid-about")));
	} else {
	    $("#empty-about").hide();
	}
	$("#about-textarea").show();
	resizeTextArea($("#about-textarea"));
	$("#save-about").show();
	$("#cancel-about").show();
    });
    $("#cancel-about").on("click", function() {
	$("#about-textarea").hide();
	$("#save-about").hide();
	$("#cancel-about").hide();
	$("#editable-about").find("p").show();
    });
    $("#save-about").on("click", function() {
	$("#about-textarea").hide();
	$("#save-about").hide();
	$("#cancel-about").hide();
	if ($("#about-textarea").val()) {
	    if ($("#empty-about").length) {
		$("#empty-about").remove();
	    }
	    if (!$("#valid-about").length) {
		$("#editable-about").append('<p id="valid-about"></p>');
	    }
	    $("#valid-about").show();
	    $("#valid-about").html(formatAsHTML($("#about-textarea").val()));
	} else {
	    if (!$("#empty-about").length) {
		$("#editable-about").append('<p id="empty-about"><em>Currently empty</em></p>');
	    }
	    if ($("#valid-about").length) {
		$("#valid-about").remove();
	    }
	    $("#empty-about").show();
	}
	$.ajax({
	    type: "POST",
	    url: "/update/",
	    data: {'about': $("#about-textarea").val()},
	    success: function(data) {
		$("#ajax-alert > p").remove();
		if (!data.success) {
		    $("#ajax-alert").show();
		    $("#ajax-alert").append("<p><strong>Error: </strong>" + data['message'] + "</p>");
		} else {
		    $("#ajax-alert").hide();
		}
	    }
	});
    });

    $("#trigger-editable-email").on("click", function() {
	if ($("#valid-email").length) {
	    $("#valid-email").hide();
	    $("#email-input").val($("#valid-email").text());
	} else {
	    $("#empty-email").hide();
	}
	$("#email-input").show();
	$("#save-email").show();
	$("#cancel-email").show();
    });
    $("#cancel-email").on("click", function() {
	$("#email-input").hide();
	$("#save-email").hide();
	$("#cancel-email").hide();
	$("#editable-email").find("p").show();
    });
    $("#save-email").on("click", function() {
	$("#email-input").hide();
	$("#save-email").hide();
	$("#cancel-email").hide();
	if ($("#email-input").val()) {
	    if ($("#empty-email").length) {
		$("#empty-email").remove();
	    }
	    if (!$("#valid-email").length) {
		$("#editable-email").append('<p id="valid-email"></p>');
	    }
	    $("#valid-email").show();
	    $("#valid-email").text($("#email-input").val());
	} else {
	    if (!$("#empty-email").length) {
		$("#editable-email").append('<p id="empty-email"><em>Currently empty</em></p>');
	    }
	    if ($("#valid-email").length) {
		$("#valid-email").remove();
	    }
	    $("#empty-email").show();
	}
	$.ajax({
	    type: "POST",
	    url: "/update/",
	    data: {'email': $("#email-input").val()},
	    success: function(data) {
		$("#ajax-alert > p").remove();
		if (!data.success) {
		    $("#ajax-alert").show();
		    $("#ajax-alert").append("<p><strong>Error: </strong>" + data['message'] + "</p>");
		} else {
		    $("#ajax-alert").hide();
		}
	    }
	});
    });

    $("#trigger-editable-phone").on("click", function() {
	if ($("#valid-phone").length) {
	    $("#valid-phone").hide();
	    $("#phone-input").val($("#valid-phone").text());
	} else {
	    $("#empty-phone").hide();
	}
	$("#phone-input").show();
	$("#save-phone").show();
	$("#cancel-phone").show();
    });
    $("#cancel-phone").on("click", function() {
	$("#phone-input").hide();
	$("#save-phone").hide();
	$("#cancel-phone").hide();
	$("#editable-phone").find("p").show();
    });
    $("#save-phone").on("click", function() {
	$("#phone-input").hide();
	$("#save-phone").hide();
	$("#cancel-phone").hide();
	if ($("#phone-input").val()) {
	    if ($("#empty-phone").length) {
		$("#empty-phone").remove();
	    }
	    if (!$("#valid-phone").length) {
		$("#editable-phone").append('<p id="valid-phone"></p>');
	    }
	    $("#valid-phone").show();
	    $("#valid-phone").text($("#phone-input").val());
	} else {
	    if (!$("#empty-phone").length) {
		$("#editable-phone").append('<p id="empty-phone"><em>Currently empty</em></p>');
	    }
	    if ($("#valid-phone").length) {
		$("#valid-phone").remove();
	    }
	    $("#empty-phone").show();
	}
	$.ajax({
	    type: "POST",
	    url: "/update/",
	    data: {'phone': $("#phone-input").val()},
	    success: function(data) {
		$("#ajax-alert > p").remove();
		if (!data.success) {
		    $("#ajax-alert").show();
		    $("#ajax-alert").append("<p><strong>Error: </strong>" + data['message'] + "</p>");
		} else {
		    $("#ajax-alert").hide();
		}
	    }
	});
    });

    $("#trigger-editable-location").on("click", function() {
	if ($("#valid-location").length) {
	    $("#valid-location").hide();
	    $("#location-input").val($("#valid-location").text());
	} else {
	    $("#empty-location").hide();
	}
	$("#location-input").show();
	$("#save-location").show();
	$("#cancel-location").show();
    });
    $("#cancel-location").on("click", function() {
	$("#location-input").hide();
	$("#save-location").hide();
	$("#cancel-location").hide();
	$("#editable-location").find("p").show();
    });
    $("#save-location").on("click", function() {
	$("#location-input").hide();
	$("#save-location").hide();
	$("#cancel-location").hide();
	if ($("#location-input").val()) {
	    if ($("#empty-location").length) {
		$("#empty-location").remove();
	    }
	    if (!$("#valid-location").length) {
		$("#editable-location").append('<p id="valid-location"></p>');
	    }
	    $("#valid-location").show();
	    $("#valid-location").text($("#location-input").val());
	} else {
	    if (!$("#empty-location").length) {
		$("#editable-location").append('<p id="empty-location"><em>Currently empty</em></p>');
	    }
	    if ($("#valid-location").length) {
		$("#valid-location").remove();
	    }
	    $("#empty-location").show();
	}
	$.ajax({
	    type: "POST",
	    url: "/update/",
	    data: {'location': $("#location-input").val()},
	    success: function(data) {
		$("#ajax-alert > p").remove();
		if (!data.success) {
		    $("#ajax-alert").show();
		    $("#ajax-alert").append("<p><strong>Error: </strong>" + data['message'] + "</p>");
		} else {
		    $("#ajax-alert").hide();
		}
	    }
	});
    });

    $("#trigger-editable-website").on("click", function() {
	if ($("#valid-website").length) {
	    $("#valid-website").hide();
	    $("#website-input").val($("#valid-website").attr('href'));
	} else {
	    $("#empty-website").hide();
	}
	$("#website-input").show();
	$("#save-website").show();
	$("#cancel-website").show();
    });
    $("#cancel-website").on("click", function() {
	$("#website-input").hide();
	$("#save-website").hide();
	$("#cancel-website").hide();
	$("#editable-website").find("p").show();
	$("#editable-website").find("a").show();
    });
    $("#save-website").on("click", function() {
	$("#website-input").hide();
	$("#save-website").hide();
	$("#cancel-website").hide();
	if ($("#website-input").val()) {
	    if ($("#empty-website").length) {
		$("#empty-website").remove();
	    }
	    if (!$("#valid-website").length) {
		$("#editable-website").append('<a id="valid-website" target="_blank"></a>');
	    }
	    $("#valid-website").show();
	    $("#valid-website").attr('href', $("#website-input").val());
	    $("#valid-website").text($("#website-input").val());
	} else {
	    if (!$("#empty-website").length) {
		$("#editable-website").append('<p id="empty-website"><em>Currently empty</em></p>');
	    }
	    if ($("#valid-website").length) {
		$("#valid-website").remove();
	    }
	    $("#empty-website").show();
	}
	$.ajax({
	    type: "POST",
	    url: "/update/",
	    data: {'website': $("#website-input").val()},
	    success: function(data) {
		$("#ajax-alert > p").remove();
		if (!data.success) {
		    $("#ajax-alert").show();
		    $("#ajax-alert").append("<p><strong>Error: </strong>" + data['message'] + "</p>");
		} else {
		    $("#ajax-alert").hide();
		}
	    }
	});
    });

    $("#trigger-editable-social").on("click", function() {
	if ($("#valid-social-blogger").length) {
	    $("#valid-social-blogger").hide();
	    $("#blogger-input").val($("#valid-social-blogger").attr('href'));
	}
	if ($("#valid-social-deviantart").length) {
	    $("#valid-social-deviantart").hide();
	    $("#deviantart-input").val($("#valid-social-deviantart").attr('href'));
	}
	if ($("#valid-social-digg").length) {
	    $("#valid-social-digg").hide();
	    $("#digg-input").val($("#valid-social-digg").attr('href'));
	}
	if ($("#valid-social-facebook").length) {
	    $("#valid-social-facebook").hide();
	    $("#facebook-input").val($("#valid-social-facebook").attr('href'));
	}
	if ($("#valid-social-flickr").length) {
	    $("#valid-social-flickr").hide();
	    $("#flickr-input").val($("#valid-social-flickr").attr('href'));
	}
	if ($("#valid-social-google_plus").length) {
	    $("#valid-social-google_plus").hide();
	    $("#google_plus-input").val($("#valid-social-google_plus").attr('href'));
	}
	if ($("#valid-social-linkedin").length) {
	    $("#valid-social-linkedin").hide();
	    $("#linkedin-input").val($("#valid-social-linkedin").attr('href'));
	}
	if ($("#valid-social-myspace").length) {
	    $("#valid-social-myspace").hide();
	    $("#myspace-input").val($("#valid-social-myspace").attr('href'));
	}
	if ($("#valid-social-orkut").length) {
	    $("#valid-social-orkut").hide();
	    $("#orkut-input").val($("#valid-social-orkut").attr('href'));
	}
	if ($("#valid-social-pinterest").length) {
	    $("#valid-social-pinterest").hide();
	    $("#pinterest-input").val($("#valid-social-pinterest").attr('href'));
	}
	if ($("#valid-social-tumblr").length) {
	    $("#valid-social-tumblr").hide();
	    $("#tumblr-input").val($("#valid-social-tumblr").attr('href'));
	}
	if ($("#valid-social-twitter").length) {
	    $("#valid-social-twitter").hide();
	    $("#twitter-input").val($("#valid-social-twitter").attr('href'));
	}
	if ($("#valid-social-wordpress").length) {
	    $("#valid-social-wordpress").hide();
	    $("#wordpress-input").val($("#valid-social-wordpress").attr('href'));
	}
	if ($("#valid-social-youtube").length) {
	    $("#valid-social-youtube").hide();
	    $("#youtube-input").val($("#valid-social-youtube").attr('href'));
	}
	if ($("#empty-social").length){
	    $("#empty-social").hide()
	}
	$("#all-social-inputs").show();
	$("#save-social").show();
	$("#cancel-social").show();
    });
    $("#cancel-social").on("click", function() {
	$("#all-social-inputs").hide();
	$("#save-social").hide();
	$("#cancel-social").hide();
	$("#editable-social").find("p").show();
	$("#editable-social").find("a").show();
    });
    $("#save-social").on("click", function() {
	$("#all-social-inputs").hide();
	$("#save-social").hide();
	$("#cancel-social").hide();
	var blogger, deviantart, digg, facebook ,flickr, google_plus, linkedin,
	    myspace, orkut, pinterest, tumblr ,twitter, wordpress, youtube;

	if ($("#blogger-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-blogger").length) {
		$("#editable-social").append('<a id="valid-social-blogger" target="_blank"><img id="appended-blogger"></a>');
	    }
	    $("#valid-social-blogger").show();
	    $("#valid-social-blogger").attr('href', $("#blogger-input").val());
	    $("#appended-blogger").attr('src', $("#blogger-img").text());
	    blogger = $("#blogger-input").val();
	} else {
	    blogger = '';
	}
	if ($("#deviantart-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-deviantart").length) {
		$("#editable-social").append('<a id="valid-social-deviantart" target="_blank"><img id="appended-deviantart"></a>');
	    }
	    $("#valid-social-deviantart").show();
	    $("#valid-social-deviantart").attr('href', $("#deviantart-input").val());
	    $("#appended-deviantart").attr('src', $("#deviantart-img").text());
	    deviantart = $("#deviantart-input").val();
	} else {
	    deviantart = '';
	}
	if ($("#digg-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-digg").length) {
		$("#editable-social").append('<a id="valid-social-digg" target="_blank"><img id="appended-digg"></a>');
	    }
	    $("#valid-social-digg").show();
	    $("#valid-social-digg").attr('href', $("#digg-input").val());
	    $("#appended-digg").attr('src', $("#digg-img").text());
	    digg = $("#digg-input").val();
	} else {
	    digg = '';
	}
	if ($("#facebook-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-facebook").length) {
		$("#editable-social").append('<a id="valid-social-facebook" target="_blank"><img id="appended-facebook"></a>');
	    }
	    $("#valid-social-facebook").show();
	    $("#valid-social-facebook").attr('href', $("#facebook-input").val());
	    $("#appended-facebook").attr('src', $("#facebook-img").text());
	    facebook = $("#facebook-input").val();
	} else {
	    facebook = '';
	}
	if ($("#flickr-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-flickr").length) {
		$("#editable-social").append('<a id="valid-social-flickr" target="_blank"><img id="appended-flickr"></a>');
	    }
	    $("#valid-social-flickr").show();
	    $("#valid-social-flickr").attr('href', $("#flickr-input").val());
	    $("#appended-flickr").attr('src', $("#flickr-img").text());
	    flickr = $("#flickr-input").val();
	} else {
	    flickr = '';
	}
	if ($("#google_plus-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-google_plus").length) {
		$("#editable-social").append('<a id="valid-social-google_plus" target="_blank"><img id="appended-google_plus"></a>');
	    }
	    $("#valid-social-google_plus").show();
	    $("#valid-social-google_plus").attr('href', $("#google_plus-input").val());
	    $("#appended-google_plus").attr('src', $("#google_plus-img").text());
	    google_plus = $("#google_plus-input").val();
	} else {
	    google_plus = $("#google_plus-input").val();
	}
	if ($("#linkedin-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-linkedin").length) {
		$("#editable-social").append('<a id="valid-social-linkedin" target="_blank"><img id="appended-linkedin"></a>');
	    }
	    $("#valid-social-linkedin").show();
	    $("#valid-social-linkedin").attr('href', $("#linkedin-input").val());
	    $("#appended-linkedin").attr('src', $("#linkedin-img").text());
	    linkedin = $("#linkedin-input").val();
	} else {
	    linkedin = '';
	}
	if ($("#myspace-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-myspace").length) {
		$("#editable-social").append('<a id="valid-social-myspace" target="_blank"><img id="appended-myspace"></a>');
	    }
	    $("#valid-social-myspace").show();
	    $("#valid-social-myspace").attr('href', $("#myspace-input").val());
	    $("#appended-myspace").attr('src', $("#myspace-img").text());
	    myspace = $("#myspace-input").val();
	} else {
	    myspace = '';
	}
	if ($("#orkut-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-orkut").length) {
		$("#editable-social").append('<a id="valid-social-orkut" target="_blank"><img id="appended-orkut"></a>');
	    }
	    $("#valid-social-orkut").show();
	    $("#valid-social-orkut").attr('href', $("#orkut-input").val());
	    $("#appended-orkut").attr('src', $("#orkut-img").text());
	    orkut = $("#orkut-input").val();
	} else {
	    orkut = '';
	}
	if ($("#pinterest-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-pinterest").length) {
		$("#editable-social").append('<a id="valid-social-pinterest" target="_blank"><img id="appended-pinterest"></a>');
	    }
	    $("#valid-social-pinterest").show();
	    $("#valid-social-pinterest").attr('href', $("#pinterest-input").val());
	    $("#appended-pinterest").attr('src', $("#pinterest-img").text());
	    pinterest = $("#pinterest-input").val();
	} else {
	    pinterest = '';
	}
	if ($("#tumblr-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-tumblr").length) {
		$("#editable-social").append('<a id="valid-social-tumblr" target="_blank"><img id="appended-tumblr"></a>');
	    }
	    $("#valid-social-tumblr").show();
	    $("#valid-social-tumblr").attr('href', $("#tumblr-input").val());
	    $("#appended-tumblr").attr('src', $("#tumblr-img").text());
	    tumblr = $("#tumblr-input").val();
	} else {
	    tumblr = '';
	}
	if ($("#twitter-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-twitter").length) {
		$("#editable-social").append('<a id="valid-social-twitter" target="_blank"><img id="appended-twitter"></a>');
	    }
	    $("#valid-social-twitter").show();
	    $("#valid-social-twitter").attr('href', $("#twitter-input").val());
	    $("#appended-twitter").attr('src', $("#twitter-img").text());
	    twitter = $("#twitter-input").val();
	} else {
	    twitter = '';
	}
	if ($("#wordpress-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-wordpress").length) {
		$("#editable-social").append('<a id="valid-social-wordpress" target="_blank"><img id="appended-wordpress"></a>');
	    }
	    $("#valid-social-wordpress").show();
	    $("#valid-social-wordpress").attr('href', $("#wordpress-input").val());
	    $("#appended-wordpress").attr('src', $("#wordpress-img").text());
	    wordpress = $("#wordpress-input").val();
	} else {
	    wordpress = '';
	}
	if ($("#youtube-input").val()) {
	    if ($("#empty-social").length) {
		$("#empty-social").remove();
	    }
	    if (!$("#valid-social-youtube").length) {
		$("#editable-social").append('<a id="valid-social-youtube" target="_blank"><img id="appended-youtube"></a>');
	    }
	    $("#valid-social-youtube").show();
	    $("#valid-social-youtube").attr('href', $("#youtube-input").val());
	    $("#appended-youtube").attr('src', $("#youtube-img").text());
	    youtube = $("#youtube-input").val();
	} else {
	    youtube = '';
	}

	if (!$("#blogger-input").val() && !$("#deviantart-input").val() && !$("#digg-input").val() && !$("#facebook-input").val() &&
	    !$("#flickr-input").val() && !$("#google_plus-input").val() && !$("#linkedin-input").val() && !$("#myspace-input").val() &&
	    !$("#orkut-input").val() && !$("#pinterest-input").val() && !$("#tumblr-input").val() && !$("#twitter-input").val() &&
	    !$("#wordpress-input").val() && !$("#youtube-input").val()) {
	    if (!$("#empty-social").length) {
		$("#editable-social").append('<p id="empty-social"><em>Currently empty</em></p>');
	    }
	    if ($("#valid-social-blogger").length) {
		$("#valid-social-blogger").remove();
	    }
	    if ($("#valid-social-deviantart").length) {
		$("#valid-social-deviantart").remove();
	    }
	    if ($("#valid-social-digg").length) {
		$("#valid-social-digg").remove();
	    }
	    if ($("#valid-social-facebook").length) {
		$("#valid-social-facebook").remove();
	    }
	    if ($("#valid-social-flickr").length) {
		$("#valid-social-flickr").remove();
	    }
	    if ($("#valid-social-google_plus").length) {
		$("#valid-social-google_plus").remove();
	    }
	    if ($("#valid-social-linkedin").length) {
		$("#valid-social-linkedin").remove();
	    }
	    if ($("#valid-social-myspace").length) {
		$("#valid-social-myspace").remove();
	    }
	    if ($("#valid-social-orkut").length) {
		$("#valid-social-orkut").remove();
	    }
	    if ($("#valid-social-pinterest").length) {
		$("#valid-social-pinterest").remove();
	    }
	    if ($("#valid-social-tumblr").length) {
		$("#valid-social-tumblr").remove();
	    }
	    if ($("#valid-social-twitter").length) {
		$("#valid-social-twitter").remove();
	    }
	    if ($("#valid-social-wordpress").length) {
		$("#valid-social-wordpress").remove();
	    }
	    if ($("#valid-social-youtube").length) {
		$("#valid-social-youtube").remove();
	    }
	    $("#empty-social").show();
	}
	$.ajax({
	    type: "POST",
	    url: "/update/",
	    data: {'blogger': blogger,
		   'deviantart': deviantart,
		   'digg': digg,
		   'facebook': facebook,
		   'flickr': flickr,
		   'google_plus': google_plus,
		   'linkedin': linkedin,
		   'myspace': myspace,
		   'orkut': orkut,
		   'pinterest': pinterest,
		   'tumblr': tumblr,
		   'twitter': twitter,
		   'wordpress': wordpress,
		   'youtube': youtube},
	    success: function(data) {
		$("#ajax-alert > p").remove();
		if (!data.success) {
		    $("#ajax-alert").show();
		    $("#ajax-alert").append("<p><strong>Error: </strong>" + formatAsHTML(data['message']) + "</p>");
		} else {
		    $("#ajax-alert").hide();
		}
	    }
	});
    });

    function resizeTextArea($element) {
	$element.height($element[0].scrollHeight);
    }

    function formattedText(element) {
	var str = $(element).html();
	var regex = /<br\s*[\/]?>/gi;
	return str.replace(regex, "\n");
    }

    function formatAsHTML(text) {
	var htmls = [];
	var lines = text.split(/\n/);
	var tmpDiv = jQuery(document.createElement('div'));
	for (var i = 0 ; i < lines.length ; i++) {
            htmls.push(tmpDiv.text(lines[i]).html());
	}
	return htmls.join("<br>");
    }
});
