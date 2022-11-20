from unittest import TestCase, mock
import pytest
import pandas as pd
import geopandas as gpd
from poly2pascal import data_loader


class TestDataLoader(TestCase):
    @pytest.fixture(autouse=True)
    def prepare_pandas_df_from_csv(self):
        self.pandas_df_from_csv = pd.DataFrame(
            {
                "image_name": {
                    0: "img0.jpg",
                    1: "img1.jpg",
                    2: "img2.jpg",
                    3: "img3.jpg",
                    4: "img4.jpg",
                },
                "object_label": {0: "cat", 1: "cat", 2: "dog", 3: "dog", 4: "cat"},
                "geometry": {
                    0: "POLYGON ((2478.89 156.77, 2478.89 297.86, 2377.97 297.86, 2377.97 156.77, 2478.89 156.77))",
                    1: "POLYGON ((939.81 1221.46, 939.81 1319.68, 715.39 1319.68, 715.39 1221.46, 939.81 1221.46))",
                    2: "POLYGON ((1559.7 1558.06, 1559.7 1966.3, 1129.73 1966.3, 1129.73 1558.06, 1559.7 1558.06))",
                    3: "POLYGON ((2090.21 1537.21, 2090.21 1799.81, 1743.67 1799.81, 1743.67 1537.21, 2090.21 1537.21))",
                    4: "POLYGON ((2342.25 1676.30, 2342.25 1952.26, 2162.13 1952.26, 2162.13 1676.30, 2342.25 1676.30))",
                },
            }
        )

        yield

    @pytest.fixture(autouse=True)
    def prepare_csv_loader_instance(self):
        self.csv_loader_instance = data_loader.CSVLoader(
            csv_file_path="path/to/file.csv", geometry_col="geometry"
        )

        yield

    def test_constructor(self):
        assert self.csv_loader_instance.csv_file_path == "path/to/file.csv"
        assert self.csv_loader_instance.geometry_col == "geometry"

    @mock.patch("poly2pascal.data_loader.pd.read_csv")
    def test_load_data(self, mock_read_csv):
        mock_read_csv.return_value = self.pandas_df_from_csv
        geo_df = self.csv_loader_instance.load_data()
        assert geo_df.columns.to_list() == ["image_name", "object_label", "geometry"]
        assert isinstance(geo_df, gpd.GeoDataFrame)
