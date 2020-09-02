from django.shortcuts import render
from main.forms import *
from main.models import *
from django.views.generic import View
from django.shortcuts import redirect
# from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

# Create your views here.

#это пакеты аутентификации
from django.contrib.auth.forms import AuthenticationForm
from urllib.parse import urlparse#разделяет наш полученный адрес по полычкам
from django.contrib.auth import logout# это выход, готовая функция
from django.contrib import messages # success, info, warning, error, debug mehagess
from django.contrib.auth.decorators import login_required#декоратор огроничения доступа
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin# это такойже декоратор как - login_required, только работает с классами
from django.contrib import auth
from django.contrib.auth import get_user_model#получаем данные User
#это пакет готовый набор новый регистрации пользователя
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

#Этот процессор добавляет токен, который используется тегом csrf_token для защиты от CSRF атак.
from django.template.context_processors import csrf



def index(request):
	return render(request, 'index.html')

class SignUpView(CreateView):
	template_name = 'regist/signup.html'
	form_class = CaseInsensitiveUserCreationForm
	profile_form = UserProfileForm()#дополнительное рассширение Пользователя(age, location)

	def get_context_data(self, **kwargs):# все элементы контекста
		context = {}
		context = super(SignUpView, self).get_context_data(**kwargs)#этод метод отправляет все контексты главного класса в шаблон
		context['profile_form'] = self.profile_form #это дополнительный контекст расширение Пользователя 
		return context
		
	def form_valid(self, form):
		profile_form = UserProfileForm(self.request.POST)

		# проверка валидности reCAPTCHA и дополнительное рассширение Пользователя(age, location)
		if profile_form.is_valid():

			user = form.save()
			profile = profile_form.save(commit=False)# Create, but don't save the new profile instance.
			profile.user = user
			profile.save()#данные сохроняются в админ панели в User profiles
			form.save()

			messages.success(self.request, 'Your password was created successfully!')
			return render(self.request, 'regist/signup_success.html', self.get_context_data())

		messages.warning(self.request, 'You need repeat again')
		return render(self.request, 'regist/signup.html', self.get_context_data())


# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
	context = {} #создаем пустой контекст	
	context.update(csrf(request)) #впихиваем в контекст токен
	context['form'] = AuthenticationForm #добовляем пустые формы аутентификации
	return context


class MyLoginView(View):

	
	def get(self, request):
			

			if auth.get_user(request).is_authenticated:
				#замечание здесь нету токена!!!!!!!!!!
				print('сработал get')
				#здесь я вывожу имя пользователя с помощью messages
				User = auth.get_user(request)
				messages.success(request, "Welkome %s!" % User)


				return redirect('addres_url')#переходим на тот адрес где мы изночально были до аутентификации
			else:
				context = create_context_username_csrf(request) #загоняем готовую фунцию токен и формы
				return render(request, 'regist/log_widget.html', context=context)
				
	def post(self, request, *args, **kwargs):

		# получив запрос на авторизацию
		form = AuthenticationForm(request, data=request.POST)
		
        # проверяем правильность формы, что есть такой пользователь
        # и он ввёл правильный пароль
		if form.is_valid():
			
            # в случае успеха авторизуем пользователя
			auth.login(request, form.get_user())

			# и если пользователь из числа персонала и заходил через url /admin/login/
			# то перенаправляем пользователя в админ панель
			if request.user.is_staff:
			    return redirect('/admin/')

			return redirect('addres_url')

		context = create_context_username_csrf(request)
		context['form'] = form
		return render(request, 'regist/log_widget.html', context=context)

def myLogout(request):
	logout(request)
	messages.info(request, "Logged out successfully!")#message с использованием шаблона

	return redirect('index_url')


class AddresView(View):

	def get(self, request):
		address = Address.objects.all()
		form = AddressForm()
		context = {
			'address' : address,
			'form' : form,
		}
		return render(request, 'addres.html', context = context)

	def post(self, request):
		
		form = AddressForm(request.POST)
		print(form)
		if form.is_valid():
			form.save()
			print('success')
			return redirect('addres_url')		
		
		#return render(request, 'addres.html', context = {'form': form })
		return redirect('addres_url')