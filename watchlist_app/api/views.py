# from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
# from rest_framework.generics import GenericAPIView
# from rest_framework import mixins
from rest_framework import status, generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from .throttling import ReviewCreateThrottle, ReviewDetailsThrottle

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = username)
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username = username)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ReviewDetailsThrottle, AnonRateThrottle]

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle, AnonRateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        review_user = self.request.user

        if not review_user.is_authenticated:
            raise ValidationError('You must login')

        review_queryset = Review.objects.filter(watchlist = movie, review_user = review_user)


        if review_queryset.exists():
            raise ValidationError('You have already reviewed this model')

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2

        movie.number_rating += 1
        movie.save()

        serializer.save(watchlist = movie, review_user = review_user)

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

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatformVS(ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data, status = status.HTTP_200_OK)

#     def retrieve(self, request, pk = None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk = pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data, status = status.HTTP_200_OK)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# class StreamPlatformView(APIView):
#     def get(self, request, format = None):
#         streamPlatform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(streamPlatform, many = True, context = {'request': request})
#         return Response(serializer.data, status = status.HTTP_200_OK)

#     def post(self, request, format = None):
#         streamPlatform = request.data
#         serializer = StreamPlatformSerializer(data = streamPlatform)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

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

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']

class WatchListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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