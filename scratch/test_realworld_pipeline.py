import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path("c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend")))

from api_doc_generator.services.local_code_service import LocalCodeService
from api_doc_generator.extractors.extraction_pipeline import ExtractionPipeline
from api_doc_generator.scanner.backend_detector import BackendFileDetector, FrameworkCandidateDetector

repo_path = "c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/scratch/laravel-realworld"
file_contents, read_errors = LocalCodeService.collect_from_folder(repo_path)
tree_entries = [
    {"path": f.get("path"), "size": f.get("size", len(f.get("content", "")))}
    for f in file_contents
    if f.get("path")
]

print(f"Total files collected: {len(file_contents)}")

detector = BackendFileDetector()
backend_file_entries = detector.find_backend_files(tree_entries)
backend_file_paths = {entry.get("path") for entry in backend_file_entries}

print(f"Backend files detected: {len(backend_file_paths)}")
print("Paths:")
for p in sorted(backend_file_paths)[:10]:
    print(f"  {p}")

frameworks = FrameworkCandidateDetector.detect(backend_file_entries)
print(f"Detected frameworks: {frameworks}")

pipeline_files = [
    {"path": f.get("path"), "content": f.get("content", "")}
    for f in file_contents
    if f.get("path") in backend_file_paths
]

pipeline = ExtractionPipeline(batch_size=50)
pipeline.add_files(pipeline_files)
endpoints, errors, stats = pipeline.run()

print(f"Extraction stats: {stats}")
print(f"Extracted {len(endpoints)} endpoints:")
for ep in endpoints[:10]:
    print(f"  {ep['method']} {ep['path']} -> {ep.get('function_name')}")
