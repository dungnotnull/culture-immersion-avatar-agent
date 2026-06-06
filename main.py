from src.main_app import CultureImmersionApp

if __name__ == "__main__":
    app = CultureImmersionApp()
    # In production, this path would be determined by the File Watcher or User Selection
    try:
        app.load_file("test.srt") 
    except Exception:
        pass
    app.run()
