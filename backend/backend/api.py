from rest_framework import viewsets, serializers, permissions
from rest_framework import routers
from django_filters.rest_framework import DjangoFilterBackend

from .models import ToDoList, ToDoItem


class ToDoItemSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = ToDoItem
        fields = ["id", "text", "finished", "created_at", "parent"]


class ToDoItemViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["parent", "finished"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            # ветка только для генерации схемы
            return ToDoItem.objects.all()
        return ToDoItem.objects.filter(parent__user=user)


class ToDoListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToDoList
        fields = ["id", "title", "created_at"]


class ToDoListViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            # ветка только для генерации схемы
            return ToDoList.objects.all()
        return ToDoList.objects.filter(user=user)


router = routers.DefaultRouter()
router.register(r"lists", ToDoListViewSet, basename="ToDoLists")
router.register(r"todo_items", ToDoItemViewSet, basename="ToDoItems")
