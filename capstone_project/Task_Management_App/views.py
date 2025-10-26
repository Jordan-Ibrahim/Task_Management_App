from rest_framework import generics, permissions, filters, status
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# --------------------------
# USER REGISTRATION VIEW
# --------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # Allow GET for development/testing visibility
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        
        return Response({
            "message": "Use POST to register a new user.",
            "example_body": {
                "username": "new_user",
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        })


# --------------------------
# USER LOGIN VIEW
# --------------------------
class LoginView(ObtainAuthToken):

    # Add GET support for testing
    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Use POST to log in and receive a token.",
            "example_body": {
                "username": "existing_user",
                "password": "userpassword"
            }
        })

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })


# --------------------------
# TASK LIST + CREATE VIEW
# --------------------------
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'priority', 'status']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --------------------------
# TASK DETAIL VIEW
# --------------------------
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# --------------------------
# MARK TASK COMPLETE VIEW
# --------------------------
class MarkTaskCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        """Development only: shows usage example"""
        return Response({
            "message": "Use POST to mark a task as complete.",
            "example_url": f"/api/tasks/{pk}/complete/"
        })

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.is_completed = True
            task.save()
            return Response({"message": "Task marked as complete"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
