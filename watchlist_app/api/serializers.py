from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Movie name is too short')

class WatchListSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()

    class Meta:
        model = WatchList
        fields = '__all__'
        # fields = ['id', 'name', 'description']
        # exclude = ['active']

    def get_len_name(self, object):
        return len(object.title)

    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError('Movie title cannot be the same as storyline')
        else:
            return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Movie name is too short")
        else:
            return value

class StreamPlatformSerializer(serializers.ModelSerializer):
    # return all data in watchlist records
    # watchlist = WatchListSerializer(many = True, read_only = True)

    # return the value we are use it in __str__ method, here is (name)
    # watchlist = serializers.StringRelatedField(many = True)

    # return primary key
    # watchlist = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    # return hyperlink for each record
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many = True,
    #     read_only = True,
    #     view_name = 'watch_list_details_view'
    #     )

    class Meta:
        model = StreamPlatform
        fields = '__all__'
        # fields = ['id', 'name']
        # exclude = ['active']

    class Meta:
        model = StreamPlatform
        fields = '__all__'

    # id = serializers.IntegerField(read_only = True)
    # name = serializers.CharField(validators = [name_length])
    # description = serializers.CharField()
    # active = serializers.BooleanField()

    # def create(self, validated_data):
    #     return Movie.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.active = validated_data.get('active', instance.active)
    #     instance.save()

    #     return instance
    
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError('Movie name cannot be the same as description')
    #     else:
    #         return data

    # # def validate_name(self, value):
    # #     if len(value) < 2:
    # #         raise serializers.ValidationError("Movie name is too short")
    # #     else:
    # #         return value