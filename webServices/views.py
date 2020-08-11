from django.db.models import Q
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blog.models import Label, Category, history, Story, Type, Account, LikeStory, JoinStory
from blog.serializers import RegistrationSerializer, LabelSerializer, CategorySerializer, historySerializer, \
    StorySerializer, TypeSerializer, JoinStorySerializer

import difflib
def mytest(request):
    return HttpResponse(request.method)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny,))
@csrf_exempt
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()

        data['email'] = account.email
        data['firstName'] = account.firstName
        data['lastName'] = account.lastName
        data['is_active'] = account.is_active
        data['is_superuser'] = account.is_superuser
        data['is_staff'] = account.is_staff
        data['username'] = account.username
        data['pk'] = account.pk
        data['is_admin'] = account.is_admin

    else:
        data = serializer.errors

    return Response(data)


################# label #########################
@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def createLabel(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    name = request.POST.get('name')

    try:
        label = Label.objects.create(name=name, created_by=user)
    except:
        raise serializers.ValidationError({'error': 'have a problem'})

    serializerData = LabelSerializer(label).data
    return Response(serializerData)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def getLabels(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    search = request.POST.get('search')

    try:
        labels = Label.objects.filter(name__istartswith=search)
    except:
        raise serializers.ValidationError({'error': 'have a problem'})

    serializersData = []

    for l in labels:
        serializersData.append(LabelSerializer(l).data)

    return Response(serializersData)


################# catagory #########################
@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def getCategories(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user

    try:
        categories = Category.objects.all()
    except:
        raise serializers.ValidationError({'error': 'have a problem'})

    serializersData = []

    for c in categories:
        serializersData.append(CategorySerializer(c).data)

    return Response(serializersData)


################# history #########################
@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def getHistories(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    type = request.POST.get('typeId')
    story = request.POST.get('storyId')
    currentStory = request.POST.get('currentStory')

    filters = {'user': user}
    if type is not None:
        filters['type'] = type
    if story is not None:
        filters['story'] = story
    if currentStory is not None:
        filters['currentStory'] = currentStory

    try:
        histories = history.objects.filter(**filters)
    except:
        raise serializers.ValidationError({'error': 'have a problem'})

    serializersData = []

    for h in histories:
        serializersData.append(historySerializer(h).data)

    return Response(serializersData)


################# story #########################
@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def getStories(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    id = request.POST.get('id')
    title = request.POST.get('title')
    content = request.POST.get('content')
    category = request.POST.get('category')
    label = request.POST.getlist('label')
    branch = request.POST.get('branch')
    isPrivate = request.POST.get('isPrivate')
    currentStory = request.POST.get('currentStory')
    created_by = request.POST.get('created_by')
    search = request.POST.get('search')
    parent = request.POST.get('parent')
    filters={}
    if id is not None and id != '':
        filters['id'] = id
    if title is not None:
        filters['title'] = title
    if content is not None:
        filters['content'] = content
    if category is not None:
        filters['category'] = category
    if label is not None and len(label) > 0:
        print(len(label))
        filters['label__in'] = label
    if branch is not None:
        filters['branch'] = branch
    if isPrivate is not None:
        filters['isPrivate'] = isPrivate
    if currentStory is not None:
        filters['currentStory'] = currentStory
    if created_by is not None:
        filters['created_by'] = created_by
    if parent is not None and parent != '' :
        filters['parent'] = parent
    # try:
    if search is None:
        stories = Story.objects.filter(**filters)
    else:
        if search is not None:
            stories = Story.objects.filter(**filters).\
                filter(Q(title__icontains=search) | Q(content__icontains=search))

    # except:
    #     raise serializers.ValidationError({'error': 'have a problem'})

    serializersData = []

    for s in stories:
        story = StorySerializer(s).data
        # category
        category = Category.objects.filter(pk=s.category_id)
        try:
            story['category'] = CategorySerializer(category[0]).data
        except:
            story['category'] = CategorySerializer(s.category_id).data

        ## label
        labelList =[]
        for l in story['label']:
            label = Label.objects.filter(pk=l)
            labelList.append(LabelSerializer(label[0]).data)

        story['label'] = labelList

        try:
            story['created_by'] = Account.objects.filter(pk=s.created_by_id)[0].username
        except: pass

        try:
            storyLikes = LikeStory.objects.filter(story=s)
            likeCounts = 0
            for like in storyLikes:
                likeCounts += like.clap
            story['clapCount'] = likeCounts
        except: story['clapCount'] = 0

        serializersData.append(story)

    return Response(serializersData)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def createStory(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})



    user = request.user
    title = request.POST.get('title')
    content = request.POST.get('content')
    category = request.POST.get('category')
    label = request.POST.getlist('label')
    branch = request.POST.get('branch')
    isPrivate = request.POST.get('isPrivate')
    type = request.POST.get('type')
    currentStory = request.POST.get('currentStory')
    created_by = user

    story = createStoryFunction(title, content, category, branch, isPrivate, currentStory, label, created_by)
        #  newHistory = history.objects.create(story=story, user=user, type=type, currentStory=currentStory)
    serializerData = []
    sStory = StorySerializer(story).data

    category = Category.objects.filter(pk=story.category_id)

    try:
        sStory['category'] = CategorySerializer(category[0]).data
    except:
        sStory['category'] = CategorySerializer(story.category_id).data

    labelList = []
    for l in sStory['label']:
        label = Label.objects.filter(pk=l)
        labelList.append(LabelSerializer(label[0]).data)

    sStory['label'] = labelList

    try:
        sStory['created_by'] = Account.objects.filter(pk=story.created_by_id)[0].username
    except:
        pass

    try:
        storyLikes = LikeStory.objects.filter(story=story)
        likeCounts = 0
        for like in storyLikes:
            likeCounts += like.clap
        sStory['clapCount'] = likeCounts
    except:
        sStory['clapCount'] = 0

    serializerData.append(sStory)

    return Response(serializerData[0])
    # except:
    #     raise serializers.ValidationError({'error': 'have a problem'})


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def createStoryBranch(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})


    label = []
    user = request.user
    storyId = request.POST.get('storyId')
    branch = request.POST.get('branch')

    stories = Story.objects.filter(pk=storyId)
    if len(stories) > 0:
        story = stories[0]
    else:
        raise serializers.ValidationError({'error': 'story is wrong'})


    branches = Story.objects.filter(Q(pk=storyId, branch=branch) | Q(parent=storyId, branch=branch))
    if len(branches) > 0:
        raise serializers.ValidationError({'error': 'branch name is exist'})

    parameters = {}
    if story.title is not None:
        parameters['title'] = story.title
    else:
        raise serializers.ValidationError({'error', 'please enter title'})
    if story.content is not None:
        parameters['content'] = story.content
    else:
        raise serializers.ValidationError({'error', 'please enter content'})
    if story.category is None:
        raise serializers.ValidationError({'error', 'category not found'})
    else:
        parameters['category'] = story.category

    if branch is not None:
        parameters['branch'] = branch
    else:
        raise serializers.ValidationError({'error', 'please enter branch'})
    if story.isPrivate is not None:
        parameters['isPrivate'] = story.isPrivate


    if storyId is not None and storyId!= '':
        parameters['parent'] = story
    parameters['created_by'] = user

    branchStory = Story.objects.create(**parameters)

    if story.label is not None:
        parameters['label'] = label
        branchStory.label.set(label)

        branchStory.save()

  #  newHistory = history.objects.create(story=story, user=user, type=type, currentStory=currentStory)
    serializerData = []
    sStory = StorySerializer(branchStory).data

    category = Category.objects.filter(pk=branchStory.category_id)

    try:
        sStory['category'] = CategorySerializer(category[0]).data
    except:
        sStory['category'] = CategorySerializer(branchStory.category_id).data

    labelList = []
    for l in sStory['label']:
        label = Label.objects.filter(pk=l)
        labelList.append(LabelSerializer(label[0]).data)

    sStory['label'] = labelList

    try:
        sStory['created_by'] = Account.objects.filter(pk=branchStory.created_by_id)[0].username
    except:
        pass

    try:
        storyLikes = LikeStory.objects.filter(story=branchStory)
        likeCounts = 0
        for like in storyLikes:
            likeCounts += like.clap
        sStory['clapCount'] = likeCounts
    except: sStory['clapCount'] = 0

    serializerData.append(sStory)


    return Response(serializerData[0])


################# type #########################
@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def getTypes(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user

    try:
        types = Type.objects.all()
    except:
        raise serializers.ValidationError({'error': 'have a problem'})

    serializersData = []

    for t in types:
        serializersData.append(TypeSerializer(t).data)

    return Response(serializersData)


################# type #########################
@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def likeStory(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    storyId = request.POST.get('storyId')
    clap = request.POST.get('clap')

    # try:
    story = Story.objects.filter(pk=storyId)
    if story:
        likeStory = LikeStory.objects.filter(user=user, story=story[0])
        if likeStory:
            if likeStory[0].clap + int(clap) <= 50:
                likeStory[0].clap = likeStory[0].clap + int(clap)
            else:
                likeStory[0].clap = 50
            likeStory[0].save()
        else:
            LikeStory.objects.create(story=story[0], user=user, clap=clap)
    # except:
    #     raise serializers.ValidationError({'error': 'have a problem'})

    serializersData = []

    likeStory = LikeStory.objects.filter(user=user, story=story[0])

    return Response({'clap': likeStory[0].clap})

@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def joinStory(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    storyId = request.POST.get('storyId')

    story = Story.objects.filter(pk=storyId)

    if len(story) == 0:
        raise serializers.ValidationError({'error': 'story not exist'})

    joinStories = story[0].members.filter(user = user)

    if len(joinStories) > 0:
        raise serializers.ValidationError({'error': 'you before joined'})

    joinStory = JoinStory.objects.create(user=user)
    story[0].members.add(joinStory)
    return Response({'result': 'Delivered'})

@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def updateJoinUser(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    storyId = request.POST.get('storyId')
    id = request.POST.get('id')
    memberId = request.POST.get('memberId')
    isActive = request.POST.get('isActive')
    isAccepted = request.POST.get('isAccepted')

    story = Story.objects.filter(pk=storyId)

    if len(story) == 0:
        raise serializers.ValidationError({'error': 'story not exist'})


    if user == story[0].created_by:
        joinStory = JoinStory.objects.get(pk=id)
        joinStory.isAccepted = isAccepted == "true"
        joinStory.save()

    return Response(JoinStorySerializer(JoinStory.objects.filter(pk=id)[0]).data)

@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def getAllJoinStoriesRequest(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    storyId = request.POST.get('storyId')

    story = Story.objects.filter(pk=storyId)
    if len(story) == 0:
        raise serializers.ValidationError({'error': 'story not exist'})

    members = []
    if user == story[0].created_by:
        members = story[0].members.filter(Q(isAccepted=False) | Q(isAccepted=True))

    serializersData =[]

    for m in members:
        member = JoinStorySerializer(m).data

        member['userName'] = m.user.username
        serializersData.append(member)

    return Response(serializersData)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def mergeRequestStory(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    storyId = request.POST.get('storyId')
    storyContentNew = request.POST.get('storyContentNew')

    story = Story.objects.filter(pk=storyId)

    if len(story) == 0:
        raise serializers.ValidationError({'error': 'story not exist'})

    storyContentOld = story[0].content
    add = []
    delete = []
    for i,s in enumerate(difflib.ndiff(storyContentOld, storyContentNew)):
        if s[0]==' ': continue
        elif s[0]=='-':
            delete.append(getOldPosition(i, add))
        elif s[0]=='+':
            add.append(i)

    story = createStoryFunction(story[0].title, storyContentNew, story[0].category.id, story[0].branch, story[0].isPrivate, story[0].currentStory, story[0].label.all(), user, parent=storyId)
        #  newHistory = history.objects.create(story=story, user=user, type=type, currentStory=currentStory)
    serializerData = []
    sStory = StorySerializer(story).data

    category = Category.objects.filter(pk=story.category_id)

    try:
        sStory['category'] = CategorySerializer(category[0]).data
    except:
        sStory['category'] = CategorySerializer(story.category_id).data

    labelList = []
    for l in sStory['label']:
        label = Label.objects.filter(pk=l)
        labelList.append(LabelSerializer(label[0]).data)

    sStory['label'] = labelList

    try:
        sStory['created_by'] = Account.objects.filter(pk=story.created_by_id)[0].username
    except:
        pass

    try:
        storyLikes = LikeStory.objects.filter(story=story)
        likeCounts = 0
        for like in storyLikes:
            likeCounts += like.clap
        sStory['clapCount'] = likeCounts
    except:
        sStory['clapCount'] = 0

    serializerData.append(sStory)

    return Response(serializerData[0])


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def comparisonTwoStories(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    storyId = request.POST.get('storyId')

    story1 = Story.objects.filter(pk=storyId)

    if len(story1) == 0:
        raise serializers.ValidationError({'error': 'story not exist'})

    story2 = Story.objects.filter(pk=story1[0].parent.id)
    storyContentNew = story1[0].content
    storyContentOld = story2[0].content

    add = []
    delete = []
    for i,s in enumerate(difflib.ndiff(storyContentOld, storyContentNew)):
        if s[0]==' ': continue
        elif s[0]=='-':
            delete.append(getOldPosition(i, add))
        elif s[0]=='+':
            add.append(i)


    return Response({'storyContentNew': storyContentNew, 'storyContentOld': storyContentOld, 'add': add, 'delete': delete})


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@csrf_exempt
def submitMergeRequestStory(request):
    if request.method != "POST":
        raise serializers.ValidationError({'error': 'your request method not POST'})

    user = request.user
    storyId = request.POST.get('storyId')
    storyCountent = request.POST.get('storyContent')


    story1 = Story.objects.filter(pk=storyId)

    if len(story1) == 0:
        raise serializers.ValidationError({'error': 'story not exist'})

    if story1[0].created_by != user:
        raise serializers.ValidationError({'error': 'this user can not access this story'})


    story1[0].content = storyCountent
    story1[0].save()

    story2 = story1[0].parent
    story2.currentStory = Story.objects.get(pk=storyId)
    story2.save()

    serializerData = []
    sStory = StorySerializer(story2).data

    category = Category.objects.filter(pk=story2.category_id)

    try:
        sStory['category'] = CategorySerializer(category[0]).data
    except:
        sStory['category'] = CategorySerializer(story2.category_id).data

    labelList = []
    for l in sStory['label']:
        label = Label.objects.filter(pk=l)
        labelList.append(LabelSerializer(label[0]).data)

    sStory['label'] = labelList

    try:
        sStory['created_by'] = Account.objects.filter(pk=story2.created_by_id)[0].username
    except:
        pass

    try:
        storyLikes = LikeStory.objects.filter(story=story2)
        likeCounts = 0
        for like in storyLikes:
            likeCounts += like.clap
        sStory['clapCount'] = likeCounts
    except:
        sStory['clapCount'] = 0

    serializerData.append(sStory)

    return Response(serializerData[0])


def getOldPosition(position, addArray):
    res = 0
    for p in addArray:
        if p < position:
            res += 1
        else:
            return position - res

    return position - res

def createStoryFunction(title, content, category, branch, isPrivate, currentStory, label, created_by, parent = None):
    parameters = {}
    if title is not None:
        parameters['title'] = title
    else:
        raise serializers.ValidationError({'error', 'please enter title'})
    if content is not None:
        parameters['content'] = content
    else:
        raise serializers.ValidationError({'error', 'please enter content'})
    if category is not None:
        c = Category.objects.filter(pk=category)
        if len(c) == 0:
            raise serializers.ValidationError({'error', 'category not found'})
        else:
            parameters['category'] = c[0]

    if branch is not None:
        parameters['branch'] = branch
    else:
        raise serializers.ValidationError({'error', 'please enter branch'})
    if isPrivate is not None:
        parameters['isPrivate'] = isPrivate
    if currentStory is not None and currentStory != '':
        parameters['currentStory'] = Story.objects.filter(pk=currentStory)

    if parent is not None:
        parameters['parent'] = Story.objects.get(pk=parent)

    parameters['created_by'] = created_by

    # try:
    story = Story.objects.create(**parameters)
    if label is not None:
        parameters['label'] = label
        for l in label:
            resultLabel, isCreate = Label.objects.get_or_create(name=l)
            story.label.add(resultLabel)

        story.save()

    return story