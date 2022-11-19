"""
Tools for loading csv files containing polygon
bounding box information.
"""

import pandas as pd
import geopandas as gpd


class CSVLoader:
    """
    Class with methods for loading csv files
    containing polygon bounding box information.
    """

    def __init__(self, csv_file_path: str, geometry_col: str = "geometry") -> None:
        """
        Load csv files containing polygon bounding box information.

        Args:
            csv_file_path (str):
            Path to csv file that contains bounding box information.
            geometry_col (str): Column name containing POLYGON bounding box information.

        Returns:
            None
        """
        self.csv_file_path = csv_file_path
        self.geometry_col = geometry_col

    def load_data(self) -> gpd.GeoDataFrame:
        """
        Load csv files containing polygon bounding box information.

        Returns:
            gpd.GeoDataFrame: DataFrame with bounding box and image information.
        """
        # load data with geopandas
        pd_df = pd.read_csv(self.csv_file_path)
        geo_df = gpd.GeoDataFrame(
            pd_df.loc[:, [c for c in pd_df.columns if c != self.geometry_col]],
            geometry=gpd.GeoSeries.from_wkt(pd_df[self.geometry_col]),
        )

        return geo_df
