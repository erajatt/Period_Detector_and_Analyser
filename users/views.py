from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, PeriodDetailSerializer
from .models import User, PeriodDetail
import jwt, datetime
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import seaborn as sns
from collections import Counter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import io


# Create your views here.
class Register(APIView):
    def post(self, request):
        print(request)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True, samesite=None)
        response.data = {
            'jwt': token
        }
        return response


class ViewUser(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class CreatePeriodDetail(APIView):
    def post(self, request):
        print(request)
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        print("error loc 1")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        
            user_id = payload.get('id')

            data = {
                'user': user_id,
                'start_date': request.data.get('start_date'),
                'end_date': request.data.get('end_date'),
                'symptoms': request.data.get('symptoms')
            }
            print("error log 2")
            # Serialize the data
            serializer = PeriodDetailSerializer(data=data)

            # Validate the serializer
            serializer.is_valid(raise_exception=True)

            # Save the period detail
            serializer.save()
            print("error loc 3")
            return Response(serializer.data)
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')
        
class RetrievePeriodsData(APIView):
    def post(self, request):
        # Retrieve the JWT token from the request
        token = request.token

        # Check if the token is provided
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Decode the JWT token
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            # Retrieve the user based on the user ID in the payload
            user_id = payload.get('id')

            # Retrieve start and end date range from request data
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            # Query period details based on user and date range
            if start_date and end_date:
                periods = PeriodDetail.objects.filter(user_id=user_id, start_date__range=[start_date, end_date]).order_by('-start_date')
            else:
                periods = PeriodDetail.objects.filter(user_id=user_id).order_by('-start_date')
                
            serializer = PeriodDetailSerializer(periods, many=True)

            return Response(serializer.data)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')


class PredictNextPeriod(APIView):
    def get(self, request):
        # Retrieve the JWT token from the request
        token = request.COOKIES.get('jwt')

        # Check if the token is provided
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Decode the JWT token
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            # Retrieve the user based on the user ID in the payload
            user_id = payload.get('id')

            # Retrieve previous start dates of the user's periods
            previous_periods = PeriodDetail.objects.filter(user=user_id).order_by('-start_date')

            if not previous_periods:
                return Response({'message': 'No previous periods available for prediction'})
            
            if len(previous_periods)==1:
                mean_gap=28
            else:
                gaps = [(previous_periods[i].start_date - previous_periods[i+1].start_date).days for i in range(len(previous_periods)-1)]
                mean_gap = sum(gaps) / len(gaps)
                
            durations=[(previous_periods[i].end_date-previous_periods[i].start_date).days for i in range(len(previous_periods))]
            mean_duration=round(sum(durations)/len(durations))
            predicted_start_date = previous_periods[0].start_date + datetime.timedelta(days=mean_gap)
            predicted_end_date = predicted_start_date + datetime.timedelta(days=mean_duration)

            return Response({'predicted_start_date': predicted_start_date,
                             "predicted_end_date":predicted_end_date,
                             "average_cycle_length":mean_duration})

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')


class AnalyzeSymptoms(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
            
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('id')

            previous_periods = PeriodDetail.objects.filter(user=user_id).order_by('-start_date')

            if not previous_periods:
                return Response({'message': 'No previous periods available for analyzing symptoms'})
            
            symptoms_data = [period.symptoms.split(',') for period in previous_periods if period.symptoms]
            
            # Flatten the list of symptoms and create a frequency count
            symptoms_flat = [symptom.strip() for sublist in symptoms_data for symptom in sublist]
            symptom_counts = Counter(symptoms_flat)
            
            # Generate a bar plot of symptom frequencies
            plt.figure(figsize=(10, 6))
            sns.barplot(x=list(symptom_counts.keys()), y=list(symptom_counts.values()))
            plt.xlabel('Symptom')
            plt.ylabel('Frequency')
            plt.title('Symptom Frequencies')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Convert the plot to a PNG image
            bar_buffer = io.BytesIO()
            plt.savefig(bar_buffer, format='png')
            bar_buffer.seek(0)
            plt.close()
            
            symptoms_df = pd.DataFrame(symptoms_data)
            
            # Generate a heatmap of symptom frequencies
            plt.figure(figsize=(10, 6))
            sns.heatmap(symptoms_df.apply(pd.Series.value_counts), annot=True, cmap='coolwarm', fmt='g')
            plt.xlabel('Symptom')
            plt.ylabel('Period')
            plt.title('Symptom Heatmap')
            plt.tight_layout()
            
            # Convert the plot to a PNG image
            heatmap_buffer = io.BytesIO()
            plt.savefig(heatmap_buffer, format='png')
            heatmap_buffer.seek(0)
            plt.close()

            # Create a PDF document
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Add title
            story.append(Paragraph("Symptom Analysis Report", styles['Title']))

            # Add bar plot as an image to the PDF
            bar_img = Image(bar_buffer)
            bar_img.drawHeight = 300
            bar_img.drawWidth = 500
            story.append(bar_img)
            
            # Add heatmap as an image to the PDF
            heatmap_img = Image(heatmap_buffer)
            heatmap_img.drawHeight = 300
            heatmap_img.drawWidth = 500
            story.append(heatmap_img)

            # Build the PDF document
            doc.build(story)
            pdf_buffer.seek(0)
            
            # Create and return the HTTP response with the PDF content
            response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=symptom_analysis.pdf'
            bar_buffer.close()
            heatmap_buffer.close()
            pdf_buffer.close()
            
            plt.close('all')
            root = tk.Tk()
            root.destroy()
            
            return response

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')