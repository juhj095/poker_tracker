import os
import glob
import tkinter as tk
from tkinter import filedialog

from db_helpers import get_connection
from xml_parser import xml_parser

def main():
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(title="Select folder containing XML files")

    if not folder_path:
        print("❌ No folder selected. Exiting...")
        return

    print(f"\n📂 Selected folder: {folder_path}\n")

    connection = get_connection()
    cursor = connection.cursor()

    for xml_file in glob.glob(os.path.join(folder_path, "*.xml")):
        try:
            xml_parser(cursor, xml_file)
            connection.commit()
        except Exception as e:
            print(f"❌ Error processing {xml_file}: {e}")
            connection.rollback()

    cursor.close()
    connection.close()
    print("🏁 All files processed")

if __name__ == "__main__":
    main()