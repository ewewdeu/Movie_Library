import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Library - Личная кинотека")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg='#1a1a2e')
        
        # Настройка стилей
        self.setup_styles()
        
        self.filename = "movies.json"
        self.movies = []
        
        self.setup_ui()
        self.load_movies()
        
        # Центрирование окна
        self.center_window()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цветовая палитра
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'accent_hover': '#ff6b6b',
            'text_light': '#ffffff',
            'text_dark': '#2d3436',
            'success': '#00b894',
            'warning': '#fdcb6e',
            'error': '#d63031',
            'border': '#2d3436'
        }
        
        # Стиль для LabelFrame
        style.configure('Card.TLabelframe',
                       background=self.colors['bg_medium'],
                       foreground=self.colors['text_light'],
                       borderwidth=2,
                       relief='flat')
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['bg_medium'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Стиль для кнопок
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text_light'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_hover'])])
        
        style.configure('Danger.TButton',
                       background=self.colors['error'],
                       foreground=self.colors['text_light'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10),
                       padding=(20, 10))
        style.map('Danger.TButton',
                 background=[('active', '#ff4757')])
        
        style.configure('Secondary.TButton',
                       background=self.colors['bg_light'],
                       foreground=self.colors['text_light'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9),
                       padding=(10, 5))
        style.map('Secondary.TButton',
                 background=[('active', '#1a5276')])
        
        # Стиль для Entry
        style.configure('Modern.TEntry',
                       fieldbackground='#2d3436',
                       foreground=self.colors['text_light'],
                       borderwidth=1,
                       relief='flat',
                       font=('Segoe UI', 10))
        
        # Стиль для Treeview
        style.configure('Modern.Treeview',
                       background='#2d3436',
                       foreground=self.colors['text_light'],
                       fieldbackground='#2d3436',
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       rowheight=30)
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_light'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       padding=(10, 5))
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', self.colors['text_light'])])
    
    def setup_ui(self):
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Заголовок приложения
        title_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                               text="🎬 Movie Library",
                               font=('Segoe UI', 26, 'bold'),
                               bg=self.colors['bg_dark'],
                               fg=self.colors['accent'])
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(title_frame,
                                  text="Личная кинотека",
                                  font=('Segoe UI', 13),
                                  bg=self.colors['bg_dark'],
                                  fg='#636e72')
        subtitle_label.pack(side='left', padx=(15, 0), pady=(10, 0))
        
        # Основной контент
        content_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        content_frame.pack(fill='both', expand=True)
        
        # Левая панель - УВЕЛИЧЕННАЯ ШИРИНА
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_dark'], width=380)
        left_panel.pack(side='left', fill='y', padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Frame для ввода данных
        input_frame = ttk.LabelFrame(left_panel, 
                                     text="  ➕ Добавление фильма  ",
                                     style='Card.TLabelframe',
                                     padding="20")
        input_frame.pack(fill='x', pady=(0, 15))
        
        # Контейнер для полей ввода с сеткой
        fields_frame = tk.Frame(input_frame, bg=self.colors['bg_medium'])
        fields_frame.pack(fill='x')
        
        # Поля ввода
        fields = [
            ("🎯 Название:", "title"),
            ("🎭 Жанр:", "genre"),
            ("📅 Год выпуска:", "year"),
            ("⭐ Рейтинг (0-10):", "rating")
        ]
        
        self.entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            # Контейнер для строки
            row_frame = tk.Frame(fields_frame, bg=self.colors['bg_medium'])
            row_frame.pack(fill='x', pady=6)
            
            # Метка с фиксированной шириной
            label = tk.Label(row_frame, 
                           text=label_text,
                           font=('Segoe UI', 11),
                           bg=self.colors['bg_medium'],
                           fg=self.colors['text_light'],
                           width=18,
                           anchor='w')
            label.pack(side='left', padx=(0, 10))
            
            # Поле ввода
            entry = ttk.Entry(row_frame, 
                            style='Modern.TEntry',
                            font=('Segoe UI', 11))
            entry.pack(side='left', fill='x', expand=True)
            self.entries[field_name] = entry
        
        # Кнопка добавления
        add_btn_frame = tk.Frame(input_frame, bg=self.colors['bg_medium'])
        add_btn_frame.pack(fill='x', pady=(20, 5))
        
        add_btn = ttk.Button(add_btn_frame, 
                            text="✨ Добавить фильм",
                            style='Accent.TButton',
                            command=self.add_movie)
        add_btn.pack(fill='x')
        
        # Frame для фильтрации
        filter_frame = ttk.LabelFrame(left_panel,
                                      text="  🔍 Фильтрация  ",
                                      style='Card.TLabelframe',
                                      padding="20")
        filter_frame.pack(fill='x')
        
        # Фильтр по жанру
        filter_genre_frame = tk.Frame(filter_frame, bg=self.colors['bg_medium'])
        filter_genre_frame.pack(fill='x', pady=(0, 12))
        
        tk.Label(filter_genre_frame, 
                text="🎭 По жанру:",
                font=('Segoe UI', 11),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_light'],
                width=14,
                anchor='w').pack(side='left', padx=(0, 10))
        
        self.filter_genre = ttk.Entry(filter_genre_frame, 
                                      style='Modern.TEntry',
                                      font=('Segoe UI', 11))
        self.filter_genre.pack(side='left', fill='x', expand=True)
        
        # Фильтр по году
        filter_year_frame = tk.Frame(filter_frame, bg=self.colors['bg_medium'])
        filter_year_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(filter_year_frame,
                text="📅 По году:",
                font=('Segoe UI', 11),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_light'],
                width=14,
                anchor='w').pack(side='left', padx=(0, 10))
        
        self.filter_year = ttk.Entry(filter_year_frame,
                                     style='Modern.TEntry',
                                     font=('Segoe UI', 11))
        self.filter_year.pack(side='left', fill='x', expand=True)
        
        # Кнопки фильтрации
        filter_btn_frame = tk.Frame(filter_frame, bg=self.colors['bg_medium'])
        filter_btn_frame.pack(fill='x')
        
        apply_btn = ttk.Button(filter_btn_frame,
                              text="🔍 Применить",
                              style='Secondary.TButton',
                              command=self.apply_filter)
        apply_btn.pack(side='left', padx=(0, 8))
        
        reset_btn = ttk.Button(filter_btn_frame,
                              text="↺ Сбросить",
                              style='Secondary.TButton',
                              command=self.reset_filter)
        reset_btn.pack(side='left')
        
        # Правая панель (таблица)
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_medium'])
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Заголовок таблицы
        table_header = tk.Frame(right_panel, bg=self.colors['bg_medium'])
        table_header.pack(fill='x', padx=20, pady=(20, 12))
        
        tk.Label(table_header,
                text="📚 Ваша коллекция",
                font=('Segoe UI', 15, 'bold'),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_light']).pack(side='left')
        
        self.movie_count_label = tk.Label(table_header,
                                         text="0 фильмов",
                                         font=('Segoe UI', 11),
                                         bg=self.colors['bg_medium'],
                                         fg='#636e72')
        self.movie_count_label.pack(side='right')
        
        # Таблица фильмов
        table_container = tk.Frame(right_panel, bg=self.colors['bg_dark'])
        table_container.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Создаем таблицу
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_container, 
                                 columns=columns, 
                                 show="headings",
                                 style='Modern.Treeview')
        
        # Настройка заголовков
        for col in columns:
            self.tree.heading(col, text=col, anchor='center')
        
        # Устанавливаем ширину колонок
        self.tree.column("Название", width=400, minwidth=250, anchor='w')
        self.tree.column("Жанр", width=180, minwidth=120, anchor='center')
        self.tree.column("Год", width=120, minwidth=90, anchor='center')
        self.tree.column("Рейтинг", width=130, minwidth=110, anchor='center')
        
        # Цветовые теги
        self.tree.tag_configure('high_rating', foreground='#00b894')
        self.tree.tag_configure('medium_rating', foreground='#fdcb6e')
        self.tree.tag_configure('low_rating', foreground='#d63031')
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_container, 
                                 orient="vertical", 
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Кнопка удаления
        delete_frame = tk.Frame(right_panel, bg=self.colors['bg_medium'])
        delete_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        delete_btn = ttk.Button(delete_frame,
                               text="🗑️ Удалить выбранный фильм",
                               style='Danger.TButton',
                               command=self.delete_movie)
        delete_btn.pack()
        
        # Статус-бар
        self.status_bar = tk.Label(self.root,
                                  text="  Готов к работе",
                                  font=('Segoe UI', 9),
                                  bg=self.colors['bg_light'],
                                  fg='#636e72',
                                  padx=15,
                                  pady=6,
                                  anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def update_status(self, message, status_type='info'):
        colors = {
            'info': '#636e72',
            'success': '#00b894',
            'error': '#d63031',
            'warning': '#fdcb6e'
        }
        self.status_bar.config(text=f"  {message}", fg=colors.get(status_type, '#636e72'))
        self.root.after(3000, lambda: self.status_bar.config(text="  Готов к работе", fg='#636e72'))
    
    def validate_input(self, title, genre, year, rating):
        if not title.strip():
            return False, "❌ Название не может быть пустым"
        
        if not year.isdigit():
            return False, "❌ Год должен быть числом"
        
        year_int = int(year)
        current_year = datetime.now().year
        if year_int < 1888 or year_int > current_year:
            return False, f"❌ Год должен быть между 1888 и {current_year}"
        
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                return False, "❌ Рейтинг должен быть от 0 до 10"
        except ValueError:
            return False, "❌ Рейтинг должен быть числом"
        
        return True, ""
    
    def add_movie(self):
        title = self.entries['title'].get()
        genre = self.entries['genre'].get()
        year = self.entries['year'].get()
        rating = self.entries['rating'].get()
        
        valid, message = self.validate_input(title, genre, year, rating)
        if not valid:
            messagebox.showerror("Ошибка валидации", message)
            self.update_status(message, 'error')
            return
        
        movie = {
            "title": title.strip(),
            "genre": genre.strip(),
            "year": int(year),
            "rating": float(rating)
        }
        
        self.movies.append(movie)
        self.save_movies()
        self.refresh_table()
        self.clear_inputs()
        
        success_msg = f"✅ Фильм '{title}' успешно добавлен!"
        messagebox.showinfo("Успех", success_msg)
        self.update_status(success_msg, 'success')
    
    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "⚠️ Выберите фильм для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот фильм?"):
            item = self.tree.item(selected[0])
            movie_title = item['values'][0]
            
            self.movies = [m for m in self.movies if m['title'] != movie_title]
            self.save_movies()
            self.refresh_table()
            
            success_msg = f"🗑️ Фильм '{movie_title}' удален"
            messagebox.showinfo("Успех", success_msg)
            self.update_status(success_msg, 'warning')
    
    def apply_filter(self):
        genre_filter = self.filter_genre.get().lower()
        year_filter = self.filter_year.get()
        
        filtered_movies = self.movies
        
        if genre_filter:
            filtered_movies = [m for m in filtered_movies 
                             if genre_filter in m['genre'].lower()]
        
        if year_filter:
            if year_filter.isdigit():
                filtered_movies = [m for m in filtered_movies 
                                 if m['year'] == int(year_filter)]
            else:
                messagebox.showwarning("Предупреждение", "⚠️ Год фильтрации должен быть числом")
                return
        
        self.refresh_table(filtered_movies)
        
        filter_msg = f"🔍 Найдено фильмов: {len(filtered_movies)}"
        self.update_status(filter_msg, 'info')
    
    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.refresh_table()
        self.update_status("🔄 Фильтры сброшены", 'info')
    
    def refresh_table(self, movies=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if movies is None:
            movies = self.movies
        
        for movie in movies:
            rating = movie['rating']
            if rating >= 7.5:
                tag = 'high_rating'
            elif rating >= 5.0:
                tag = 'medium_rating'
            else:
                tag = 'low_rating'
            
            self.tree.insert("", "end", values=(
                movie['title'],
                movie['genre'],
                str(movie['year']),
                f"★ {movie['rating']:.1f}"
            ), tags=(tag,))
        
        total_movies = len(movies)
        self.movie_count_label.config(text=f"{total_movies} фильмов")
    
    def clear_inputs(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries['title'].focus()
    
    def save_movies(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)
    
    def load_movies(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
                self.refresh_table()
                self.update_status(f"📂 Загружено {len(self.movies)} фильмов", 'info')
            except:
                self.movies = []
                self.update_status("⚠️ Ошибка загрузки файла", 'error')

def main():
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()

if __name__ == "__main__":
    main()