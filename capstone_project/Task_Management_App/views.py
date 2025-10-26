from rest_framework import generics, permissions, filters, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create or get token for the new user
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Welcome! Registration Successful.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token.key,  # 👈 immediately return token
        }, status=status.HTTP_201_CREATED)



# --------------------------
# USER LOGIN VIEW
# --------------------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)

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
