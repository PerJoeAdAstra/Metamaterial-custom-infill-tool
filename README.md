# Metamaterial-custom-infill-tool
A python program which takes in a set of points and returns a file which can be used with the Slic3r meta infill fork to create custom infills.

## SVG
Convert SVG's by using Sinhao's SVG path to points tool (Github: https://github.com/Shinao/PathToPoints - Online Converter: https://shinao.github.io/PathToPoints/) and saving the "all paths" section to a txt file and running it through the converter.

### Running from source
As this program can only currently be run from source. To run the program from source make sure that pysdl2 (https://pypi.org/project/PySDL2/) is installed in the location specified in the pythonpath in main '''os.environ["PYSDL2_DLL_PATH"] = "path/to/PySDL2-0.9.3"'''

### About
This project is written in python 2.7() and uses the pysdl2() library.
