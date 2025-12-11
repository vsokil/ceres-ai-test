import rasterio
import matplotlib.pyplot as plt
from typing import Dict, Any


class RasterProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_summary(self) -> Dict[str, Any]:
        summary = {}

        with rasterio.open(self.file_path) as src:
            summary['width'] = src.width
            summary['height'] = src.height
            summary['num_bands'] = src.count
            summary['crs'] = src.crs.to_string() if src.crs else None
            summary['bounds'] = tuple(src.bounds)
            summary['pixel_size'] = (src.res[0], src.res[1])  # (x_res, y_res)

            first_band = src.read(1)
            summary['min_value'] = first_band.min()
            summary['max_value'] = first_band.max()

        return summary

    def plot_and_save_band(self, output_png: str, band: int = 1, cmap: str = 'gray') -> None:
        with rasterio.open(self.file_path) as src:
            data = src.read(band)

            plt.figure(figsize=(8, 8))
            plt.imshow(data, cmap=cmap)
            plt.colorbar(label="Pixel values")
            plt.title(f"{self.file_path} - Band {band}")
            plt.axis('off')
            plt.savefig(output_png, bbox_inches='tight', dpi=150)
            plt.close()
            print(f"Saved raster plot as '{output_png}'")
