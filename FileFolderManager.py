import os
import shutil
from pathlib import Path


class FileManager:
    def __init__(self, default_directory: str = '/home/lind/'):
        self.current_directory = Path(default_directory).expanduser()
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        """Ensure the current directory exists, create if necessary"""
        try:
            self.current_directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"⚠️ Error accessing directory: {e}")
            self.current_directory = Path.home()
            print(f"⚠️ Defaulting to home directory: {self.current_directory}")

    def change_directory(self, new_directory: str) -> bool:
        """Change the current working directory"""
        try:
            new_path = Path(new_directory).expanduser().absolute()
            if new_path.is_dir():
                self.current_directory = new_path
                print(f"✅ Changed directory to: {self.current_directory}")
                return True
            print(f"❌ Directory not found: {new_directory}")
            return False
        except Exception as e:
            print(f"❌ Error changing directory: {e}")
            return False

    def create_file(self) -> bool:
        """Create a new file in current directory"""
        try:
            file_name = input("Enter file name (with extension): ").strip()
            if not file_name:
                print("❌ File name cannot be empty")
                return False

            file_path = self.current_directory / file_name

            if file_path.exists():
                print(f"⚠️ File already exists: {file_name}")
                return False

            file_path.touch()
            print(f"✅ Created file: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return False

    def create_folder(self) -> bool:
        """Create a new folder in current directory"""
        try:
            folder_name = input("Enter folder name: ").strip()
            if not folder_name:
                print("❌ Folder name cannot be empty")
                return False

            folder_path = self.current_directory / folder_name

            if folder_path.exists():
                print(f"⚠️ Folder already exists: {folder_name}")
                return False

            folder_path.mkdir()
            print(f"✅ Created folder: {folder_path}")
            return True
        except Exception as e:
            print(f"❌ Error creating folder: {e}")
            return False

    def list_directory(self) -> bool:
        """List contents of current directory"""
        try:
            print(f"\n📂 Contents of {self.current_directory}:")
            print("-" * 60)

            items = sorted(os.listdir(self.current_directory))
            if not items:
                print("(empty)")
                return True

            for item in items:
                full_path = self.current_directory / item
                if full_path.is_dir():
                    print(f"📁 {item}/")
                else:
                    print(f"📄 {item}")
            print("-" * 60)
            return True
        except Exception as e:
            print(f"❌ Error listing directory: {e}")
            return False

    def delete_item(self, is_folder: bool = False) -> bool:
        """Delete a file or folder"""
        try:
            item_name = input(f"Enter {'folder' if is_folder else 'file'} name: ").strip()
            if not item_name:
                print("❌ Name cannot be empty")
                return False

            item_path = self.current_directory / item_name

            if not item_path.exists():
                print(f"❌ {'Folder' if is_folder else 'File'} not found: {item_name}")
                return False

            if is_folder:
                if not item_path.is_dir():
                    print(f"❌ Not a folder: {item_name}")
                    return False
                shutil.rmtree(item_path)
            else:
                if not item_path.is_file():
                    print(f"❌ Not a file: {item_name}")
                    return False
                item_path.unlink()

            print(f"✅ Deleted {'folder' if is_folder else 'file'}: {item_name}")
            return True
        except Exception as e:
            print(f"❌ Error deleting {'folder' if is_folder else 'file'}: {e}")
            return False

    def rename_item(self) -> bool:
        """Rename a file or folder"""
        try:
            old_name = input("Enter current name: ").strip()
            if not old_name:
                print("❌ Current name cannot be empty")
                return False

            old_path = self.current_directory / old_name

            if not old_path.exists():
                print(f"❌ Item not found: {old_name}")
                return False

            new_name = input("Enter new name: ").strip()
            if not new_name:
                print("❌ New name cannot be empty")
                return False

            new_path = self.current_directory / new_name

            if new_path.exists():
                print(f"⚠️ Item already exists: {new_name}")
                return False

            old_path.rename(new_path)
            print(f"✅ Renamed '{old_name}' to '{new_name}'")
            return True
        except Exception as e:
            print(f"❌ Error renaming item: {e}")
            return False

    def move_item(self) -> bool:
        """Move a file or folder to another location"""
        try:
            item_name = input("Enter item name to move: ").strip()
            if not item_name:
                print("❌ Item name cannot be empty")
                return False

            source_path = self.current_directory / item_name

            if not source_path.exists():
                print(f"❌ Item not found: {item_name}")
                return False

            destination = input("Enter destination path: ").strip()
            if not destination:
                print("❌ Destination cannot be empty")
                return False

            dest_path = Path(destination).expanduser().absolute()

            if not dest_path.is_dir():
                print(f"❌ Destination is not a directory: {destination}")
                return False

            shutil.move(str(source_path), str(dest_path))
            print(f"✅ Moved '{item_name}' to '{dest_path}'")
            return True
        except Exception as e:
            print(f"❌ Error moving item: {e}")
            return False


def main():
    print("📁 File and Folder Manager")
    print("=" * 40)

    manager = FileManager()

    while True:
        print(f"\nCurrent directory: {manager.current_directory}")
        print("\nMenu:")
        print("1. Create File")
        print("2. Create Folder")
        print("3. List Directory Contents")
        print("4. Delete File")
        print("5. Delete Folder")
        print("6. Rename File/Folder")
        print("7. Move File/Folder")
        print("8. Change Directory")
        print("9. Exit")

        try:
            choice = input("\nEnter your choice (1-9): ").strip()

            if choice == '1':
                manager.create_file()
            elif choice == '2':
                manager.create_folder()
            elif choice == '3':
                manager.list_directory()
            elif choice == '4':
                manager.delete_item(is_folder=False)
            elif choice == '5':
                manager.delete_item(is_folder=True)
            elif choice == '6':
                manager.rename_item()
            elif choice == '7':
                manager.move_item()
            elif choice == '8':
                new_dir = input("Enter new directory path: ").strip()
                manager.change_directory(new_dir)
            elif choice == '9':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number 1-9.")

            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user.")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == '__main__':
    main()