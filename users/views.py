from django.shortcuts import render
from .models import User, Doctor, Conversation, Message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import json
from django.http import JsonResponse
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer, DoctorSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .services.openai_service import get_ai_response
from openai import OpenAI
from django.conf import settings
from django.http import JsonResponse
import time
from google import genai
from .rag import get_rag_context

# client = OpenAI()
# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# genai.configure(api_key="settings.API_KEY")

# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Hello")
client = genai.Client(api_key=settings.API_KEY)


# print(response.text)

@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    try:
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"message": "Email does not exist","status_code": 0})
        if not check_password(password, user.password):
            return Response({"message": "Invalid password","status_code": 0})        
        user = authenticate(username=email, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "token": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "status_code": 1
        })
    except Exception as e:
        return Response({
            "message": "Error during login",
            "error": str(e),
            "status_code": 0
        })

@csrf_exempt
@api_view(['POST'])
def register(request):
     if request.method == "POST":
        data = json.loads(request.body)
        e = data.get("email")
        p = data.get("password")
        name = data.get("name")
        number = data.get("mobileNumber")
        user = User.objects.filter(email=e).exists()
        if user:
            return Response({"message": "User already exists", "status_code": 0}, status_code=1)
        try: 
            user = User.objects.create_user(username=e, email=e, password=p)
            serializer = UserSerializer(user)   
            profile = Profile.objects.create(user=user, mobilenumber=number, name=name)
            return Response({"message": "Joined Successful", "user": {"id": user.id,"email": user.email},
            "profile": {"mobile": profile.mobilenumber,"name": profile.name}, "status_code": 1})
        except Exception as e:
            return Response({"message": "Error while registering","error": str(e), "status_code":0})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userdata(request):
    # id = request.data.get("id")
    user = request.user
    print("users", user);
    try:
        profile = Profile.objects.get(user=user)
        if profile:
            return Response({"user": {"name": profile.name,"email": user.email,"mobile": profile.mobilenumber}, "status_code":1})
        else:
            return Response({"user": {"user does not found"}, "status_code":0})
    except Exception as e:
        return Response({"message": "Error while getting the data","error": str(e), "status_code":0})
  
@api_view(['POST'])
def emailExistorNot(request):
    email = request.data.get("email") 
    print("Emailsss", email)   
    existemail = User.objects.filter(email=email).first()
    print("Existemail", existemail)
    if existemail:
        return Response({
            "message": "The Email is already Exists", 
            "status_code":1, 
            "existemail": {"id": existemail.id, "email": existemail.email,}})
    else:
        return Response({"message": "The Email is not Exists", "status_code":0})

@api_view(['POST'])
def updatepassword(request):
    try:
        email= request.data.get("email")
        password= request.data.get("retypepassword")
        id= request.data.get("id")
        user = User.objects.get(id=id)
        user.set_password(password)
        user.save()
        return Response({"message": "Password updated successfully","status_code": 1})
    except User.DoesNotExist:
        return Response({"message": "User not found","status_code": 0})
    except Exception as e:
        return Response({"message": "Error updating password","error": str(e), "status_code": 0})
   
@api_view(['POST'])
def add_doctors(request):
    print("Doctors request data", request.data);
    name = request.data.get("name")
    specialization =  request.data.get("specialization")
    experience = request.data.get("experience")
    profession = request.data.get("Profession")
    hospitalName = request.data.get("HospitalName")
    hospitalLocation = request.data.get("HospitalLocation")
    mobileNumber = request.data.get("MobileNumber")
    try:
        doctor = Doctor.objects.create(name=name, specialization=specialization, experience = experience, profession=profession, hospitalname=hospitalName, hospital_location=hospitalLocation, mobilenumber=mobileNumber)
        return Response({"message": "Doctors added Successfully", "doctor":{
            "name":doctor.name
        }, "status_code": 1})
    except Exception as e:
            return Response({"message": "Error while Adding doctors","error": str(e), "status_code":0})
  
@api_view(['GET'])
def getDoctorsdata(request):
    try:
        doctor = Doctor.objects.all()
        print("get doctors", doctor)
        serializer = DoctorSerializer(doctor, many=True)

        return Response({
            "data": serializer.data,
            "status_code": 1
        })

        # return Response({doctor})
    except Exception as e:
            return Response({"message": "Error while getting doctors","error": str(e), "status_code":0})

