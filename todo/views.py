from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo

# Create your views here.

'''Function for home page'''


def home(request):
	return render(request, 'todo/home.html')


'''Function for user creation'''


def signup_user(request):
	if request.method == 'GET':
		return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('current_todos')
			except IntegrityError:
				return render(request, 'todo/signup_user.html',
							  {'form': UserCreationForm,
							   'error': 'That username is already used. Please choose another username'})
		else:
			# Error passwords
			return render(request, 'todo/signup_user.html',
						  {'form': UserCreationForm, 'error': 'Passwords did not match'})


'''Function for login'''


def login_user(request):
	if request.method == 'GET':
		return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'todo/login_user.html',
						  {'form': AuthenticationForm(), 'error': 'Invalid username or password'})
		else:
			login(request, user)
			return redirect('current_todos')


'''Function for logout'''


@login_required
def logout_user(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')


'''Function for creating todos'''


@login_required
def create_todo(request):
	if request.method == 'GET':
		return render(request, 'todo/create_todo.html', {'form': TodoForm()})
	else:
		try:
			form = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('current_todos')
		except ValueError:
			return render(request, 'todo/create_todo.html', {'form': TodoForm(), 'error': 'Bad data passed in'})


'''Function to display page with todos'''


@login_required
def current_todos(request):
	todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
	return render(request, 'todo/current_todos.html', {'todos': todos})


'''Function for completed todos'''


@login_required
def completed_todos(request):
	todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
	return render(request, 'todo/completed_todos.html', {'todos': todos})


'''Function for certain todo'''


@login_required
def view_todo(request, todo_pk):
	certain_todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method == 'GET':
		form = TodoForm(instance=certain_todo)
		return render(request, 'todo/view_todo.html', {'certain_todo': certain_todo, 'form': form})
	else:
		try:
			form = TodoForm(request.POST, instance=certain_todo)
			form.save()
			return redirect('current_todos')
		except ValueError:
			return render(request, 'todo/view_todo.html', {'form': TodoForm(), 'error': 'Bad info'})


'''Function for complete todo'''


@login_required
def complete_todo(request, todo_pk):
	certain_todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method == "POST":
		certain_todo.datecompleted = timezone.now()
		certain_todo.save()
		return redirect('current_todos')


'''Function for delete todo'''


@login_required
def delete_todo(request, todo_pk):
	certain_todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method == 'POST':
		certain_todo.delete()
		return redirect('current_todos')
