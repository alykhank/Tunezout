function switchGenre(id) {
	var url = (id !== '0') ? '/genre/'+id+'/' : '/';
	$('table').load(url + ' table', function() {
		$('.genre').removeClass('btn-danger').addClass('btn-default');
		$('#genre' + id).removeClass('btn-default').addClass('btn-danger');
		$('.hasTooltip').tooltip();
	});
}
function rateSong(song, rating, genre) {
	$('table').load('/rate/' + song + '/' + rating + '/' + genre + ' table', function() {
		$('.hasTooltip').tooltip();
	});
}
