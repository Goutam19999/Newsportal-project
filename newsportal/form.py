from django import forms
from newsportal.models import Comment, Contact , NewsLetter, Post
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"

class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = "__all__"      


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields =['title','content']        