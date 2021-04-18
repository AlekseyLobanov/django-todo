from rest_framework import viewsets, serializers, permissions
from rest_framework import routers
from django_filters.rest_framework import DjangoFilterBackend

from .models import ToDoList, ToDoItem


class ToDoListField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        return ToDoList.objects.filter(user=user)


class ToDoItemSerializer(serializers.HyperlinkedModelSerializer):
    parent = ToDoListField(many=False, read_only=False, help_text="ID родительского списка")

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

    def create(self, validated_data):
        todo_list = ToDoList.objects.create(
            user=self.context["request"].user, title=validated_data["title"]
        )
        return todo_list


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
