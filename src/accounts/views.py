from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.contrib import messages
from twilio.rest import Client
from core.env import config

from .forms import RegisterForm, UserCreationForm
from .detection import FaceRecognition
from .tasks import send_email

User = get_user_model()  # Obtient le modèle utilisateur personnalisé utilisé dans le projet.
faceRecognition = FaceRecognition()  # Initialise une instance de la classe FaceRecognition.


# Vue pour la page d'accueil des comptes.
def accounts_home(request):
    context = {}
    return render(request, "home.html", context)  # Rend la page d'accueil avec le contexte vide.


# Vue pour la page d'inscription des utilisateurs.
def accounts_register(request):
    form = UserCreationForm(request.POST or None, request.FILES or None)  # Crée une instance du formulaire d'inscription.
    
    if form.is_valid():  # Vérifie si le formulaire est valide.
        new_user = form.save(commit=False)  # Sauvegarde l'utilisateur sans encore le committer dans la base de données.
        new_user.save()  # Sauvegarde l'utilisateur dans la base de données.
        
        face_id = new_user.id  # Récupère l'identifiant de l'utilisateur pour la reconnaissance faciale.
        phone_number = new_user.phone_number  # Récupère le numéro de téléphone de l'utilisateur.
        
        # Reconnaissance faciale.
        faceRecognition.faceDetect(face_id)  # Détecte le visage et l'associe à l'identifiant utilisateur.
        faceRecognition.trainFace()  # Entraîne le modèle de reconnaissance faciale.

        # # Envoi de message SMS (commenté).
        # if phone_number is not None:
        #     account_sid = config('PHONE_ACCOUNT_SID', default=None)
        #     auth_token = config('PHONE_AUTH_TOKEN', default=None)
        #     client = Client(account_sid, auth_token)
        #     message = client.messages.create(
        #         body="Hello there.",
        #         from_=config("PHONE_FROM", default=None),
        #         to=f'+216{phone_number}'
        #     )
        
        # # Envoi d'email (commenté).
        # _title = f"Hello {new_user.username}"
        # email = new_user.email
        # title = _title
        # send_email.delay(title, email)

        return redirect("accounts:login")  # Redirige l'utilisateur vers la page de connexion après l'inscription.

    context = {
        "form": form,  # Passe le formulaire dans le contexte pour être utilisé dans le template.
    }
    return render(request, "accounts/register.html", context)  # Rend la page d'inscription avec le contexte.


# Vue pour afficher la page de connexion.
def accounts_login_page(request):
    return render(request, "accounts/login.html", {})  # Rend la page de connexion.


# Vue pour traiter la connexion des utilisateurs.
def accounts_login(request):
    face_id = faceRecognition.recognizeFace()  # Reconnaît le visage de l'utilisateur et retourne l'identifiant correspondant.

    try:
        user = get_object_or_404(User, id=face_id)  # Recherche l'utilisateur avec l'identifiant retourné par la reconnaissance faciale.
        login(request, user)  # Connecte l'utilisateur s'il est trouvé.
        return redirect("accounts:home")  # Redirige vers la page d'accueil des comptes.
    except:
        messages.error(request, "You don't have an account, Create new account")  # Affiche un message d'erreur si l'utilisateur n'existe pas.
        return redirect("accounts:register")  # Redirige vers la page d'inscription.


# Vue pour déconnecter les utilisateurs.
def accounts_logout(request):
    logout(request)  # Déconnecte l'utilisateur actuel.
    return redirect("accounts:login")  # Redirige vers la page de connexion.
