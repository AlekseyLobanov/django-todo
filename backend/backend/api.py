from rest_framework import viewsets, serializers, permissions
from rest_framework import routers
from rest_framework.response import Response
from rest_framework import status

from .models import ToDoList


class ToDoListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToDoList
        fields = ["title", "created_at"]

class WriteToDoListSerializer(serializers.Serializer):
    class Meta:
        model = ToDoList
        fields = ["title", "created_at", "user"]
    
    def create(self, validated_data):
        return ToDoList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance

class ToDoListViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoListSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = ToDoList.objects.all()
        print(type(queryset), queryset.__dict__)
        user = self.request.user
        print(type(user), user.__dict__)
        return queryset.filter(user=user)
    
    def create(self, request):
        data = {
            'user': request.user,
            'title': request.data['title'],
        }
        serializer = WriteToDoListSerializer(data=data)
        print(serializer.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


router = routers.DefaultRouter()
router.register(r"lists", ToDoListViewSet, basename="ToDoList")
