import os
import cv2
import pandas as pd
import numpy as np
import glob
from poly2pascal.data_loader import CSVLoader


class XMLAnnotator:
    """
    Class wiht methods for getting xml annotations
    in Pascal VOC format.
    """

    def __init__(
        self,
        images_path: str,
        csv_file_path: str,
        image_name_col: str,
        image_label_col: str,
        xml_output_path: str,
        geometry_col: str = "geometry",
        xml_end_content: str = "\n</annotation>",
    ) -> None:
        """
        Constructs XMLAnnotator instance.

        Args:
            images_path (str): Path to where images are saved.
            csv_file_path (str): Path to csv file containing bounding box information.
            image_name_col (str): Column name containing names of unique images.
            image_label_col (str): Column name containing object labeles.
            xml_output_path (str): Path where xml annotation files will be saved to.
            geometry_col (str): Column name containing POLYGON bounding box information.
            xml_end_content (str): Content to end xml annotation file with.

        Returns:
            None
        """
        self.images_path = images_path
        self.csv_file_path = csv_file_path
        self.image_name_col = image_name_col
        self.image_label_col = image_label_col
        self.xml_output_path = xml_output_path
        self.geometry_col = geometry_col
        self.xml_end_content = xml_end_content
        self.data_loader = CSVLoader(csv_file_path, geometry_col)
        self.geo_df = self.data_loader.load_data()

    def _get_start_of_img_annotation(
        self,
        folder,
        filename,
        path,
        width,
        height,
        depth=3,
        segmented=0,
        database="Unknown",
    ) -> str:
        """
        Get start of xml file that specifies image label in
        Pascal VOC format. This has to happen for every new
        image.

        Args:
            folder (str): Folder where image is located.
            filename (sr): File name of image.
            path (str): Path to image.
            width (int): Image width in number of pixels.
            height (int): Image height in number of pixels.
            depth (int): Number of colour channels in image.
            segmented (int): Optional metadata for annotaion.
            database (str): Optional metadata for annotation.

        Returns:
            str: Start of XML annotation file.
        """

        xml_start_str = f"""<annotation>
        <folder>{folder}</folder>
        <filename>{filename}</filename>
        <path>{path}</path>
        <source>
            <database>{database}</database>
        </source>
        <size>
            <width>{width}</width>
            <height>{height}</height>
            <depth>{depth}</depth>
        </size>
        <segmented>{segmented}</segmented>"""

        return xml_start_str

    def _get_annotaion_for_object(
        self,
        name,
        xmin,
        xmax,
        ymin,
        ymax,
        pose="Unspecified",
        truncated=0,
        difficult=0,
        occluded=0,
    ) -> str:
        """
        Return the populated object section of an image label in
        Pascal VOC format. This has to heppen for each onject in
        an image.

        Args:
            name (str): Object label.
            xmin (float): Bounding box minimum x-value.
            xmax (float): Bounding box maximum x-value.
            ymin (float): Bounding box minimum y-value.
            ymax (float): Bounding box maximum y-value.
            pose (str): Optional metadata for annotation.
            truncated (int): Optional metadata for annotation.
            difficult (int): Optional metadata for annotation.
            occluded (int): Optional metadata for annotation.

        Returns:
            str: Annotation content of an object in the image.
        """

        object_xml = f"""
        <object>
            <name>{name}</name>
            <pose>{pose}</pose>
            <truncated>{truncated}</truncated>
            <difficult>{difficult}</difficult>
            <occluded>{occluded}</occluded>
            <bndbox>
                <xmin>{xmin}</xmin>
                <xmax>{xmax}</xmax>
                <ymin>{ymin}</ymin>
                <ymax>{ymax}</ymax>
            </bndbox>
        </object>"""

        return object_xml

    def _get_image_size(self, image_name: str) -> tuple:
        """
        Open image to get height, width, and number
        of colour channels. This has to happen for each
        new image.

        Args:
            image_name (str): Name of image.

        Returns:
            tuple: Tuple of image height, width, and number of colour channels.
        """
        im = cv2.imread(os.path.join(self.images_path, image_name))
        h, w, c = im.shape
        del im  # remove to reduce memory usage
        return h, w, c

    def _get_object_label_and_bbox_limits(self, image_name: str) -> np.ndarray:
        """
        Get bounding box limits and object name
        from loaded data. This is used later to 
        populate the Pascal VOC annotations.
        This has to happen for each onject in
        an image.

        Args:
            image_name (str): Name of image of interest for which to get object data.

        Returns:
            np.ndarray: Array of arrays with image height, width, and number of colour channels.
        """
        # get bounding box limits for each object
        bounds_df = self.geo_df[self.geo_df[self.image_name_col] == image_name]
        bounds_df = pd.concat([bounds_df, bounds_df.bounds], axis=1)

        # get object details
        object_details = bounds_df[
            [self.image_label_col, "minx", "maxx", "miny", "maxy"]
        ].values

        return object_details

    def _get_image_xml_annotaion(self, image_name: str) -> str:
        """
        Return a string format of the xml contents
        with bounding box annotaions for a given image.
        This has to be done for each image.

        Args:
            image_name (str): Name of image for which to get object annotations.

        Returns:
            str: Entire xml content that makes up the annotation of an image.
        """
        # get details to populate xml annotation with
        h, w, c = self._get_image_size(image_name)
        xml_start_content = self._get_start_of_img_annotation(
            folder="",
            filename=image_name,
            path=self.images_path,
            width=w,
            height=h,
            depth=c,
            segmented=0,
            database="Unknown",
        )
        object_details = self._get_object_label_and_bbox_limits(image_name)

        # populate list of strings of xml objects
        xml_object_strings = []
        for detail in object_details:
            xml_object_strings.append(
                self._get_annotaion_for_object(
                    name=detail[0],
                    xmin=detail[1],
                    xmax=detail[2],
                    ymin=detail[3],
                    ymax=detail[4],
                )
            )

        # return final xml content
        final_xml_content_list = (
            [xml_start_content] + xml_object_strings + [self.xml_end_content]
        )
        final_xml_content = "".join(final_xml_content_list)
        return final_xml_content

    def _write_to_xml_file(self, image_name: str, xml_content: str) -> None:
        """
        Create XML file with annotation content 
        at desired location.

        Args:
            image_name (str): Name of image for which to get object annotations.
            xml_content (str): XML annotation in Pascal VOC format.

        Returns:
            None
        """
        xml_file_path = os.path.join(
            self.xml_output_path, image_name.replace(".jpg", ".xml")
        )
        with open(xml_file_path, "w") as f_:
            f_.write(xml_content)

    def get_all_xml_annotations(self, img_format: str = ".jpg") -> None:
        """
        Get all annotations of images with given
        file format. XML annotation files will
        be saved with names correspoding to 
        image names.

        Args:
            img_format (str): Format of images to look for in images directory.

        Returns:
            None
        """
        # get all images in folder
        all_image_names = [
            os.path.basename(p) for p in glob.glob(f"{self.images_path}/*{img_format}")
        ]
        # get their xml anotations and save to file
        for img_name in all_image_names:
            xml_content = self._get_image_xml_annotaion(img_name)
            self._write_to_xml_file(img_name, xml_content)
