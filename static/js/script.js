fetch('/data')
  .then(res => res.json())
  .then(data => {
    const stats = document.getElementById('stats');

    if (!data || Object.keys(data).length === 0) {
      stats.innerHTML = "<p>No data found 😢</p>";
      return;
    }

    // 📝 Summary
    stats.innerHTML = `
      <p>🎬 <strong>Total Movies Watched:</strong> ${data.total_movies}</p>
      <p>🥇 <strong>First movie:</strong> ${data.first_movie}</p>
      <p>🔚 <strong>Most recent:</strong> ${data.last_movie}</p>
      <p>🔥 <strong>Longest Streak:</strong> ${data.longest_streak} days</p>
    `;

    // ⭐ Top 10 favorites
    if (data.top_favorites.length > 0) {
      stats.innerHTML += "<h3>⭐ Top 10 Favorite Movies (by Rating)</h3>";
      data.top_favorites.forEach(movie => {
        stats.innerHTML += `<p>${movie.Name} — ${movie.Rating} ⭐</p>`;
      });
    }

    // 🔁 Most rewatched
    if (data.most_rewatched.length > 0) {
      stats.innerHTML += "<h3>🔁 Most Rewatched Movies</h3>";
      data.most_rewatched.forEach(movie => {
        stats.innerHTML += `<p>${movie.Name} — ${movie['Rewatch Count']} times</p>`;
      });
    }

    // 🏷️ Tags
    if (data.top_tags.length > 0) {
      stats.innerHTML += "<h3>🏷️ Top Tags</h3><p>";
      data.top_tags.forEach(tag => {
        stats.innerHTML += `${tag.Tag} (${tag.Count}) `;
      });
      stats.innerHTML += "</p>";
    }

    // 📊 Bar Charts
    renderBarChart('yearChart', 'Diary: Movies by Year', data.watch_by_year);
    renderBarChart('monthChart', 'Monthly Activity', data.month_activity);
    renderBarChart('weekdayChart', 'Weekday Activity', data.weekday_activity);
    renderBarChart('watchedYearChart', 'Watched.csv: Movies by Year', data.watched_by_year);
    renderBarChart("decadeChart", "Average Rating by Decade", data.highest_rated_decades);

  });

// 📊 Chart rendering function
function renderBarChart(id, label, data) {
  const ctx = document.getElementById(id).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: label,
        data: Object.values(data),
        backgroundColor: '#4e79a7'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}
