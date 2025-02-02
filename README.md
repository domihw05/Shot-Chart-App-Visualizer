# Shot-Chart-App-Visualizer
Scrape data off of Understat website and create shot chart and statistical visualizations.

**GOAL:** Use Understats website to scrape player shot data. Then, use that shot data to create a shto chart visualization, including relevant statistics.

**FILES:**
*** playerShotChartApp**

Scrapes online data, processes it, and output player visualization into app window.

*** playerShotChartVisualizer**

Scrapes online data, processes it, and saves player visualization into image called player_visualization.png.

**HOW TO USE:**
*** playerShotChartApp**

Run "python playerShotChartApp.py". This opens a window where you must input a player's ID according to the Understat database. Mohamed Salah's player ID, for example, is 1250. Then, you can select which season you want the data to be from (2000-2024 or All). This will then print the visualization in the window.

*** playerShotChartVisualizer**

Run "python playerShotChartVisualizer.py". The terminal will prompt you to input a player's ID according to the Understat database. Mohamed Salah's player ID, for example, is 1250. This will then save the player's career shot chart and statistics to _player_visualization.png_.

