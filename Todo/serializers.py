from django.db.models import F
from rest_framework import serializers

from Todo.models import Category, ToDo
from common_library import get_max_int_from_queryset, make_space_ordering_from_queryset


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'orderNumber',
        ]


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'author',
            'name',
            'orderNumber',
        ]
        extra_kwargs = {'author': {'required': False}}

    def create(self, validated_data):
        orderNumber = int(validated_data.pop('orderNumber'))
        category_set = self.context['request'].user.category_set.all()

        # 정렬 순서가 초과하면 맨 마지막에 정렬 순서 배치
        if orderNumber != 1 and not category_set.filter(orderNumber=orderNumber - 1).exists():
            # 생성하는 경우 1개가 더 생김으로 + 1
            orderNumber = get_max_int_from_queryset(category_set, 'orderNumber') + 1

        category_set.filter(
            orderNumber__gte=orderNumber
        ).update(
            orderNumber=F('orderNumber') + 1
        )

        category = self.Meta.model.objects.create(**validated_data, orderNumber=orderNumber)
        return category

    def update(self, instance, validated_data):
        update_fields = ['name', 'updated_at']

        category_set = self.context['request'].user.category_set.all()
        instance.name = validated_data.get('name', instance.name)
        orderNumber = int(validated_data.get('orderNumber'))

        # 정렬 순서가 초과하면 맨 마지막에 정렬 순서 배치
        if orderNumber != 1 and not category_set.filter(orderNumber=orderNumber - 1).exists():
            orderNumber = get_max_int_from_queryset(category_set, 'orderNumber')

        if instance.orderNumber != orderNumber:
            target_category_orderNumber = orderNumber
            current_category_orderNumber = instance.orderNumber

            make_space_ordering_from_queryset(category_set, current_category_orderNumber, target_category_orderNumber, 'orderNumber')

            update_fields.append('orderNumber')
            instance.orderNumber = orderNumber

        instance.save(update_fields=update_fields)
        return instance


class ToDoListSerializer(serializers.ModelSerializer):
    category__id = serializers.IntegerField(source='category.id', default=None)
    category__name = serializers.CharField(source='category.name', default=None)

    class Meta:
        model = ToDo
        fields = [
            'id',
            'orderNumber',
            'deadLine',
            'startDate',
            'completedDate',
            'updated_at',
            'text',
            'category__id',
            'category__name',
        ]

class ToDoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = [
            'author',
            'orderNumber',
            'deadLine',
            'startDate',
            'text',
            'category',
        ]
        extra_kwargs = {'author': {'required': False}}

    def create(self, validated_data):
        todo_qs = self.context['request'].user.todo_set.filter(
            completedDate__isnull=True,
            orderNumber__isnull=False,
        )
        max_orderNumber = get_max_int_from_queryset(todo_qs, 'orderNumber')

        if not max_orderNumber:
            max_orderNumber = 1
        else:
            max_orderNumber += 1

        todo = self.Meta.model.objects.create(**validated_data, orderNumber=max_orderNumber)
        return todo

    def update(self, instance, validated_data):
        instance.deadLine = validated_data.get('deadLine', instance.deadLine)
        instance.text = validated_data.get('text', instance.text)
        instance.category_id = validated_data.get('category', instance.category_id)
        instance.save(update_fields=['deadLine', 'text', 'category_id', 'updated_at'])
        return instance
