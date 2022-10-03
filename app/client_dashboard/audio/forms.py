from app.audio_player.models import Audio
from bootstrap_modal_forms.forms import BSModalModelForm

class AudioModelForm(BSModalModelForm):
    class Meta:
        model = Audio
        fields = ['title', 'author' , 'audioUrl']