<p align="center">
    <img src="./media/OOP_POINTS.png" alt="logo" width="800" height="373">
</p>

# Assignment 3

Assignment 3 for the course Object-Oriented Programming written and programmed by Ofri Tavor and Nir Sasson.

## Overview
In this project we were tasked to port from Java our [Assignment 2](https://github.com/SassonNir/OOP-Ex2) where we were given an API defined using interfaces to implement all the interfaces.

## Getting started

### Clone the repositorty
Enter your IDE and clone the repository:

```sh
git clone https://github.com/Unusual55/OOP-Ex3.git
```

### Prerequisites

Enter the terminal in your IDE and install the next commands in order to install the required modules:

```git
pip install -r requirements.txt
```

### Usage

In order to run the program enter the following in your terminal:

```sh
cd path/to/src/folder
python main.py
```

Note that the `cd` is important since the main uses relative paths.  

In order to run the GUI enter the following in your terminal:

```sh
python path/to/Gui/folder/GuiPanel.py 
```

## Documentation

For more information and details about the structure and background of the project please refer to the [Wiki Pages](../../wiki).

## Comparison and Stats

These results ran on a laptop with the following CPU: AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx (8 CPUs), ~2.1 GHz, 12 GB RAM.

### Shortest Path

![Shortest Path Graph](./media/SHORTESTPATH_SMALLGRAPHS.png)

### Centre

![Centre Graph](./media/CENTRE_SMALLGRAPHS.png)

### TSP

![TSP Graph](./media/TSP_SMALLGRAPHS.png)

### Results

Some graphs may be misleading since the in the larger graphs that are not shown in the images above, the algorithm is taking much longer to run in Python than in Java.
You can see the more detailed results in the file [Comparison Excel file](https://github.com/Unusual55/OOP-Ex3/blob/main/media/Comparison.xlsx).

In the smaller graphs Python seems to be faster than Java, 
but when the graphs are larger the difference is much more profound in the way that Java is more consistent.
