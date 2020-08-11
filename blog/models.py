from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
from django.utils import timezone

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("user must have an email address")
        if not username:
            raise ValueError("user must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = False
        user.is_active = True

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True, null=False)
    firstName = models.CharField(verbose_name='firstName', max_length=30, null=True)
    lastName = models.CharField(verbose_name='lastName', max_length=30, null=True)
    username = models.CharField(verbose_name='username', max_length=30, null=False)
    number = models.BigIntegerField(verbose_name='number', null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Category(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30, unique=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30, unique=True)

    created_by = models.ForeignKey(Account, editable=False, null=True, blank=True, on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class JoinStory(models.Model):
    user = models.ForeignKey(Account, verbose_name='Join User', on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)
    isAccepted = models.BooleanField(default=False)


    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

class Story(models.Model):
    title = models.CharField(verbose_name='Title', max_length=60)
    content = models.TextField(verbose_name='Content')
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    label = models.ManyToManyField(Label, verbose_name='Label')
    members = models.ManyToManyField(JoinStory, related_name='members')
    branch = models.CharField(verbose_name='Branch Name', max_length=30)
    isPrivate = models.BooleanField(verbose_name='Is Private', default=False)
    parent = models.ForeignKey(to='Story', on_delete=models.CASCADE, related_name='parent_story', null=True, blank=True)
    currentStory = models.ForeignKey(to='Story', on_delete=models.CASCADE, related_name='current_story', null=True, blank=True)
    #find add this record

    created_by = models.ForeignKey(Account, editable=False, null=True, blank=True, on_delete=models.CASCADE)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(verbose_name='content')
    story = models.ForeignKey(Story, verbose_name='Story', on_delete=models.CASCADE)
    user = models.ForeignKey(Account, verbose_name='User', on_delete=models.CASCADE)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.content


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, verbose_name='content', on_delete=models.CASCADE)
    user = models.ForeignKey(Story, verbose_name='Story', on_delete=models.CASCADE)
    clap = IntegerRangeField(verbose_name='clap', max_value=1, min_value=0)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class LikeStory(models.Model):
    story = models.ForeignKey(Story, verbose_name='Story', on_delete=models.CASCADE)
    user = models.ForeignKey(Account, verbose_name='User', on_delete=models.CASCADE)
    clap = IntegerRangeField(verbose_name='Clap', max_value=50, min_value=0)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Type(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30, unique=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class history(models.Model):
    story = models.ForeignKey(Story, verbose_name='Story', on_delete=models.CASCADE, related_name='base_story')
    user = models.ForeignKey(Account, verbose_name='User', on_delete=models.CASCADE)
    type = models.ForeignKey(Type, verbose_name='type', on_delete=models.CASCADE)

    currentStory = models.ForeignKey(Story, verbose_name='Current Story', on_delete=models.CASCADE, related_name='current')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


