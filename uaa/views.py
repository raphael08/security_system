from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from uaa.models import Profile,User
from django.contrib.auth import authenticate,login,logout
import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail

# Create your views here.
def LoginView(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('Email')
            password = request.POST.get('Password')
            
            user_instance = User.objects.filter(email=username).first()
            if user_instance is None:
                messages.info(request,'User not found')
                return redirect('login_url')
            
            profile_instance = Profile.objects.filter(user=user_instance).first()
            if not profile_instance.is_verified:
                messages.info(request, 'User not verified')
                return redirect('login_url')
            
            user = authenticate(request, email=username, password=password)
            if user is not None and user.is_active:
                login(request,user)
                messages.success(request, 'Your are now logged in !!')
                return redirect('dashboard_url')
    
            else:
                messages.warning(request, 'Invalid Credentials !!')
                return redirect('login_url')
                
    except Exception as e:
        print(e)
    
    context = {}
    return render(request,"login.html")

def RegisterView(request):
    
    
    try:
        if request.method == 'POST':
            username = request.POST.get('Username')
            email = request.POST.get('Email')
            BranchId = request.POST.get('BranchId')
            password = request.POST.get('Password')
            password1 = request.POST.get('ConfirmPassword')
            
            if User.objects.filter(username=username).first():
                messages.info(request,'Username is already taken')
                return redirect('register_url')
            
            if User.objects.filter(email=email).first():
                messages.info(request,'Email is already taken')
                return redirect('register_url')
            
            if len(username) < 5:
                messages.info(request,'username, atlest 5 characters')
                return redirect('register_url')
            
            if password != password1:
                messages.info(request,'password does not match')
                return redirect('register_url')
            
            if len(password) < 8:
                messages.info(request, 'password, 8 mixed characters required')
                return redirect('register_url')
            
            #Sending email for verification.
            auth_token = str(uuid.uuid4())
            try:
                SendEmailRegister(email, auth_token)
            except:
                messages.info(request, 'Either no internet || Invalid email')
                return redirect('register_url')
            
            #Creating and saving a user to the database.
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            
            #Adding a default role to the registered user.
            grp = Group.objects.get(name="customer")
            user= User.objects.get(username=username)
            user.groups.add(grp)
            
            #creating a user profile.
            profile_obj = Profile.objects.create(user=user_obj, branch_id=BranchId, auth_token=auth_token)
            profile_obj.save()
            
            messages.info(request,'Check your email to verify.')
            return redirect('login_url')
        
    except Exception as e:
        print(e)
    
  
    return render(request,"uaa/register.html")

#A function for sending email for verification.
def SendEmailRegister(email, token):
    
    try:
        subject = 'Your accounts needs to be verified'
        # message = f'Hi verify your account Brone.pythonanywhere.com/verify/{token}'
        message = f'Hi verify your account 127.0.0.1:8000/verify/{token}' #for localhost use.
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message,email_from,recipient_list)
    except Exception as e:
        print(e)
    

#Verify your account.
def VerifyView(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your account is alredy verified')
                return redirect('login_url')
             
            profile_obj.is_verified = True
            profile_obj.save() 
            messages.success(request,'Your account has been verified')
            return redirect('success_url')
        
        else: 
            return redirect('error_url')
    except Exception as e:
        return HttpResponse(e)


def ResetPasswordView(request):
     
    try:
        if request.method == 'POST':
            email = request.POST.get('Email')
            
            user_email_instance = User.objects.filter(email=email).first()
            if user_email_instance is None:
                messages.info(request,'Email does not exist.')
                return redirect('resetpassword_url')
            
            try:
                SendEmailPasswordResetView(email)
            except Exception as e:
                return HttpResponse(e)
            
            messages.info(request,'Check your email, change password.')
            return redirect('login_url')
        
    except Exception as e:
        print(e)
    
    context = {}
    return render(request,"uaa/resetpassword.html")

def SendEmailPasswordResetView(email):
    try:
        subject = 'password reset, click the link below'
        # message = f'Hi verify your account Brone.pythonanywhere.com/RecoverPassword/{email}'
        message = f'Hi verify your account 127.0.0.1:8000/RecoverPassword/{email}' #for local host
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message,email_from,recipient_list)
    except Exception as e:
        print(e)


