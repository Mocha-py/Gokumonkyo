
# Gokumonkyō

![alt text](https://mocha-existz.neocities.org/documentation/Gokumonkyō/icon.jpg)

Gokumonkyō is a python project designed to be able to encrypt any file so it is completely unable to be opened/read/understood without the generated key. This key is then used to decrypt the file to revert it to its previous state.

This program is inspired by the prison realm (Gokumonkyō) from Jujutsu Kaisen. I do not claim to own the rights to it or anything of the like those all belong to Gege Akutami.


## Usage

Please use the arrow keys to navigate the program, and use the space bar to select an option.
Move the files you wish to encrypt or decrypt into the "files" folder
If you are decrypting, please also insert your key into the key folder

## Features

- Encryption and decryption of files (clones file in the process, metadata is not kept.)
- Generation of a movable encryption key file which also contains the files that were encrypted with the key


## Warnings

- Encrypting new files when an encryption key file is already in the key folder WILL overwrite the key and the files encrypted by it WILL be lost PERMANENTLY.
- Removing the .gkmk extension from an encrypted file will mean it is NOT detected when attempting to decrypt it.
- Changing the name of key files or encrypted files will mean they are not detected.

Please move your keys after generating them, I am not responsible if you lose your files.
## Documentation

[Gokumonkyō Documentation](https://mocha-existz.neocities.org/documentation/Gokumonkyō/)


## Authors

- [@Mocha-py](https://github.com/Mocha-py)


## Acknowledgements

 - [Gege Akutami on X](https://twitter.com/jujutsuAkutami?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)
 - [Icon created by Sensei Chromosome](https://github.com/SenseiChromosome)



## Running Tests

To run tests, run the following command in cmd

```bash
  python -m unittest discover -s testing -p '*_test.py'
```

I've already ran all of these tests in vscode and they all returned OK, but I have left the tests in the repository anyway.

There are docstrings in the file containing the tests that explain what each test does.

Some functions have been manually tested by me using big bang testing.


## Installation

If you are trying to install the packages needed to run the python code, please run this command in the root directory of the program:

```bash
  python -m pip install -r requirements.txt
```

You should also delete the .gitkeep files in the files and key folders, but this isn't 100% necassary for functionality.
    
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Feedback

If you have any feedback, please email me at mochaexistz@gmail.com or use another contact method listed on my website.


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)  

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

