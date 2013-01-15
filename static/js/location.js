// Script to find the (current) location of the user, and
// build a list of closest users.
$(document).ready(function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    } else {
        console.log('GPS not supported');
    }
});

function successCallback(position) {
    console.log('GPS location successful');
    getNearbyUsers(position.coords.latitude, position.coords.longitude);
}

function errorCallback(error) {
    console.log('Must enter location manually');
}

function getNearbyUsers(lat, lng) {
    // Simple test of AJAX get.
    $.get('/list_users/', function(data) {
	var users = JSON.parse(data);
	for (var i = 0; i < users.length; i++) {
	    $('#output').append(
		'<a href="/user/' + users[i] + '/"/ >' + users[i] + '</a>');
	    $('#output').append('<br />');
	}
    });

    // Simple test of AJAX post.
/*    $.ajaxSetup({
	beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		// Send the token to same-origin, relative URLs only.
		// Send the token only if the method warrants CSRF protection
		// Using the CSRFToken value acquired earlier
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
	}
    });
    $.post('/xhr_test/', {
	name: 'Monty',
	food: 'spam'
    },
	   function(data) {
	       alert(data);
	   }
    );
*/
}
