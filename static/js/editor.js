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
	$("#about-textarea").select();
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
