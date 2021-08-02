from final import init_app

"""Initialization from __init__.py"""
app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')