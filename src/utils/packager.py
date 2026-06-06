import shutil
import os
from src.core.config import settings

def package_app(build_dir="dist"):
    logger = settings.LOG_LEVEL # Simplification
    print(f"Packaging {settings.APP_NAME}...")
    
    # In real run: 
    # subprocess.run(["pyinstaller", "--onefile", "--windowed", "main.py"])
    
    # Mocking the packaging process
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    with open(f"{build_dir}/manifest.txt", "w") as f:
        f.write(f"App: {settings.APP_NAME}\nVersion: 1.0.0\nBuild: Mock")
    
    print(f"Build completed in {build_dir}")

if __name__ == "__main__":
    package_app()