def RecoverPasswordView(request, email):
    
    try:
        if request.method == 'POST':
            password = request.POST.get('Password')
            confirmPassword = request.POST.get('ConfirmPassword')
            passwordLength = len(password)
            
            userEmailInstance = User.objects.filter(email=email).first()
            if userEmailInstance:
                if password != confirmPassword:
                    messages.info(request, 'password does not match')
                    return redirect('resetpassword_url')
            
                if passwordLength < 8:
                    messages.info(request, 'password is too short')
                    return redirect('resetpassword_url')
                
                userEmailInstance.set_password(password)
                userEmailInstance.save()
                messages.info(request,'password set')
                return redirect('login_url')
            
    except Exception as e:
        return HttpResponse(e)
    
    context = {}
    return render(request,"uaa/recoverPassword.html")


def DashboardView(request):
    
    context = {}
    return render(request,"uaa/dashboard.html")


def ProfileView(request):
    try:
        myCredentials = User.objects.get(id=request.user.id)
        
        myProfileInfos = Profile.objects.get(user=request.user)
    
    except:
        return render(None, 'uaa/error500.html')
        
    context = {"myCredential":myCredentials, "myProfileInfo":myProfileInfos}
    return render(request,"uaa/profile.html", context)

def UpdateProfileView(request):
    
    try:
        updateUser = User.objects.get(id=request.user.id)
        updateProfile = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            FirstName = request.POST.get('FirstName')
            LastName = request.POST.get('LastName')
            PhoneNumber = request.POST.get('PhoneNumber')
            NidaNumber = request.POST.get('NidaNumber')
            Bod = request.POST.get('Bod')
            Address = request.POST.get('Address')
            genderValue = request.POST.get('genderValue')
            
        
            if len(FirstName) < 3:
                messages.info(request,'First Name, Is too short')
                return redirect('/profile')
            
            if len(LastName) < 3:
                messages.info(request,'Last Name, Is too short')
                return redirect('/profile')
            
            if len(PhoneNumber) < 10 or len(PhoneNumber) > 10:
                messages.info(request,'Invalid phone number format')
                return redirect('/profile')
        
        
            updateUser.first_name = FirstName
            updateUser.last_name = LastName
            updateUser.save()
            
            updateProfile.phone_number = PhoneNumber
            updateProfile.nida_no = NidaNumber
            updateProfile.dob = Bod
            updateProfile.address = Address
            updateProfile.gender = genderValue
            updateProfile.save()
            
            messages.info(request,'Your Profile Is Updated')
            return redirect('/profile')
    
    except:
        return render(None, 'uaa/error500.html')
    
def UpdateProfilePicView(request):
    
    try:
        updateProfilePic = User.objects.get(id=request.user.id)
        if request.method == 'POST' and 'profilePic' in request.FILES:
            profile = request.FILES
            profileImage = profile['profilePic']
            
            updateProfilePic.profileImage = profileImage
            updateProfilePic.save()
            
            messages.info(request,'Your Profile picture Is Updated')
            return redirect('profile_url')
    
    except:
        return render(None, 'uaa/error500.html')


def SuccessView(request):
    
    context = {}
    return render(request,"uaa/success.html")


def TokenSendView(request):
    
    context = {}
    return render(request,"uaa/tokensend.html")


def ErrorView(request):
    
    context = {}
    return render(request,"uaa/error.html")


def UaaUserListView(request):
  
    roleInstance = Group.objects.all()
    
    
    
    userList = Profile.objects.all()
        
   
    
    context = {'roleInstanceData': roleInstance, 'userListData':userList}
    return render(request, 'uaa/uaaUserList.html', context)


