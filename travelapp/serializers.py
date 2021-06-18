from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Comment, Category, PostImages, Product, Tour, Like, Rating


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Name must start with upper case")
        return value

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError("Password didn't match!")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data.get('last_name'))
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'is_staff',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
        return representation


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImages
        exclude = ('id', )


class TourSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = ('id', 'title', 'body', 'owner', 'comments', 'category', 'preview', 'images', )

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get('request')
        # print("Файлы: ", request.FILES)
        images_data = request.FILES
        created_post = Tour.objects.create(**validated_data)
        print(created_post)
        print("worked: ", images_data.getlist)
        print("doesnt work: ", images_data)
        # for image_data in images_data.getlist('images'):
        #     PostImages.objects.create(post=created_post, image=image_data)
        images_obj = [
            PostImages(post=created_post, image=image) for image in images_data.getlist('images')
        ]
        PostImages.objects.bulk_create(images_obj)
        return created_post


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # category = CategorySerializer(many=False, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        request = self.context.get('request')
        # print("Файлы: ", request.FILES)
        images_data = request.FILES
        user = request.user
        created_product = Product.objects.create(**validated_data)
        print(created_product)
        print("worked: ", images_data.getlist)
        print("doesnt work: ", images_data)
        # for image_data in images_data.getlist('images'):
        #     PostImages.objects.create(post=created_product, image=image_data)
        images_obj = [
            PostImages(post=created_product, image=image) for image in images_data.getlist('images')
        ]
        PostImages.objects.bulk_create(images_obj)
        return created_product


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'post')


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rating
        fields = ('rating_field', 'owner', 'tour', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.email
        return representation


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ('owner', 'post', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.email
        return representation
