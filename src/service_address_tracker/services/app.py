"""

Tkinter GUI app

"""
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Tk
from service_address_tracker.constants import SUPPORTED_FILE_EXTENSIONS
from service_address_tracker.services.asset_manager import build_assets
from pandas.errors import (
    EmptyDataError,
    ParserError
)
import zipfile


class App:
    """
    
    The main app object that will run inside the Tkinter environment.
    """
    def __init__(self, root: Tk) -> None:
        """Initializes the app object class

        Args:
            root (Tk): the root Tkinter object
            
        Returns:
            None
        """
        
        # Initialize Tkinter window
        self.root = root
        self.root.title("Service Address Tracker")
        self.root.geometry("350x125")
        
        # Pop up the window to the top
        self.root.attributes("-topmost", True)
        self.root.lift()
        self.root.attributes("-topmost", False)
        
        # initialize dataframe object
        self.df = None
        
        # Populate the window to show whether the file has been selected,
        # and the button to select the file
        self.file_label = tk.Label(self.root, text="No file selected")
        self.file_label.pack(padx=10, pady=5)
        self.file_button = tk.Button(
            root,
            text="Choose file...",
            command=self.load_file
        )
        self.file_button.pack(padx=10, pady=5)

        # once the file has been properly selected, the user can
        # import the assets into the asset builder
        self.run_button = tk.Button(
            root,
            text="Process Assets",
            command=self.run_import
        )
        self.run_button.pack(padx=10, pady=15)
    
    def load_file(self) -> None:
        """

        Prompts the user for a proper file to be loaded into the program,
        then reads and converts the data into a pandas DataFrame. Informs the
        user if the reading of the file had an error.

        Returns:
            None
        """
        file_path: str = filedialog.askopenfilename(
            filetypes=[
                ("All supported filetypes", SUPPORTED_FILE_EXTENSIONS),
                ("Excel Files", SUPPORTED_FILE_EXTENSIONS[0:-1]),
                ("CSV Files", SUPPORTED_FILE_EXTENSIONS[-1])
            ]
        )

        # grabs the extension of the selected file to later check if it
        # is a compatible filetype
        ext = os.path.splitext(file_path)[1].lower()

        # end the file loading if no file was selected
        if not file_path:
            return

        # depending on the filetype, pandas has to read the file
        # with different commands. If not compatible, an error is thrown.
        try:
            if ext in [".xlsx", ".xls"]:
                self.df = pd.read_excel(file_path)
            elif ext == ".csv":
                self.df = pd.read_csv(file_path)
        except FileNotFoundError as e:
            messagebox.showerror("File Not Found Error", str(e))
            return
        except PermissionError as e:
            messagebox.showerror("Permission Error", str(e))
            return
        except IsADirectoryError as e:
            messagebox.showerror("Is a Directory Error", str(e))
            return
        except UnicodeDecodeError as e:
            messagebox.showerror("Unicode Decode Error", str(e))
            return
        except EmptyDataError as e:
            messagebox.showerror("Empty Data Error Error", str(e))
            return
        except ParserError as e:
            messagebox.showerror("Parser Error", str(e))
            return
        except ValueError as e:
            messagebox.showerror("Value Error", str(e))
            return
        except ImportError as e:
            messagebox.showerror("Import Error", str(e))
            return
        except zipfile.BadZipFile as e:
            messagebox.showerror("Excel Corruption Error", str(e))
            return
        except OSError as e:
            messagebox.showerror("OS Error", str(e))
            return

        # updates the label with the file path to show the user that the file
        # was properly selected.
        self.file_label.config(text=file_path)
        
    def run_import(self) -> None:
        """

        Executed when the user clicks the "Import Assets" button. Sends the
        DataFrame to the asset_builder, then filters out any assets that have
        invalid conditions as defined in the constants file. Once completed,
        prompts the user to save the resulting file.

        Returns:
            None
        """

        # does not proceed if no file was selected already
        if self.df is None:
            messagebox.showwarning(
                "Warning",
                "Load an Excel or CSV file first!"
            )
            return

        assets = build_assets(self.df)
        print(assets)
