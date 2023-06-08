from django.urls import path
from fridge.views import *
from uaa import views

#paths for account app.
urlpatterns = [
    path('', views.LoginView, name='login_url'),
    path('register/',views.RegisterView, name="register_url"),
    path('resetpassword/', views.ResetPasswordView, name='resetpassword_url'),
    path('RecoverPassword/<str:email>', views.RecoverPasswordView, name='RecoverPassword_url'),
    
    path('dashboard/', deviceMapView, name='dashboard_url'),
    path('profile/', views.ProfileView, name='profile_url'),  
    path('updateProfile', views.UpdateProfileView, name='updateProfile_url'),
    path('updateProfilePic/', views.UpdateProfilePicView, name='updateProfilePic_url'),
    
    path('success/', views.SuccessView, name='success_url'),
    path('tokensend/', views.TokenSendView, name='tokensend_url'),
    path('verify/<auth_token>', views.VerifyView, name='verify_url'),
    path('error/', views.ErrorView, name='error_url'),
    
    path('uaaUserList/', views.UaaUserListView, name='uaaUserList_url'),
    path('createUser/', views.CreateUserView, name='createUser_url'),
    path('updateUser/', views.UpdateUserView, name='updateUser_url'),
    path('userStatusView/', views.UserStatusView, name='userStatusView_url'),
    path('approveUser/', views.ApproveUserView, name='approveUser_url'),
    
    # path('branch/', views.BranchView, name='branch_url'),
    # path('createBranch/', views.CreateBranchView, name='createBranch_url'),
    # path('branchStatus/', views.BranchStatusView, name="branchStatus_url"),
    # path('deleteBranch/<str:pk>', views.DeleteBranchView, name='deleteBranch_url'),
    
    path('logout/',views.LogoutView, name='logout_url'),
]