def CreateUserView(request):
    
    try:
        if request.method == 'POST':
            username = request.POST.get('Username')
            email = request.POST.get('Email') 
            # branchId = request.POST.get('branchId')
            # RoleId = request.POST.get('RoleId')
            password = request.POST.get('Password')
            password1 = request.POST.get('ConfirmPassword')
            
            if User.objects.filter(username=username).first():
                messages.info(request,'Username is already taken')
                return redirect('uaaUserList_url')
            
            if User.objects.filter(email=email).first():
                messages.info(request,'Email is already taken')
                return redirect('uaaUserList_url')
            
            if len(username) < 5:
                messages.info(request,'username, atlest 5 characters')
                return redirect('uaaUserList_url')
            
            if password != password1:
                messages.info(request,'password does not match')
                return redirect('uaaUserList_url')
            
            # if len(password) < 8:
            #     messages.info(request, 'password, 8 mixed characters required')
            #     return redirect('uaaUserList_url')
            
            #Creating and saving a user to the database.
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            
            #Adding a default role to the registered user.
            # grp = Group.objects.get(id=RoleId)
            # user= User.objects.get(username=username)
            # user.groups.add(grp)
            
            #creating a user profile.
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token, createdBy_id=request.user.id, updatedBy_id=request.user.id)
            profile_obj.save()
            
            #Sending email for verification.
            # try:
            #     SendEmailRegister(email, auth_token)
            # except Exception as e:
            #     print(e)
            
            # messages.info(request,'Check your email to verify.')
            return redirect('uaaUserList_url')
        
    except:
        return render(None, 'uaa/error500.html')

def UpdateUserView(request):
    try:
        if request.method == "POST":
            profileId = request.POST.get('profileId')
            Username = request.POST.get('Username') 
            Email = request.POST.get('Email')
            branchId = request.POST.get('branchId')
            RoleId = request.POST.get('RoleId')
            
            try:
                requestUserInstance = request.user
                profileInstance = Profile.objects.get(id=profileId)
                userId = profileInstance.user.id
                userInstance = User.objects.get(id=userId)
            except Exception as e:
                print(e)
                
            try:
                if userInstance == requestUserInstance:
                    return redirect('uaaUserList_url')
            except Exception as e:
                print(e)
            
            try:
                userInstance.username = Username
                userInstance.email = Email
                userInstance.save()
            except Exception as e:
                print(e)
            
            try:
                profileInstance.branch_id = branchId
                profileInstance.updatedBy_id = request.user.id
                profileInstance.save()
            except Exception as e:
                print(e)
            
            try:
                newGroup = Group.objects.get(id=RoleId)
                currentUserGroups = userInstance.groups.all()
                #removing user to all roles.
                for group in currentUserGroups:
                    userInstance.groups.remove(group)
                #add the user to new role
                userInstance.groups.add(newGroup)
            except Exception as e:
                print(e)
            
            messages.success(request,'User Updated')
            return redirect('uaaUserList_url')
        
    except:
        return render(None, 'uaa/error500.html')

def UserStatusView(request):
    
    try:
        userInstance = request.user
        userStatusObject = get_object_or_404(User,pk=request.GET.get('userStatus_id'))
        if userInstance == userStatusObject:
            return redirect('uaaUserList_url')
        
        userStatusObject.is_active = not userStatusObject.is_active
        userStatusObject.save()
        messages.info(request,'User status changed')
        return redirect('uaaUserList_url')

    except:
        return render(None, 'uaa/error500.html')
        

def ApproveUserView(request):
    try:
        userInstance = request.user
        userStatusObject = get_object_or_404(Profile,pk=request.GET.get('approveProfile_id'))
        if userInstance == userStatusObject.user:
            return redirect('uaaUserList_url')
        
        userStatusObject.is_approved = not userStatusObject.is_approved
        userStatusObject.save()
        messages.info(request,'User  successfully approved.')
        return redirect('uaaUserList_url')
    
    except:
        return render(None, 'uaa/error500.html')



        


def LogoutView(request):
    logout(request)
    return redirect('login_url')
