document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('speak-button').onclick = function () {
		const text = document.getElementById('text-input').value;
		const voice = document.getElementById('voice-select').value;
		const speed = document.getElementById('speed-input').value;

		fetch('/speak', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ text: text, voice: voice, speed: speed }),
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.audio_url) {
					const audioElement = document.getElementById('audio');
					audioElement.src = data.audio_url;
					audioElement.play();
				} else {
					console.error('Error:', data.error);
				}
			});
	};
});
