from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib import messages
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Reteta
from .serializers import RecipeSerializer

def homepage(request):

    return render(request, 'homepage.html', {
        "user" : request.user
    })

def contactpage(request):

    return render(request, 'contactpage.html', {
        'content': 'This is the contact page'
    })

def loginview(request):

    return render(request, 'login.html', {

    })

class RecipeView(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get_object(self, recipe_id, user_id):
        try:
            return Reteta.objects.get(name=recipe_id, owner=user_id)
        except Reteta.DoesNotExist:
            return None

    def get(self, request, recipe_id=None, *args, **kwargs):
        if recipe_id:
            try:
                recipe_instance = Reteta.objects.get(id=recipe_id)
                serializer = RecipeSerializer(recipe_instance)
            except Reteta.DoesNotExist:
                raise Http404("Recipe does not exist")
        else:
            retete = Reteta.objects.all()
            serializer = RecipeSerializer(retete, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # 2. Create
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'accounts': request.data.get('accounts'),
            'ingredients': request.data.get('ingredients'),
            'text': request.data.get('text'),
            'timp': request.data.get('timp'),
            'owner': request.user.id
        }
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def put(self, request, recipe_id, *args, **kwargs):
        recipe_instance = self.get_object(recipe_id, request.user.id)
        if not recipe_instance:
            return Response({"res": "Object with recipe id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        serializer = RecipeSerializer(instance=recipe_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        recipe_instance = self.get_object(request.data.get("name"), request.user.id)
        if not recipe_instance:
            return Response({"res": "Object with recipe id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        recipe_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)


# class LoginView(APIView):
#     def post(request):
#         if request.method == 'POST':
#             form = AuthenticationForm(request, data=request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     token, created = Token.objects.get_or_create(user=user)
#                     response = redirect('homepage')
#                     response.set_cookie(
#                         'auth_token',
#                         token.key,
#                         httponly=True,
#                         secure=True,
#                         samesite='Lax'
#                     )
#                     return render(request, 'homepage.html')
#                 else:
#                     messages.error(request, "Invalid username or password.")
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})


@login_required()
def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000')

def loginview2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('http://127.0.0.1:8000')
    return render(request, 'login.html')


@login_required()
def show_recipes(request):
    return render(request, 'recipes_list.html', {'user': request})  # Pass data to the template