from webapp import create_app

# Initialize Flask instance
app = create_app()

if __name__ == "__main__":
    # Run Flask app
    app.run(debug=True)
