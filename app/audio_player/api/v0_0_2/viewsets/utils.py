def build_audio_obj(audio):
    audio_dict = {
        'id': audio.id,
        'title': audio.title,
        'duration': audio.duration,
        'author': audio.author.name,
        'thumbnailUrl': audio.author.thumbnailUrl,
        'audioUrl': audio.audioUrl,
        'listenCount': audio.listen_count,
        'votes': audio.votes,
    }
    return audio_dict