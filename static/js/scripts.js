function rate(songId, rating) {
	$.get($SCRIPT_ROOT + '/rate', {
		ID: songId,
		Rate: rating
	});
	updateSongs();
	return false;
}
function updateSongs() {
	$.getJSON($SCRIPT_ROOT + '/songs', { 'Genre':$GENRE }, function(data) {
		$('tbody').html('');
		$('table caption').text(data.genre);
		jQuery.each(data.songs, function(index, song) {
			$('tbody').append('<tr>'
			+ '<td>' + (parseInt(index,10)+1).toString() + '</td>'
			+ '<td>' + song.title + '</td>'
			+ '<td>' + song.artist + '</td>'
			+ '<td>' + song.year + '</td>'
			+ '<td>' + song.genre + '</td>'
			+ '<td> <span class="badge badge-inverse">' + song.score + '</span>'
			+ '&nbsp;'
			+ '<div class="btn-group">'
				+ '<a class="btn" onclick="rate(' + song.id + ', 2, ' + $GENRE + ')">'
					+ '<span class="text-success">' + song.up + '</span> <i class="icon-thumbs-up"></i>'
				+ '</a>'
				+ '<a class="btn" onclick="rate(' + song.id + ', 1, ' + $GENRE + ')">'
					+ '<span class="text-error">' + song.down + '</span> <i class="icon-thumbs-down"></i>'
				+ '</a>'
			+ '</div>'
			+ '<td>'
			+ '</tr>');
		});
	});
}
