from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
# from rest_framework import mixins
from rest_framework import status, generics
from watchlist_app.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        serializer.save(watchlist = movie)

# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  GenericAPIView):
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.all()

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetails(mixins.RetrieveModelMixin,
#                     # mixins.UpdateModelMixin,
#                     # mixins.DestroyModelMixin,
#                     GenericAPIView):
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.all()

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

class StreamPlatformView(APIView):
    def get(self, request, format = None):
        streamPlatform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamPlatform, many = True, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, format = None):
        streamPlatform = request.data
        serializer = StreamPlatformSerializer(data = streamPlatform)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailsView(APIView):
    def get(self, request, pk = None):
        try:
            streamPlatform = StreamPlatform.objects.get(pk = pk)
            serializer = StreamPlatformSerializer(streamPlatform, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except StreamPlatform.DoesNotExist:
            return Response({"ERROR":"STREAM PLATFORM NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)

    def put(self, request, pk = None):
        try:
            streamPlatform = StreamPlatform.objects.get(pk = pk)
            serializer = StreamPlatformSerializer(streamPlatform, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
        except StreamPlatform.DoesNotExist:
            return Response({"ERROR":"STREAM PLATFORM NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk = None):
        try:
            streamPlatform = StreamPlatform.objects.get(pk = pk)
            streamPlatform.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except StreamPlatform.DoesNotExist:
            return Response({"ERROR":"STREAM PLATFORM NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)

class WatchListView(APIView):
    def get(self, request, format = None):
        watchList = WatchList.objects.all()
        serializer = WatchListSerializer(watchList, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, format = None):
        data = request.data
        serializer = WatchListSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class WatchListDetailView(APIView):
    def get(self, request, pk = None):
        try:
            watchList = WatchList.objects.get(id = pk)
            serializer = WatchListSerializer(watchList)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except WatchList.DoesNotExist:
            return Response({"ERROR":"WATCHLIST NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)

    def put(self, request, pk = None):
        try:
            watchList = WatchList.objects.get(id = pk)
            serializer = WatchListSerializer(watchList, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except WatchList.DoesNotExist:
            return Response({"ERROR":"WATCHLIST NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk = None):
        try:
            watchList = WatchList.objects.get(id = pk)
            watchList.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except WatchList.DoesNotExist:
            return Response({"ERROR":"WATCHLIST NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)