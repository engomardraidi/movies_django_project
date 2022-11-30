from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from watchlist_app.models import Movie
from .serializers import MovieSerializer

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        movie_data = request.data
        serializer = MovieSerializer(data = movie_data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_details(request, pk):
    try:
        movie = Movie.objects.get(pk = pk)
        if request.method == 'GET':
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            movie_data = request.data
            serializer = MovieSerializer(movie, data = movie_data)
            if serializer.is_valid():
                movie = serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            movie.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
    except Movie.DoesNotExist:
        return Response({"ERROR":"MOVIE NOT FOUND"}, status = status.HTTP_404_NOT_FOUND)