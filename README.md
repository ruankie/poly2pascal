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
- [ ] build and publish on pypi test
- [ ] build and publish to pypi
- [ ] format with black
- [ ] add badges to README
- [ ] show example of csv data schema
- [ ] fix docstrings

### Optional
- [ ] pylint score >= 8.0
- [ ] add Sphinx docs
- [ ] add unit tests
- [ ] add github actions for automated testing
- [ ] add code coverage