# RetroAchievements Yearly Stats Visualizer

Welcome to RA Yearly Stats! This Jupyter notebook is a window to your yearly RetroAchievements stats. Do you want to know how many games you beat this last year? How many achievements you got? Maybe how they are distributed among the consoles or which dev gave you the most achievements? You're in for a treat!

This is a project I started just for the fun of learning how to make API calls that ended up in what you see now. At some point I was happy enough with the shape it was taking to decide that it might be of interest to people other than me. Ever since I discovered RetroAchievements, I wanted to repay the community in some way for all of the free fun that it has given me, so take this as my little thank you to you all.

### Showcase example

Here's a sample of what you can expect from RA Yearly Stats, using my own results from 2024:

![First page](https://github.com/jorloru/RAYearlyStats/blob/main/images/example1.png)

![Second page](https://github.com/jorloru/RAYearlyStats/blob/main/images/example2.png)

![Third page](https://github.com/jorloru/RAYearlyStats/blob/main/images/example3.png)

![Fourth page](https://github.com/jorloru/RAYearlyStats/blob/main/images/example4.png)

### How to use

The application is set up to work using Binder, an online free service to run Jupyter notebooks like this program. You just need to hit the button below to be redirected to the Binder page which, after loading for a bit, will load the tool ready for use.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jorloru/RAYearlyStats/main?urlpath=%2Ftree%2Fsrc%2FRAYearlyStats.ipynb)

Once loaded, please read carefully both Instructions and Considerations sections to know how to use the tool and what to expect.

### What if I can't use Binder?

In case Binder isn't an option due to a huge amount of achievement data or because the service is down, I leave below the steps you need to follow in order to run the tool locally in your computer:

1) You will need to have both Python and Jupyter installed in your computer. If you require help with the installation of these programs, head below to the 'Installing and using Python and Jupyter' section.

2) Download the contents of the `src` folder. Place this files wherever you like but keep all of them in the same folder. You will also need to download the `requirements.txt` file.

3) Open a terminal and type `jupyter notebook` to open a Jupyter terminal in your browser.

4) Open the downloaded Jupyter Notebook `RAYearlyStats.ipynb` from the Jupyter terminal.

5) Follow the instructions that you will find within the Notebook under the tab Instructions. Please read the information listed under the Considerations tab as well.

### Installing and using Python and Jupyter

Here's a step by step installation of the necessary tools to run the code.

Please note that these steps are not unique as there is more than one way of installing Jupyter, but this section is meant to help the people who are not familiar with Python or Jupyter and need guidance with this process.

1) Download the recommended Python installer from https://www.python.org/downloads/.

2) Run the installer.

3) If you are installing on Windows, make sure to enable the checkbox labeled 'Add Python.exe to PATH' that will appear on the very first screen.

4) Follow the instructions on screen until the installation process is finished.

5) Open a terminal.

6) Type `python --version`. You should see a response similar to Python 3.x.y, with x and y being any numbers.

7) Type `pip install notebook`. This will install Jupyter Notebook.

8) Navigate to the folder where you have the `requirements.txt` file. You can navigate to a folder by typing `cd path`, where `path` refers to your folder path.

9) Type `pip install requirements.txt`. This will install all other necessary libraries.

10) Close the current terminal and open a new one. Type `jupyter notebook` to run Jupyter Notebook. This should open a new browser tab. Keep your terminal open until you are finished using Jupyter.

11) In Jupyter (the newly opened browser tab), navigate to the downloaded `src` folder.

12) Follow steps 4 and 5 from the previous section.