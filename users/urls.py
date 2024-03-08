from django.urls import path
from .views import Register, Login, ViewUser, Logout, CreatePeriodDetail, PredictNextPeriod, RetrievePeriodsData, AnalyzeSymptoms

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('user', ViewUser.as_view()),
    path('logout', Logout.as_view()),
    path('createPeriodDetail', CreatePeriodDetail.as_view()),
    path('retrievePeriodsData', RetrievePeriodsData.as_view()),
    path('predictNextPeriod', PredictNextPeriod.as_view()),
    path('analyzeSymptoms', AnalyzeSymptoms.as_view())
]