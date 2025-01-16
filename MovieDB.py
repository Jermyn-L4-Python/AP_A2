import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

class MovieApp:
    def __init__(self, root):
        
        self.base_url = "https://api.themoviedb.org/3/"
        self.API_KEY = 'a59b01a38c311dff0332dc71414dd307'
        self.image_base_url = "https://image.tmdb.org/t/p/w500"

        
        self.root = root
        self.root.title("TMDB App")
        self.root.geometry("500x700")
        self.root.config(bg="#71788F")

        
        self.frame_input = tk.Frame(self.root, bg="#2C3E50")
        self.frame_input.pack(fill="x")

        self.label = tk.Label(self.frame_input, text="The MovieDB", font=("Arial", 20), fg="#FFBF00", bg="#2C3E50")
        self.label.pack(side="top", anchor="center", pady=10)

        self.frame_center = tk.Frame(self.frame_input, bg="#2C3E50")
        self.frame_center.pack(pady=10)

        self.enter_movie = tk.Entry(self.frame_center, font=("Arial", 15))
        self.enter_movie.pack(side="left", padx=10, pady=10)

        self.search_button = tk.Button(self.frame_center, text="Search", font=("Arial", 14), bg="#FFBF00", command=self.on_search_click)
        self.search_button.pack(side="left", padx=10, pady=10)

        
        self.movie_details_frame = tk.Frame(self.root, bg="#71788F")
        self.movie_details_frame.pack(pady=40)

        self.label_image = tk.Label(self.movie_details_frame, highlightbackground="black", highlightthickness=2)
        self.label_image.pack(side="left", padx=10, pady=10)

        self.label_result = tk.Label(self.movie_details_frame, text="", font=("Arial", 15), fg="black", bg="#71788F", justify="left", anchor="w", width=50, wraplength=400)
        self.label_result.pack(side="left", padx=10, pady=10)

    def on_search_click(self):
        movie_title = self.enter_movie.get()
        if movie_title:
            self.get_movie_info(movie_title)
        else:
            messagebox.showerror("Input Error", "Please enter a movie title.")

    def get_movie_info(self, movie_title):
        
        url = f"{self.base_url}search/movie?api_key={self.API_KEY}&query={movie_title}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data['results']:
                movie = data['results'][0]  
                title = movie.get("title", "N/A")
                release_date = movie.get("release_date", "N/A")
                overview = movie.get("overview", "N/A")
                rating = movie.get("vote_average", "N/A")
                if rating != "N/A":
                    rating = round(rating, 1)
                poster_path = movie.get("poster_path", None)

                if poster_path:
                    self.display_poster(poster_path)

                movie_info = f"Title: {title}\n\nRelease Date: {release_date}\n\nOverview: {overview}\n\nRating: {rating}/10"
                self.label_result.config(text=movie_info)
            else:
                messagebox.showerror("Movie Not Found", "No movie found with that title.")
        else:
            messagebox.showerror("Error", f"Failed to fetch data. Status code: {response.status_code}")

    def display_poster(self, poster_path):
        poster_url = f"{self.image_base_url}{poster_path}"
        img_response = requests.get(poster_url)
        img_data = img_response.content
        img = Image.open(io.BytesIO(img_data))  
        img = img.resize((400, 500))  
        img_tk = ImageTk.PhotoImage(img)  

        self.label_image.config(image=img_tk)
        self.label_image.image = img_tk  



root = tk.Tk()
app = MovieApp(root)
root.mainloop()