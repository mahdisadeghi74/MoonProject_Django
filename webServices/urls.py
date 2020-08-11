from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from webServices.views import mytest, register, createLabel, getLabels, getCategories, getHistories, getStories, \
    createStory, getTypes, likeStory, createStoryBranch, updateJoinUser, joinStory, getAllJoinStoriesRequest, \
    submitMergeRequestStory, comparisonTwoStories, mergeRequestStory

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', register, name='register'),
    path('createLabel/', createLabel, name='createLabel'),
    path('getLabels/', getLabels, name='getLabels'),
    path('getCategories/', getCategories, name='getCategories'),
    path('getHistories/', getHistories, name='getHistories'),
    path('getStories/', getStories, name='getStories'),
    path('createStory/', createStory, name='createStory'),
    path('getTypes/', getTypes, name='getTypes'),
    path('likeStory/', likeStory, name='likeStory'),
    path('createStoryBranch/', createStoryBranch, name='createStoryBranch'),
    path('updateJoinUser/', updateJoinUser, name='updateJoinUser'),
    path('joinStory/', joinStory, name='joinStory'),
    path('getAllJoinStoriesRequest/', getAllJoinStoriesRequest, name='getAllJoinStoriesRequest'),
    path('mergeRequestStory/', mergeRequestStory, name='mergeRequestStory'),
    path('comparisonTwoStories/', comparisonTwoStories, name='comparisonTwoStories'),
    path('submitMergeRequestStory/', submitMergeRequestStory, name='submitMergeRequestStory'),
]