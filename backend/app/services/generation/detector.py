import os
from typing import List, Dict

class ProjectDetector:
    def detect_project_type(self, file_names: List[str]) -> Dict[str, str]:
        """Scrape folder file listings and determine package details."""
        files_set = set(file_names)
        
        if "package.json" in files_set:
            return {"language": "Node.js", "build_system": "npm", "docker_base": "node:20-alpine"}
        elif "requirements.txt" in files_set or "pyproject.toml" in files_set:
            return {"language": "Python", "build_system": "pip/poetry", "docker_base": "python:3.13-slim"}
        elif "go.mod" in files_set:
            return {"language": "Go", "build_system": "go modules", "docker_base": "golang:1.22-alpine"}
        elif "pom.xml" in files_set:
            return {"language": "Java", "build_system": "maven", "docker_base": "eclipse-temurin:21-jre-alpine"}
        elif "Cargo.toml" in files_set:
            return {"language": "Rust", "build_system": "cargo", "docker_base": "rust:1.78-slim"}
        return {"language": "generic", "build_system": "unknown", "docker_base": "alpine:latest"}

# Global detector instance
project_detector = ProjectDetector()
