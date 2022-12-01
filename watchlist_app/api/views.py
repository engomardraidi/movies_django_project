from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from watchlist_app.models import Movie
from .serializers import MovieSerializer

class MovieList(APIView):
    def get(self, request, format = None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, format = None):
        data = request.data
        serializer = MovieSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class MovieDetail(APIView):
    def get(self, request, pk = None):
        try:
            movie = Movie.objects.get(id = pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"ERROR":"MOVIE NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)

    def put(self, request, pk = None):
        try:
            movie = Movie.objects.get(id = pk)
            serializer = MovieSerializer(movie, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"ERROR":"MOVIE NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk = None):
        try:
            movie = Movie.objects.get(id = pk)
            movie.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({"ERROR":"MOVIE NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)