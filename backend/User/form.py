from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128)
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class FindPasswordBackForm_FS(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class FindPasswordBackForm_SE(forms.Form):
    password_1 = forms.CharField(label="密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    code = forms.CharField(label="验证码", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ChangeEmailForm_FS(forms.Form):
    old_email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    new_email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class ChangeEmailForm_SE(forms.Form):
    old_email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    new_email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    code = forms.CharField(label="验证码", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))



class ChangeUserNameForm(forms.Form):
    old_username = forms.CharField(label="旧用户名", max_length=128)
    new_username = forms.CharField(label='新用户名', max_length=128)

class ChangePictureForm(forms.Form):
    url = forms.CharField(label="头像地址", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))