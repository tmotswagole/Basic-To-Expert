"""Entry point for the Python File Processor CLI.

This file will orchestrate the file processing application and hold the main menu loop.
"""

from __future__ import annotations

try:
    from .analyzer import analyze_file, filter_lines, normalize_lines, non_empty_lines, stream_lines
    from .backup import BackupOperation
    from .decorators import history
    from .exceptions import FileProcessorError
    from .models import format_size
    from .scanner import scan_directory, scan_summary
    from .snapshots import compare_snapshots, create_snapshot
except ImportError:
    from analyzer import analyze_file, filter_lines, normalize_lines, non_empty_lines, stream_lines
    from backup import BackupOperation
    from decorators import history
    from exceptions import FileProcessorError
    from models import format_size
    from scanner import scan_directory, scan_summary
    from snapshots import compare_snapshots, create_snapshot


def main() -> None:
    while True:
        print("========================================")
        print("       PYTHON FILE PROCESSOR")
        print("========================================")
        print("1. Scan directory")
        print("2. Analyze file")
        print("3. Create snapshot")
        print("4. Compare snapshots")
        print("5. Backup files")
        print("6. Stream file contents")
        print("7. View operation history")
        print("8. Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                snapshot = scan_directory(input("Directory: "))
                summary = scan_summary(snapshot)
                print(f"{summary['files']} files found")
                print(f"{format_size(summary['total_size'])} total")
                print(f"{summary['python_files']} Python files")
                print(f"{summary['text_files']} text files")
                print(f"{summary['other_files']} other files")
            elif choice == "2":
                analysis = analyze_file(input("File: "))
                for key, value in analysis.items():
                    print(f"{key}: {value}")
            elif choice == "3":
                print(f"Snapshot created: {create_snapshot(input('Directory: '))}")
            elif choice == "4":
                diff = compare_snapshots(input("Old snapshot: "), input("New snapshot: "))
                for label, files in diff.items():
                    print(label.upper())
                    for file in files:
                        print(f"  {file}")
            elif choice == "5":
                with BackupOperation(input("Source: "), input("Destination: ")) as backup:
                    print(f"Backed up {backup.copy()} files.")
            elif choice == "6":
                path = input("File: ")
                keyword = input("Filter keyword (blank for all): ").strip()
                lines = non_empty_lines(stream_lines(path))
                if keyword:
                    lines = filter_lines(lines, keyword)
                for line in normalize_lines(lines):
                    print(line)
            elif choice == "7":
                for item in history():
                    print(item)
            elif choice == "8":
                break
            else:
                print("Choose a valid option.")
        except (OSError, FileProcessorError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
