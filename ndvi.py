import sys
import os
import numpy as np
import rasterio
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def NDVI(r: np.array, n: np.array) -> np.array:
    """The NDVI function.
    Args:
        r (np.array): Red band array
        n (np.array): NIR band array
    Returns:
        np.array: NDVI array
    """
    np.seterr(divide='ignore', invalid='ignore') # Ignore the divided by zero or Nan appears
    # BE CAREFULL! Without this convertion, doesn't work correctly !
    n = n.astype(rasterio.float32)
    r = r.astype(rasterio.float32)
    ndvi = (n - r) / (n + r) # The NDVI formula

    return ndvi

if __name__ == "__main__":
    Tk().withdraw()
    red_band_path = askopenfilename(title="Select the red band image", filetypes=[("TIFF files", "*.tif"), ("All files", "*.*")])
    
    if not red_band_path:
        print("Red band image is required.")
        sys.exit(-1)
    nir_band_path = askopenfilename(title="Select the NIR band image", filetypes=[("TIFF files", "*.tif"), ("All files", "*.*")])
    
    if not nir_band_path:
        print("NIR band image is required.")
        sys.exit(-1)

    output_directory = askdirectory(title="Select the directory to save the output image")
    if not output_directory:
        print("Output directory is required.")
        sys.exit(-1)

    output_file_name = input("Enter the output file name (default: NDVI.tif): ")
    if not output_file_name:
        output_file_name = "NDVI.tif"

    # Reading red band.
    red = rasterio.open(red_band_path, "r")
    red_array = red.read()
    metadata = red.meta.copy()
    
    # Reading NIR band
    nir = rasterio.open(nir_band_path, "r")
    nir_array = nir.read()

    # Calling the NDVI function.
    ndvi_array = NDVI(red_array, nir_array)
    
    # Updating metadata
    metadata.update({"driver": "GTiff", "dtype": rasterio.float32})        

    # Writing the NDVI raster with the same properties as the original data
    output_path = os.path.join(output_directory, output_file_name)
    with rasterio.open(output_path, "w", **metadata) as dst:
        if ndvi_array.ndim == 2:
            dst.write(ndvi_array, 1)
        else:
            dst.write(ndvi_array)