# NAME: main
# AUTHOR: Patrick Cronin
# Date: 15/06/2025
# Update: 15/06/2025
# Purpose: Main Python file to run 'Facilities Asset Maintenance App' application from.
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)