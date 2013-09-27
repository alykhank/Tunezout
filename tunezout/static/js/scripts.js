function switchGenre(id) {
	$.get('/songs?genre=' + id, function(data) {
		$('table').html(data);
		$('.genre').removeClass('btn-danger').addClass('btn-inverse');
		$('#genre' + id).removeClass('btn-inverse').addClass('btn-danger');
	});
}
function rateSong(song, rating, genre) {
	$.get('/rate?id=' + song + '&rate=' + rating + '&genre=' + genre, function(data) {
		$('table').html(data)
	});
}
