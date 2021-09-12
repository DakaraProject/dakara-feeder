from unittest import TestCase
from unittest.mock import patch

from path import Path
from yaml import YAMLError

from dakara_feeder.yaml_opener import (
    YamlContentInvalidError,
    YamlFileInvalidError,
    YamlFileNotFoundError,
    get_yaml_file_content,
)


@patch.object(Path, "text", autoset=True)
class GetYamlFileContentTestCase(TestCase):
    """Test the get_yaml_file_content function"""

    def test_get(self, mocked_text):
        """Test to get a YAML file"""
        # create the mock
        content = {"name": "tag1"}
        mocked_text.return_value = str(content)

        # call the method
        content_parsed = get_yaml_file_content(Path("path/to/file"))

        # assert the result
        self.assertDictEqual(content, content_parsed)

        # assert the call
        mocked_text.assert_called_with()

    def test_get_error_not_found(self, mocked_text):
        """Test to get a YAML file that does not exist"""
        # create the mock
        mocked_text.side_effect = FileNotFoundError()

        # call the method
        with self.assertRaisesRegex(
            YamlFileNotFoundError, "Unable to find YAML file 'path/to/file'"
        ):
            get_yaml_file_content(Path("path/to/file"))

    @patch("dakara_feeder.yaml_opener.yaml.load")
    def test_get_error_invalid(self, mocked_load, mocked_text):
        """Test to get an invalid YAML file"""
        # create the mock
        content = [{"name": "tag1"}]
        mocked_text.return_value = str(content)
        mocked_load.side_effect = YAMLError("error message")

        # call the method
        with self.assertRaisesRegex(
            YamlFileInvalidError,
            "Unable to parse YAML file 'path/to/file': error message",
        ):
            get_yaml_file_content(Path("path/to/file"))

    def test_get_key(self, mocked_text):
        """Test to get the key of a YAML file"""
        # create the mock
        content = {"tags": {"name": "tag1"}}
        mocked_text.return_value = str(content)

        # call the method
        content_parsed = get_yaml_file_content(Path("path/to/file"), "tags")

        # assert the result
        self.assertDictEqual(content["tags"], content_parsed)

        # assert the call
        mocked_text.assert_called_with()

    def test_get_key_error(self, mocked_text):
        """Test to get a invalid key of a YAML file"""
        # create the mock
        content = {"tags": {"name": "tag1"}}
        mocked_text.return_value = str(content)

        # call the method
        with self.assertRaisesRegex(
            YamlContentInvalidError,
            "Unable to find key 'other' in YAML file 'path/to/file'",
        ):
            get_yaml_file_content(Path("path/to/file"), "other")
