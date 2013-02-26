$(document).ready(function() {
    $(".sortable-items").sortable({
	opacity: 0.5,
	update : function (){
	    var order = $(this).sortable("serialize");
	    $.ajax({
		type: "POST",
		url: "/reorder_items/",
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

