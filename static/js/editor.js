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
	    data: {'about': $("#about-textarea").val()}
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
	    data: {'email': $("#email-input").val()}
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
	    data: {'phone': $("#phone-input").val()}
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
	    data: {'location': $("#location-input").val()}
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
	    data: {'website': $("#website-input").val()}
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
