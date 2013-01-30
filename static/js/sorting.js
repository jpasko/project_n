/*$(function() {
    $( "#sortable" ).sortable();
    $( "#sortable" ).disableSelection();
});*/

$(document).ready(function() {
    $(".sortable-photos").sortable({
	opacity: 0.5,
	update : function (){
	    var order = $(this).sortable("serialize");
	    $.ajax({
		type: "POST",
		url: "/reorder_photos/",
		data: order
	    }); 
	}   
    });
    $(".sortable-galleries").sortable({
	opacity: 0.5,
	update : function (){
	    var order = $(this).sortable("serialize");
	    $.ajax({
		type: "POST",
		url: "/reorder_galleries/",
		data: order
	    }); 
	}   
    }); 
});

