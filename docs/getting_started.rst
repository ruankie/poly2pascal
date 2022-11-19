Getting Started
===============

Installation
------------

You can install `poly2pascal` using pip by running the following command

.. code-block::

       pip install poly2pascal

Usage
-----

Here is a simple example of how to use this `poly2pascal` for getting the object annotations from images as `.xml` files in the Pascal VOC format:

.. code-block::

      # import annotator
      from poly2pascal.annotations import XMLAnnotator

      # create annotator
      xmla = XMLAnnotator(
          images_path="path/to/images", 
          csv_file_path="path/to/csv/file.csv", 
          image_name_col="<image_name_column>",
          image_label_col="<object_label_column>", 
          xml_output_path="path/to/xml/annotation/output"
      )

      # create xml annotation files in Pascal VOC format
      xmla.get_all_xml_annotations(img_format=".jpg")

Required Data Format
--------------------

This package requires a `.csv` file with the following format of images and polygon annotations. These will be converted to `.xml` annotation files in the Pascal VOC format:

  +------------+--------------+--------------------------------------------------------------------------------------------+
  | image_name | object_label | geometry                                                                                   |
  +============+==============+============================================================================================+
  | img_01.jpg | cat          | POLYGON ((2478.89 156.77, 2478.89 297.86, 2377.97 297.86, 2377.97 156.77, 2478.89 156.77)) |
  +------------+--------------+--------------------------------------------------------------------------------------------+
  | img_02.jpg | cat          | POLYGON ((939.81 1221.46, 939.81 1319.68, 715.39 1319.68, 715.39 1221.46, 939.81 1221.46)) |
  +------------+--------------+--------------------------------------------------------------------------------------------+
  | img_03.jpg | dog          | POLYGON ((1559.7 1558.06, 1559.7 1966.3, 1129.73 1966.3, 1129.73 1558.06, 1559.7 1558.06)) |
  +------------+--------------+--------------------------------------------------------------------------------------------+
