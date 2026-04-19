# Minecraft Inventory Management System

## Project Overview
This project is a Minecraft-themed inventory management system built in Python using Tkinter for the GUI. It lets users manage items like tools, blocks, food, and weapons in a simple interface.
Users can add, update, remove, search, and sort items. All prices are shown in gold ingots.

## How to run it

1. Make sure you have Python installed (Python 3 is fine)
2. Download or open the project folder
3. Open a terminal in that folder
4. Run:

python main.py

Or just run main.py in VS Code using the run button.

No extra libraries are needed, everything used (like tkinter) is built into Python.

## How to use it

When you open the app, you’ll see a form at the top and a table of items below.

- **Add Item**: Fill out all fields and click “Add Item”
- **Update Item**: Click an item in the table, edit the fields, then click “Update Item”
- **Remove Item**: Enter or select an item ID and click “Remove Item”
- **Search**:
  - By ID → enter ID and click “Search ID”
  - By Name → enter part of a name and click “Search Name”
  - By Category → enter a category and click “Search Category”
- **Sort**: Choose name, price, or quantity and click “Sort”
- **Show All Items**: Resets the table to show everything

There are already sample Minecraft items loaded in when the program starts so you can test it quickly.

## How it works

We used three main data structures:

- A **list** to store all items and display them
- A **dictionary (hash table)** to quickly find items by ID
- A **binary search tree** to sort items by name, price, or quantity

## Notes
- Item IDs have to be unique
- Prices are stored as gold ingots (Minecraft theme)
- If something doesn’t work, just restart the program and try again

## Authors
- Gigi Germanski: gigigermanski@oakland.edu
- Natalie Muscas: nataliemuscas@oakland.edu
- Kenny Hartwell: kchartwell@oakland.edu
