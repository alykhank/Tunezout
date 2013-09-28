function switchGenre(id) {
  var url = (id !== '0') ? '/genre/'+id+'/' : '/';
	$('table').load(url + ' table', function() {
		$('.genre').removeClass('btn-danger').addClass('btn-inverse');
		$('#genre' + id).removeClass('btn-inverse').addClass('btn-danger');
	});
}
function rateSong(song, rating, genre) {
	$('table').load('/rate/' + song + '/' + rating + '/' + genre + ' table');
}
