$(document).ready(function(){

    $("#dialog").dialog({
      modal: true,
            bgiframe: true,
            width: 500,
            height: 200,
      autoOpen: false
      });

    $("a.confirm").click(function(e) {
        e.preventDefault();
        var theHREF = $(this).attr("href");

        $("#dialog").dialog('option', 'buttons', {
                "Confirm" : function() {
                    window.location.href = theHREF;
                    },
                "Cancel" : function() {
                    $(this).dialog("close");
                    }
                });

        $("#dialog").dialog("open");

    });

    $("#dialog-change-account").dialog({
      modal: true,
            bgiframe: true,
            width: 500,
            height: 200,
      autoOpen: false
      });

    $("a.confirm-change-account").click(function(e) {
        e.preventDefault();
        var theHREF = $(this).attr("href");

        $("#dialog-change-account").dialog('option', 'buttons', {
                "Yes" : function() {
                    window.location.href = theHREF;
                    },
                "Cancel" : function() {
                    $(this).dialog("close");
                    }
                });

        $("#dialog-change-account").dialog("open");

    });

});