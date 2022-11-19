[![p2p Logo](https://github.com/ruankie/poly2pascal/blob/main/images/p2p_250_250.png)](https://github.com/ruankie/poly2pascal)

[![Install PyPI](https://img.shields.io/badge/install-pypi-brightgreen)](https://pypi.org/project/poly2pascal/)
[![API docs](https://img.shields.io/badge/docs-api-blue)](https://poly2pascal.github.io/)
[![GitHub contributors](https://img.shields.io/github/contributors/ruankie/poly2pascal)](https://github.com/ruankie/poly2pascal/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/ruankie/poly2pascal)](https://github.com/ruankie/poly2pascal/commits/main)
[![GitHub forks](https://img.shields.io/github/forks/ruankie/poly2pascal)](https://github.com/ruankie/poly2pascal/network)
[![GitHub stars](https://img.shields.io/github/stars/ruankie/poly2pascal)](https://github.com/ruankie/poly2pascal/stargazers)
[![GitHub license](https://img.shields.io/github/license/ruankie/poly2pascal)](https://github.com/ruankie/poly2pascal/blob/main/LICENSE)

# poly2pascal
Convert POLYGON bounding boxes from `.csv` files to `.xml` annotation files in the Pascal VOC format for computer vision projects. Read the package documentation [here](https://poly2pascal.github.io/).

## Installation
Install `poly2pascal` with pip
```bash
  pip install poly2pascal
```

## Usage
See the example notebook for more details. Here are the essentials of how to use this package:
```python
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
```

## Required Data Format
This package requires a `.csv` file with the following format of images and polygon annotations. These will be converted to `.xml` annotation files in the Pascal VOC format:

  | image_name | object_label | geometry                                                                                   |
  |------------|--------------|--------------------------------------------------------------------------------------------|
  | img_01.jpg | cat          | POLYGON ((2478.89 156.77, 2478.89 297.86, 2377.97 297.86, 2377.97 156.77, 2478.89 156.77)) |
  | img_02.jpg | cat          | POLYGON ((939.81 1221.46, 939.81 1319.68, 715.39 1319.68, 715.39 1221.46, 939.81 1221.46)) |
  | img_03.jpg | dog          | POLYGON ((1559.7 1558.06, 1559.7 1966.3, 1129.73 1966.3, 1129.73 1558.06, 1559.7 1558.06)) |


## Licence
* [MIT](https://github.com/ruankie/poly2pascal/blob/main/LICENSE)

## Authors
- [@ruankie](https://www.github.com/ruankie)

## TODO
- [x] pylint score >= 8.0
- [ ] add Sphinx docs
  - [ ] build static
  - [ ] link in readme
  - [ ] link in pypi
- [ ] add unit tests
- [ ] add github actions for automated testing
- [ ] add code coverage
- [ ] add logo and graphics

## References
- [Build python package](https://towardsdatascience.com/how-to-convert-your-python-project-into-a-package-installable-through-pip-a2b36e8ace10)