[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poly2pascal)](https://pypi.org/project/poly2pascal/)
[![GitHub contributors](https://img.shields.io/github/contributors/ruankie/frontier-rl)](https://github.com/ruankie/frontier-rl/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/ruankie/frontier-rl)](https://github.com/ruankie/frontier-rl/commits/main)
[![GitHub forks](https://img.shields.io/github/forks/ruankie/frontier-rl)](https://github.com/ruankie/frontier-rl/network)
[![GitHub stars](https://img.shields.io/github/stars/ruankie/frontier-rl)](https://github.com/ruankie/frontier-rl/stargazers)
[![GitHub license](https://img.shields.io/github/license/ruankie/frontier-rl)](https://github.com/ruankie/frontier-rl/blob/main/LICENSE)

# poly2pascal
Convert POLYGON bounding boxes from `.csv` files to `.xml` annotation files in the Pascal VOC format for computer vision projects.

## Installation
Install `poly2pascal` with pip
```bash
  pip install poly2pascal
```

## Usage
See the example notebook for more details. Here are the essentials:
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

## Licence
* [MIT](./LICENSE)

## Authors
- [@ruankie](https://www.github.com/ruankie)

## TODO
### Essential
- [x] add jupyterlab to dev requirements
- [x] run through example notebook to ensure everythin works as expected
- [x] build and publish on pypi test
- [x] build and publish to pypi
- [ ] format with black
- [x] add badges to README
- [ ] show example of csv data schema
- [ ] fix docstrings

### Optional
- [ ] pylint score >= 8.0
- [ ] add Sphinx docs
- [ ] add unit tests
- [ ] add github actions for automated testing
- [ ] add code coverage

## References
- [Build python package](https://towardsdatascience.com/how-to-convert-your-python-project-into-a-package-installable-through-pip-a2b36e8ace10)