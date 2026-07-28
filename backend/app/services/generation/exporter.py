import io
import zipfile
from typing import Dict

class ArtifactExporter:
    def export_to_zip(self, files: Dict[str, str]) -> bytes:
        """Compress file mappings (relative_path -> content) into a zip memory stream."""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_path, content in files.items():
                zip_file.writestr(file_path, content)
        return zip_buffer.getvalue()

# Global exporter instance
artifact_exporter = ArtifactExporter()
