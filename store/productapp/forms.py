from django import forms
class UserProfileInfoForm(forms.Form):


	username = forms.CharField(max_length=20,label="Enter UserName:")
	email = forms.EmailField(label="Enter Email")
	password = forms.CharField(widget=forms.PasswordInput,label="Enter Password")

	def __str__(self):
		return self.portfolio_site

class LoginForm(forms.Form):


	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput)

	def __str__(self):
		return self.portfolio_site

class AddProduct(forms.Form):

	pname = forms.CharField(max_length=20,label="Enter Product Name:",widget=forms.TextInput(attrs={'style': 'text-transform: uppercase;'}))
	pid = forms.CharField(max_length=20,label="Enter Product ID:",widget=forms.TextInput(attrs={'style': 'text-transform: uppercase;'}))
	quantity = forms.IntegerField(label="Enter Quantity:")
	price = forms.IntegerField(label="Enter Price:")
	user = forms.IntegerField(lbel="Enter the date on which it filled")

class Search(forms.Form):
	pid = forms.CharField(max_length=20,label="Enter Product ID To Search:")

class SearchByName(forms.Form):
	pname = forms.CharField(max_length=20,label="Enter Product Name To Search:",widget=forms.TextInput(attrs={'style': 'text-transform: uppercase;'}))