from django import forms


class RatingForm(forms.Form):
    ratingValue=forms.IntegerField(min_value=1,max_value=5)

    def clean_userId(self):
        userID=self.cleaned_data.get('userId')
        return userID

    def clean_movieID(self):
        movieID=self.cleaned_data.get('movieId')
        return movieID
    def clean_ratingValue(self):
        ratingValue=self.cleaned_data.get('ratingValue')
        return ratingValue
    def clean_movieName(self):
        movieName=self.cleaned_data.get('movieName')
        return movieName

class CreateGroupForm(forms.Form):

    username=forms.CharField()

    def clean_username(self):
        username=self.cleaned_data.get('username')
        return username
