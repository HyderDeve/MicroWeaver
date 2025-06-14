import os
import shutil
from pathlib import Path
from typing import Dict
import zipfile

class ProjectGenerator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    async def create_directory_structure(self):
        """Create the basic directory structure for the microservice"""
        directories = [
            self.base_path / 'app' / 'routes',
            self.base_path / 'app' / 'models',
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    async def create_files(self, template_data: Dict[str, str]):
        """Create all necessary files with provided templates"""
        files = {
            self.base_path / 'app' / 'main.py': template_data.get('main_py', ''),
            self.base_path / 'app' / '__init__.py': '',
            self.base_path / 'app' / 'routes' / '__init__.py': '',
            self.base_path / 'app' / 'models' / '__init__.py': '',
            self.base_path / 'requirements.txt': template_data.get('requirements_txt', ''),
            self.base_path / 'Dockerfile': template_data.get('dockerfile', ''),
            self.base_path / 'README.md': template_data.get('readme_md', '')
        }
        
        for file_path, content in files.items():
            file_path.write_text(content)

    async def zip_project(self) -> str:
        """Zip the generated project and return the zip file path"""
        zip_path = str(self.base_path) + '.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(str(self.base_path)):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, str(self.base_path))
                    zipf.write(file_path, arcname)
        return zip_path

    async def cleanup(self):
        """Clean up generated files after zipping"""
        if self.base_path.exists():
            shutil.rmtree(str(self.base_path))