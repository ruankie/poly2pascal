from unittest import TestCase, mock
import pytest
import pandas as pd
import numpy as np
import geopandas as gpd
from poly2pascal import data_loader, annotations


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
    def prepare_xml_annotator_instance(self):
        with mock.patch(
            "poly2pascal.data_loader.CSVLoader.load_data"
        ) as mock_csv_loader:
            pd_df = self.pandas_df_from_csv
            mock_geo_df = gpd.GeoDataFrame(
                pd_df.loc[:, [c for c in pd_df.columns if c != "geometry"]],
                geometry=gpd.GeoSeries.from_wkt(pd_df["geometry"]),
            )
            mock_csv_loader.return_value = mock_geo_df

            self.xml_annotator_instance = annotations.XMLAnnotator(
                images_path="path/to/images",
                csv_file_path="path/to/file.csv",
                image_name_col="image_name",
                image_label_col="object_label",
                xml_output_path="path/to/annotations",
                geometry_col="geometry",
                xml_end_content="\n</annotation>",
            )

        yield

    def test_constructor(self):
        assert self.xml_annotator_instance.images_path == "path/to/images"
        assert self.xml_annotator_instance.csv_file_path == "path/to/file.csv"
        assert self.xml_annotator_instance.image_name_col == "image_name"
        assert self.xml_annotator_instance.image_label_col == "object_label"
        assert self.xml_annotator_instance.xml_output_path == "path/to/annotations"
        assert self.xml_annotator_instance.geometry_col == "geometry"
        assert self.xml_annotator_instance.xml_end_content == "\n</annotation>"
        assert isinstance(
            self.xml_annotator_instance.data_loader, data_loader.CSVLoader
        )
        assert not self.xml_annotator_instance.geo_df.empty

    def test_get_start_of_img_annotation(self):
        xml_str = self.xml_annotator_instance._get_start_of_img_annotation(
            folder="some_folder",
            filename="some_file.name",
            path="some/path",
            width=800,
            height=500,
            depth=3,
            segmented=0,
            database="Unknown",
        )

        assert (
            xml_str
            == f"""<annotation>
        <folder>some_folder</folder>
        <filename>some_file.name</filename>
        <path>some/path</path>
        <source>
            <database>Unknown</database>
        </source>
        <size>
            <width>800</width>
            <height>500</height>
            <depth>3</depth>
        </size>
        <segmented>0</segmented>"""
        )

    def test_get_annotaion_for_object(self):
        xml_str = self.xml_annotator_instance._get_annotaion_for_object(
            name="some_name",
            xmin=123,
            xmax=423,
            ymin=55,
            ymax=120,
            pose="Unspecified",
            truncated=0,
            difficult=0,
            occluded=0,
        )

        assert (
            xml_str
            == f"""
        <object>
            <name>some_name</name>
            <pose>Unspecified</pose>
            <truncated>0</truncated>
            <difficult>0</difficult>
            <occluded>0</occluded>
            <bndbox>
                <xmin>123</xmin>
                <xmax>423</xmax>
                <ymin>55</ymin>
                <ymax>120</ymax>
            </bndbox>
        </object>"""
        )

    def test_get_object_label_and_bbox_limits(self):
        object_details = self.xml_annotator_instance._get_object_label_and_bbox_limits(
            image_name="img0.jpg"
        )
        matching = object_details == np.array(
            ["cat", 2377.97, 2478.89, 156.77, 297.86], dtype=object
        )
        assert matching.all()
