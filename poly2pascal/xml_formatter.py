import os
import cv2
import pandas as pd
import geopandas as gpd


# set base xml content for start and end of file
def get_start_str(
    folder, filename, path, width, height, depth=3, segmented=0, database="Unknown"
):
    """
    Get start of xml file that specifies image label in
    Pascal VOC format.
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


def get_xml_object_str(
    name,
    xmin,
    xmax,
    ymin,
    ymax,
    pose="Unspecified",
    truncated=0,
    difficult=0,
    occluded=0,
):
    """
    Return the populated object section of an image label in
    Pascal VOC format.
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


def get_image_xml_annotaion(
    image_data_path: str,
    image_name: str,
    image_sub_folder="",
    xml_end_content="\n</annotation>",
) -> str:
    """
    Return a string format of the xml contents
    with bounding box annotaions for a given image.
    """
    # open image to get image size
    im = cv2.imread(os.path.join(image_data_path, image_name))
    h, w, c = im.shape
    del im

    # get start of xml content
    xml_start_content = get_start_str(
        folder="", filename=image_name, path=image_data_path, width=w, height=h, depth=c
    )

    # get bounding box limits for each moth
    bounds_df = geo_df[geo_df["image_id"] == image_name]
    bounds_df = pd.concat([bounds_df, bounds_df.bounds], axis=1)

    # get object details
    object_details = bounds_df[["worm_type", "minx", "maxx", "miny", "maxy"]].values

    # populate list of strings of xml objects
    xml_object_strings = []
    for detail in object_details:
        xml_object_strings.append(
            get_xml_object_str(
                name=detail[0],
                xmin=detail[1],
                xmax=detail[2],
                ymin=detail[3],
                ymax=detail[4],
            )
        )

    # return final xml content
    final_xml_content_list = (
        [xml_start_content] + xml_object_strings + [xml_end_content]
    )
    final_xml_content = "".join(final_xml_content_list)
    return final_xml_content
