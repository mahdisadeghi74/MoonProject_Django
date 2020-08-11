from rest_framework import serializers

from blog.models import Account, Story, Label, Category, history, Type, JoinStory


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username',
                  'email','password', 'password2']
        extra_kwarg = {
            'password': {'write_only': True}
        }


    def save(self):
        account = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'passwords must match'})

        account.set_password(password)
        account.save()
        return account


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = [
            'id',
            'name',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'name',]

class StorySerializer(serializers.ModelSerializer):
    # c = Category.objects.get(pk=1)
    # cat = CategorySerializer(c, source='*').data

    class Meta:
        model = Story
        fields = ['id',
            'title',
            'content',
            'category',
            'label',
            'branch',
            'parent',
            'currentStory',
            'created_by',
        ]

class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = [
            'id',
            'name', ]


class historySerializer(serializers.ModelSerializer):

    class Meta:
        model = history
        fields = [
            'id',
            'story',
            'user',
            'type',
            'currentStory',
        ]

class JoinStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinStory
        fields = [
            'id',
            'user',
            'isActive',
            'isAccepted',
        ]

