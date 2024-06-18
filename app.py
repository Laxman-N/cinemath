from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Movie:
    def __init__(self, title, genre, rating):
        self.title = title
        self.genre = genre
        self.rating = rating

class CineMatch:
    def __init__(self):
        self.movies = []
        self.movie_dict = {}

    def add_movie(self, title, genre, rating):
        if title in self.movie_dict:
            return False
        movie = Movie(title, genre, rating)
        self.movies.append(movie)
        self.movie_dict[title] = movie
        return True

    def search_by_title(self, title):
        return self.movie_dict.get(title, None)

    def search_by_genre(self, genre):
        return [movie for movie in self.movies if movie.genre.lower() == genre.lower()]

    def recommend_top_n_movies(self, n):
        sorted_movies = sorted(self.movies, key=lambda movie: movie.rating, reverse=True)
        return sorted_movies[:n]

    def delete_movie(self, title):
        movie = self.movie_dict.pop(title, None)
        if movie:
            self.movies.remove(movie)
            return True
        return False

cinematch = CineMatch()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = float(request.form['rating'])
        if cinematch.add_movie(title, genre, rating):
            return redirect(url_for('index'))
        else:
            return "Movie already exists!"
    return render_template('add_movie.html')

@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    if request.method == 'POST':
        title = request.form['title']
        movie = cinematch.search_by_title(title)
        return render_template('search_movie.html', movie=movie)
    return render_template('search_movie.html', movie=None)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend_movie():
    if request.method == 'POST':
        top_n = request.form.get('top_n')
        genre = request.form.get('genre')
        
        if top_n:  # If top_n is provided, recommend top N movies
            n = int(top_n)
            top_movies = cinematch.recommend_top_n_movies(n)
            return render_template('recommend_movie.html', movies=top_movies, mode='Top N')
        elif genre:  # If genre is provided, recommend movies of that genre
            genre_movies = cinematch.search_by_genre(genre)
            return render_template('recommend_movie.html', movies=genre_movies, mode='Genre')
        else:
            return "Please provide either Top N or Genre for recommendations."
    
    return render_template('recommend_movie.html', movies=None)

@app.route('/delete', methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        title = request.form['title']
        if cinematch.delete_movie(title):
            return redirect(url_for('index'))
        else:
            return "Movie not found!"
    return render_template('delete_movie.html')

if __name__ == '__main__':
    app.run(debug=True)
