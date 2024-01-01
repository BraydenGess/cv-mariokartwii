from setuptools import setup,find_packages

setup(name='cv-mariokartwii',
      version = '1.0',
      description = 'Computer Vision MarioKart Wii Music and Stats',
      packages=find_packages(),
      py_modules=['train_models','tools/deep_learning','tools/imagemanipulation','tools/utility'])