from app import create_app


app = create_app('config.development')

if __name__ == '__main__':
   # app.run(debug=True, use_reloader=False)  # had to put the use_reloader=False, because when app runs, it reloads and fills the database twice?
    app.run()
