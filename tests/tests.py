import os
import zipfile
from tkinter import filedialog, messagebox
import pandas as pd
from pandas.errors import (
    EmptyDataError,
    ParserError
)
from service_address_tracker.constants import SUPPORTED_FILE_EXTENSIONS

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
    quit(1)

# depending on the filetype, pandas has to read the file
# with different commands. If not compatible, an error is thrown.

df: pd.DataFrame = pd.DataFrame()

try:
    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    elif ext == ".csv":
        df = pd.read_csv(file_path)
except FileNotFoundError as e:
    messagebox.showerror("File Not Found Error", str(e))
    quit(1)
except PermissionError as e:
    messagebox.showerror("Permission Error", str(e))
    quit(1)
except IsADirectoryError as e:
    messagebox.showerror("Is a Directory Error", str(e))
    quit(1)
except UnicodeDecodeError as e:
    messagebox.showerror("Unicode Decode Error", str(e))
    quit(1)
except EmptyDataError as e:
    messagebox.showerror("Empty Data Error Error", str(e))
    quit(1)
except ParserError as e:
    messagebox.showerror("Parser Error", str(e))
    quit(1)
except ValueError as e:
    messagebox.showerror("Value Error", str(e))
    quit(1)
except ImportError as e:
    messagebox.showerror("Import Error", str(e))
    quit(1)
except zipfile.BadZipFile as e:
    messagebox.showerror("Excel Corruption Error", str(e))
    quit(1)
except OSError as e:
    messagebox.showerror("OS Error", str(e))
    quit(1)

df = df.filter([ # pyright: ignore[reportPossiblyUnboundVariable]
        "Service Address",
        "Type of Service Replacement (Project Category)",
        "C2M Status",
        "Date Checked in C2M",
        "Public Material",
        "Public Date of Material Confirmation",
        "Public Diameter",
        "Private Material",
        "Private Date of Material Confirmation",
        "Private Diameter",
        "Map Indy Year Built",
        "Meter Location",
        "Meter Location Notes"
        ], axis=1)

df["Meter Location Notes"] = df["Meter Location Notes"].fillna("test")
print(df)
# df.to_excel("test_file.xlsx")