@api_view(['POST'])
def book_appointments(request):
    id=request.data.get("storageuserid")
    doctorid=request.data.get("id")
    time=request.data.get("time")
    date=request.data.get("date")
    description=request.data.get("description")
    try:
        appointment = Appointment.objects.create(doctor_id=doctorid, user_id=id, time=time, date=date, status=1, description=description)
        return Response({"message": "Appointment done", "appointment":{"id":appointment.id
        }, "status_code": 1})
    except Exception as e:
        return Response({"message": "Error while Adding doctors","error": str(e), "status_code":0})

@api_view(['GET'])
def getAppointments(request):
    id=request.query_params.get("user_id")
    print("Idddd", id)
    try:
        appointment = Appointment.objects.filter(user_id=id)
        print("Appointments", appointment);
        serializer = AppointmentSerializer(appointment, many=True)
        return Response({
            "data": serializer.data,
            "status_code": 1
        })
    except Exception as e:
        return Response({"message": "Error while getting Appointments","error": str(e), "status_code":0})

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            user_message = body.get("message")
            conversation_id = body.get("conversation_id")
            user_id = body.get("user_id")

            if not user_message:
                return JsonResponse({"error": "Message is required"}, status=400)

            if not user_id:
                return JsonResponse({"error": "User ID required"}, status=400)

            #  STEP 1: Get or Create Conversation FIRST
            if conversation_id:
                conversation = Conversation.objects.filter(
                    id=conversation_id,
                    user_id=user_id
                ).first()

                if not conversation:
                    return JsonResponse({"error": "Conversation not found"}, status=404)
            else:
                conversation = Conversation.objects.create(
                    user_id=user_id,
                    title=user_message[:30]
                )

            #  STEP 2: MEMORY
            messages = Message.objects.filter(
                conversation=conversation
            ).order_by("-id")[:10]

            messages = list(messages)[::-1]

            chat_history = ""
            for msg in messages:
                chat_history += f"{msg.sender}: {msg.content}\n"

            #  STEP 3: RAG (NOW conversation exists)
            context = get_rag_context(user_message, conversation.id)

            #  STEP 4: PROMPT
            prompt = f"""
You are a helpful AI assistant.
Instructions:
- Give a brief but informative answer
- Use clear headings 
- Use bullet points
- Each bullet point must be SHORT 
- Add relevant emojis in headings and points
- Keep it visually structured and engaging
- Add a blank line between each bullet point
- Make output clean and readable
- Do NOT give plain paragraphs
- Limit to 5-6 bullet points maximum


Example format:

### 🚀 Topic

- Point 1

- Point 2

- Point 3

Now answer:

Conversation:
{chat_history}

Context:
{context}

User: {user_message}
AI:
"""

            print("User:", user_message)

            #  STEP 5: SAVE USER MESSAGE
            Message.objects.create(
                conversation=conversation,
                sender="user",
                content=user_message
            )

            #  STEP 6: AI CALL
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            # reply = response.text
            reply = call_gemini(prompt)
            # print("Reply", reply)


            #  STEP 7: SAVE AI MESSAGE
            Message.objects.create(
                conversation=conversation,
                sender="ai",
                content=reply
            )

            return JsonResponse({
                "reply": reply,
                "conversation_id": conversation.id
            })

        except Exception as e:
            print("ERROR:", str(e))
            return JsonResponse({
                "reply": "Something went wrong"
            }, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


 
@csrf_exempt
def get_chatting(request):
    body = json.loads(request.body)
    user_id = body.get("user_id")
    print("userid", user_id)
    if not user_id:
        return JsonResponse({"error": "user_id required"}, status=400)
    convs = Conversation.objects.filter(user_id=user_id).order_by("-id")
    print("Conversation", convs)
    data = [
        {
            "id": c.id,
            "title": c.title
        }
        for c in convs
    ]

    return JsonResponse(data, safe=False)

@csrf_exempt
def get_previouschatting(request):
    body = json.loads(request.body)
    conversationId = body.get("conversationId")
    if conversationId:
        msg = Message.objects.filter(conversation_id=conversationId).order_by("id")
        print("Messages", msg)
        data = [{
            "id":m.id,
            "conversation_id":m.conversation_id,
            "sender":m.sender,
            "content":m.content
        } for m in msg
        ]
    return JsonResponse(data, safe=False)

def call_gemini(prompt):
    for i in range(3):  # retry 3 times
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print("Retrying...", i)
            time.sleep(2)

    return "⚠️ AI is busy. Please try again."



