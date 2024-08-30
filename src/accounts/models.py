from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission
)
from django.core.validators import RegexValidator

# UserManager : Gère la création des utilisateurs et super-utilisateurs.
class UserManager(BaseUserManager):
    # Méthode pour créer un utilisateur standard.
    def create_user(self, email, username, first_name, last_name, gender, password=None):
        """
        Crée et enregistre un utilisateur avec l'email, le nom d'utilisateur,
        le prénom, le nom de famille, le genre, et un mot de passe.
        """
        # Vérifie si l'email est fourni.
        if not email:
            raise ValueError('Users must have an email address')

        # Vérifie si le nom d'utilisateur est fourni.
        if not username:
            raise ValueError('Must have username')

        # Vérifie que le mot de passe contient au moins 8 caractères.
        if len(password) < 8:
            raise ValueError('Password must be over 8 characters')

        # Crée un nouvel utilisateur avec les informations fournies.
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
        )

        # Définit le mot de passe pour l'utilisateur.
        user.set_password(password)
        # Enregistre l'utilisateur dans la base de données.
        user.save(using=self._db)
        return user

    # Méthode pour créer un super-utilisateur (admin).
    def create_superuser(self, email, username, first_name, last_name, gender, password=None):
        """
        Crée et enregistre un super-utilisateur avec l'email, le nom d'utilisateur,
        le prénom, le nom de famille, le genre, et un mot de passe.
        """
        # Appelle la méthode create_user pour créer un utilisateur standard.
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            gender,
            password=password,
        )
        # Attribue les privilèges d'admin au super-utilisateur.
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        # Enregistre le super-utilisateur dans la base de données.
        user.save(using=self._db)
        return user


# Définition d'une regex pour valider les noms d'utilisateur.
USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


# NewUser : Modèle personnalisé d'utilisateur.
class NewUser(PermissionsMixin, AbstractBaseUser):
    # GENDER : Choix pour le genre de l'utilisateur.
    class GENDER(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    # Champs du modèle utilisateur.
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=125,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be alphanumeric or contain any of the following: ". @ + -"',
                code='invalid_username'
            ),
        ],
        unique=True
    )
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    id_image = models.ImageField(upload_to="id-images/", null=True, blank=True)
    country = models.CharField(max_length=125, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER.choices)
    phone_number = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Champs de statut de l'utilisateur.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Utilisation du UserManager personnalisé pour ce modèle.
    objects = UserManager()

    # Spécifie que l'email est utilisé pour se connecter.
    USERNAME_FIELD = 'email'
    # Champs obligatoires pour l'inscription.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender']

    # Retourne l'email de l'utilisateur comme représentation de l'objet.
    def __str__(self):
        return self.email

    # Retourne le nom complet de l'utilisateur.
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

#####################################################################################
#####################################################################################
#####################################################################################

# from models.py
# add PermissionsMixin
# remove has_perm and has_module_perms

# from admin.py
# fieldsets -> Permissions -> add ('groups', 'user_permissions')
# remove filter_horizontal


# class Profile(models.Model):
#     class STATE_CHOICES(models.TextChoices):
#         MALE = "MA", 'Male'
#         FEMALE = "FA", "Female"

#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField()
#     id_image = models.ImageField(upload_to="id-images/")
#     phone_number = models.IntegerField()
#     status = models.CharField(max_length=6, choices=STATE_CHOICES.choices)

    