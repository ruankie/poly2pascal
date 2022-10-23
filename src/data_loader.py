import pandas as pd
import geopandas as gpd

class CSVLoader():
    def __init__(self, csv_file_path: str, image_name_col:str, geometry_col:str = "geometry") -> None:
        """
        Load csv files containing polygon bounding box information.
    
        Args:
            csv_file_path (str): Path to csv file.
            image_name_col (str): Column name containing names of unique images.
            geometry_col (str): Column name containing POLYGON bounding box information.
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
            # crs="epsg:3005",
        )