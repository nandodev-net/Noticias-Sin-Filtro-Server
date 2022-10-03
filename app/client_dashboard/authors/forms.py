from app.audio_player.models import Author
from bootstrap_modal_forms.forms import BSModalModelForm

class AuthorModelForm(BSModalModelForm):
    class Meta:
        model = Author
        fields = ['name', 'description' , 'thumbnailUrl', 'type']