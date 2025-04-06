import os
import pandas as pd

def load_and_merge_data(upload_dir):
    diary_path = os.path.join(upload_dir, 'diary.csv')
    ratings_path = os.path.join(upload_dir, 'ratings.csv')
    watched_path = os.path.join(upload_dir, 'watched.csv')

    if not os.path.exists(diary_path):
        print("❌ No diary.csv found.")
        return {}

    try:
        diary_df = pd.read_csv(diary_path)
        diary_df.rename(columns=lambda x: x.strip(), inplace=True)

        # Total movies watched (from watched.csv)
        watched_df = pd.read_csv(watched_path)
        watched_df.rename(columns=lambda x: x.strip(), inplace=True)
        total_movies = len(watched_df)

        # Convert diary dates
        diary_df['Watched Date'] = pd.to_datetime(diary_df['Watched Date'], errors='coerce')
        diary_df = diary_df.dropna(subset=['Watched Date'])
        diary_df = diary_df.sort_values('Watched Date')

        first_movie = diary_df.iloc[0]['Name'] if not diary_df.empty else None
        last_movie = diary_df.iloc[-1]['Name'] if not diary_df.empty else None

        # Longest streak of consecutive watch days
        dates = diary_df['Watched Date'].drop_duplicates().sort_values()
        streak, max_streak = 1, 1
        for i in range(1, len(dates)):
            if (dates.iloc[i] - dates.iloc[i - 1]).days == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1
        longest_streak = max_streak

        # Most rewatched movies
        rewatched_df = diary_df[diary_df['Rewatch'].str.lower() == 'yes']
        rewatched_counts = rewatched_df['Name'].value_counts() + diary_df['Name'].value_counts() - rewatched_df['Name'].value_counts()
        top_rewatched = [{'Name': name, 'Rewatch Count': count} for name, count in rewatched_counts.dropna().sort_values(ascending=False).head(10).items()]

        # Top 10 favorite movies from ratings.csv
                # Top 10 favorite movies from ratings.csv
        top_favorites = []
        highest_rated_decades = {}
        if os.path.exists(ratings_path):
            ratings_df = pd.read_csv(ratings_path)
            ratings_df.rename(columns=lambda x: x.strip(), inplace=True)
            ratings_df = ratings_df.dropna(subset=['Rating', 'Year'])

            # Top favorite 5-star movies
            top_favorites = ratings_df[ratings_df['Rating'] == 5][['Name', 'Rating']].drop_duplicates().head(10).to_dict(orient='records')

            # Highest rated decades
            ratings_df['Decade'] = (ratings_df['Year'] // 10) * 10
            decade_ratings = ratings_df.groupby('Decade')['Rating'].mean().round(2)
            highest_rated_decades = decade_ratings.sort_values(ascending=False).to_dict()


        # Tags
        if 'Tags' in diary_df.columns:
            tag_series = diary_df['Tags'].dropna().str.lower().str.split(',')
            tags = tag_series.explode().str.strip().value_counts().head(10)
            top_tags = [{'Tag': tag, 'Count': count} for tag, count in tags.items()]
        else:
            top_tags = []

        # Watch activity from diary
        watch_by_year = diary_df['Watched Date'].dt.year.value_counts().sort_index().to_dict()
        watch_by_month = diary_df['Watched Date'].dt.month.value_counts().sort_index().to_dict()
        watch_by_weekday = diary_df['Watched Date'].dt.day_name().value_counts().to_dict()

        # Watched.csv year activity
        # Watched.csv year activity from 'Year' column
        if 'Year' in watched_df.columns:
            watched_by_year = watched_df['Year'].value_counts().sort_index().to_dict()
        else:
            watched_by_year = {}


        return {
            'total_movies': total_movies,
            'first_movie': first_movie,
            'last_movie': last_movie,
            'longest_streak': longest_streak,
            'top_favorites': top_favorites,
            'most_rewatched': top_rewatched,
            'top_tags': top_tags,
            'watch_by_year': watch_by_year,
            'month_activity': watch_by_month,
            'weekday_activity': watch_by_weekday,
            'watched_by_year': watched_by_year,
            "highest_rated_decades":highest_rated_decades
        }

    except Exception as e:
        print("❌ Error reading CSV:", e)
        return {}
