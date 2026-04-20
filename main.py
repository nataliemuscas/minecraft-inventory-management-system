import tkinter as tk
from tkinter import ttk, messagebox


# =========================================================
# ITEM CLASS
# =========================================================
# This class represents one inventory item in our Minecraft-themed store.
# We chose fields that make sense for a store system and also make it easy
# to demonstrate different data structure operations.
#
# Fields:
# - item_id: unique identifier for fast searching
# - name: item name, such as Diamond Sword or Oak Planks
# - category: broad grouping like Weapon, Block, Food, Tool
# - price_gold: price measured in gold ingots
# - quantity: how many of that item are currently in inventory
#
# We chose Minecraft items because they are recognizable, fun to demo,
# and still behave like normal store items in an inventory system.
# =========================================================

class Item:
    def __init__(self, item_id, name, category, price_gold, quantity):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price_gold = price_gold
        self.quantity = quantity

    def to_tuple(self):
        """Returns item data in tuple form for displaying in the GUI table."""
        return (
            self.item_id,
            self.name,
            self.category,
            f"{self.price_gold} gold ingots",
            self.quantity
        )

    def __str__(self):
        """Readable string version for debugging or console output if needed."""
        return (
            f"ID: {self.item_id} | "
            f"Name: {self.name} | "
            f"Category: {self.category} | "
            f"Price: {self.price_gold} gold ingots | "
            f"Quantity: {self.quantity}"
        )


# =========================================================
# BINARY SEARCH TREE NODE
# =========================================================
# Each BST node stores:
# - item: the actual inventory item
# - key: the value we are sorting by (name, price, or quantity)
# - left / right children
#
# We use a BST because the assignment specifically mentions binary search trees
# for sorting items by values like price or name.
# =========================================================

class BSTNode:
    def __init__(self, item, key):
        self.item = item
        self.key = key
        self.left = None
        self.right = None


# =========================================================
# BINARY SEARCH TREE
# =========================================================
# This BST is built temporarily whenever the user wants to sort items.
# We support sorting by:
# - name
# - price
# - quantity
#
# Important note:
# We rebuild the BST from the list whenever sorting is requested.
# This keeps the program simpler and avoids having to constantly maintain
# multiple permanent BSTs after every update.
# =========================================================

class BinarySearchTree:
    def __init__(self, sort_by="price"):
        self.root = None
        self.sort_by = sort_by

    def get_key(self, item):
        """Selects the correct comparison key based on the requested sort field."""
        if self.sort_by == "name":
            return item.name.lower()
        elif self.sort_by == "price":
            return item.price_gold
        elif self.sort_by == "quantity":
            return item.quantity
        else:
            return item.name.lower()

    def insert(self, item):
        """Public insert function."""
        key = self.get_key(item)
        self.root = self._insert_recursive(self.root, item, key)

    def _insert_recursive(self, node, item, key):
        """
        Recursively inserts a new item into the BST.
        Smaller keys go left, larger or equal keys go right.
        """
        if node is None:
            return BSTNode(item, key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, item, key)
        else:
            node.right = self._insert_recursive(node.right, item, key)

        return node

    def inorder_traversal(self):
        """
        Returns items in sorted order by using in-order traversal:
        left -> root -> right
        """
        items = []
        self._inorder_recursive(self.root, items)
        return items

    def _inorder_recursive(self, node, items):
        """Recursive helper for in-order traversal."""
        if node is not None:
            self._inorder_recursive(node.left, items)
            items.append(node.item)
            self._inorder_recursive(node.right, items)


# =========================================================
# INVENTORY SYSTEM
# =========================================================
# This is the main logic class.
#
# Data Structures Used:
# 1. self.items_list
#    - Python list
#    - Stores every item in the inventory
#    - Good for displaying all items and rebuilding the BST
#
# 2. self.items_dict
#    - Python dictionary (hash table)
#    - Maps item_id -> item object
#    - Allows fast average O(1) searching by ID
#
# 3. BinarySearchTree
#    - Built when a sorted view is needed
#    - Lets us show sorted items by name, price, or quantity
#
# We combine structures because no single structure does everything best:
# - List is easy for traversal
# - Hash table is fast for searching
# - BST gives sorted structure
# =========================================================

class InventorySystem:
    def __init__(self):
        self.items_list = []
        self.items_dict = {}

    def add_item(self, item):
        """
        Adds a new item to both major storage structures:
        - list for traversal/display
        - dictionary for fast ID lookup

        Returns:
            (True, message) on success
            (False, message) on failure
        """
        if item.item_id in self.items_dict:
            return False, "An item with that ID already exists."

        self.items_list.append(item)
        self.items_dict[item.item_id] = item
        return True, "Item added successfully."

    def remove_item(self, item_id):
        """
        Removes an item from both the dictionary and the list.
        Dictionary removal is fast.
        List removal requires finding the object and removing it.
        """
        if item_id not in self.items_dict:
            return False, "Item not found."

        item = self.items_dict[item_id]
        self.items_list.remove(item)
        del self.items_dict[item_id]
        return True, "Item removed successfully."

    def update_item(self, item_id, name, category, price_gold, quantity):
        """
        Updates an existing item's fields.
        We do not need to replace the object in the list or dictionary because
        both structures reference the same item object.
        """
        if item_id not in self.items_dict:
            return False, "Item not found."

        item = self.items_dict[item_id]
        item.name = name
        item.category = category
        item.price_gold = price_gold
        item.quantity = quantity
        return True, "Item updated successfully."

    def search_by_id(self, item_id):
        """
        Uses the dictionary (hash table) for fast ID lookup.
        Average time complexity is O(1).
        """
        return self.items_dict.get(item_id, None)

    def search_by_name(self, name):
        """
        Searches by name.
        Since our dictionary is keyed by ID, name searching is done by scanning
        the list.
        """
        results = []
        for item in self.items_list:
            if name.lower() in item.name.lower():
                results.append(item)
        return results

    def search_by_category(self, category):
        """Returns all items whose category matches the given text."""
        results = []
        for item in self.items_list:
            if category.lower() in item.category.lower():
                results.append(item)
        return results

    def get_all_items(self):
        """Returns all items in insertion order."""
        return self.items_list

    def get_sorted_items(self, sort_by):
        """
        Builds a BST from the list and returns items in sorted order.
        """
        bst = BinarySearchTree(sort_by)
        for item in self.items_list:
            bst.insert(item)
        return bst.inorder_traversal()


# =========================================================
# GUI
# =========================================================
# This class creates the Tkinter interface and connects buttons to inventory
# operations.
#
# The GUI is intentionally basic for straightforward usabilily:
# - Simple form inputs
# - Action buttons
# - A table to display results
# - Status messages using popups
# =========================================================

class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Inventory Management System")
        self.root.geometry("1100x650")
        self.root.configure(bg="#d9f2d9")

        self.inventory = InventorySystem()

        # Load starter sample items so the app looks complete immediately.
        self.load_sample_data()

        # Build the GUI layout.
        self.create_title()
        self.create_form()
        self.create_buttons()
        self.create_search_sort_controls()
        self.create_table()

        # Initially show all items.
        self.refresh_table(self.inventory.get_all_items())

    def create_title(self):
        """Creates the title banner at the top of the window."""
        title = tk.Label(
            self.root,
            text="Minecraft Inventory Management System",
            font=("Arial", 20, "bold"),
            bg="#2e7d32",
            fg="white",
            pady=10
        )
        title.pack(fill="x")

    def create_form(self):
        """
        Creates the input form for item fields.
        These fields correspond directly to the Item class attributes.
        """
        form_frame = tk.Frame(self.root, bg="#d9f2d9", pady=10)
        form_frame.pack(fill="x", padx=15)

        tk.Label(form_frame, text="Item ID", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=8, pady=5)
        self.id_entry = tk.Entry(form_frame, width=18)
        self.id_entry.grid(row=0, column=1, padx=8, pady=5)

        tk.Label(form_frame, text="Name", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=8, pady=5)
        self.name_entry = tk.Entry(form_frame, width=20)
        self.name_entry.grid(row=0, column=3, padx=8, pady=5)

        tk.Label(form_frame, text="Category", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=0, column=4, padx=8, pady=5)
        self.category_entry = tk.Entry(form_frame, width=18)
        self.category_entry.grid(row=0, column=5, padx=8, pady=5)

        tk.Label(form_frame, text="Price (gold ingots)", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=8, pady=5)
        self.price_entry = tk.Entry(form_frame, width=18)
        self.price_entry.grid(row=1, column=1, padx=8, pady=5)

        tk.Label(form_frame, text="Quantity", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=1, column=2, padx=8, pady=5)
        self.quantity_entry = tk.Entry(form_frame, width=20)
        self.quantity_entry.grid(row=1, column=3, padx=8, pady=5)

    def create_buttons(self):
        """Creates the main CRUD action buttons."""
        button_frame = tk.Frame(self.root, bg="#d9f2d9", pady=10)
        button_frame.pack(fill="x", padx=15)

        tk.Button(button_frame, text="Add Item", width=15, bg="#4caf50", fg="white", command=self.add_item).grid(row=0, column=0, padx=8, pady=5)
        tk.Button(button_frame, text="Update Item", width=15, bg="#1976d2", fg="white", command=self.update_item).grid(row=0, column=1, padx=8, pady=5)
        tk.Button(button_frame, text="Remove Item", width=15, bg="#d32f2f", fg="white", command=self.remove_item).grid(row=0, column=2, padx=8, pady=5)
        tk.Button(button_frame, text="Clear Fields", width=15, bg="#757575", fg="white", command=self.clear_fields).grid(row=0, column=3, padx=8, pady=5)
        tk.Button(button_frame, text="Show All Items", width=15, bg="#6a1b9a", fg="white", command=lambda: self.refresh_table(self.inventory.get_all_items())).grid(row=0, column=4, padx=8, pady=5)

    def create_search_sort_controls(self):
        """Creates the search and sort controls below the main action buttons."""
        controls_frame = tk.Frame(self.root, bg="#d9f2d9", pady=10)
        controls_frame.pack(fill="x", padx=15)

        tk.Label(controls_frame, text="Search by ID", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=6, pady=5)
        self.search_id_entry = tk.Entry(controls_frame, width=15)
        self.search_id_entry.grid(row=0, column=1, padx=6, pady=5)
        tk.Button(controls_frame, text="Search ID", command=self.search_by_id, bg="#00897b", fg="white").grid(row=0, column=2, padx=6, pady=5)

        tk.Label(controls_frame, text="Search by Name", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=0, column=3, padx=6, pady=5)
        self.search_name_entry = tk.Entry(controls_frame, width=18)
        self.search_name_entry.grid(row=0, column=4, padx=6, pady=5)
        tk.Button(controls_frame, text="Search Name", command=self.search_by_name, bg="#00897b", fg="white").grid(row=0, column=5, padx=6, pady=5)

        tk.Label(controls_frame, text="Search by Category", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=0, column=6, padx=6, pady=5)
        self.search_category_entry = tk.Entry(controls_frame, width=18)
        self.search_category_entry.grid(row=0, column=7, padx=6, pady=5)
        tk.Button(controls_frame, text="Search Category", command=self.search_by_category, bg="#00897b", fg="white").grid(row=0, column=8, padx=6, pady=5)

        tk.Label(controls_frame, text="Sort Items", bg="#d9f2d9", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=6, pady=10)
        self.sort_choice = ttk.Combobox(controls_frame, values=["name", "price", "quantity"], state="readonly", width=15)
        self.sort_choice.grid(row=1, column=1, padx=6, pady=10)
        self.sort_choice.set("price")
        tk.Button(controls_frame, text="Sort", command=self.sort_items, bg="#f9a825", fg="black").grid(row=1, column=2, padx=6, pady=10)

    def create_table(self):
        """
        Creates the table used to display items.
        Treeview is a good fit because it displays rows and columns clearly.
        """
        table_frame = tk.Frame(self.root, bg="#d9f2d9")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("ID", "Name", "Category", "Price", "Quantity")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # When the user clicks a row, populate the form with that row's data.
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_sample_data(self):
        """
        Adds starter Minecraft-themed items.
        We chose these items to give variety across categories:
        - Weapons
        - Blocks
        - Food
        - Tools
        - Armor
        This makes the app look complete and helps demonstrate searching/sorting.
        """
        sample_items = [
            Item(101, "Diamond Sword", "Weapon", 45, 8),
            Item(102, "Oak Planks", "Block", 6, 128),
            Item(103, "Golden Apple", "Food", 30, 12),
            Item(104, "Iron Pickaxe", "Tool", 22, 15),
            Item(105, "Netherite Helmet", "Armor", 60, 4),
            Item(106, "Cooked Beef", "Food", 10, 40),
            Item(107, "Cobblestone", "Block", 4, 256),
            Item(108, "Bow", "Weapon", 18, 10),
            Item(109, "Torch", "Utility", 3, 80),
            Item(110, "Enchanted Book", "Magic", 50, 6)
        ]

        for item in sample_items:
            self.inventory.add_item(item)

    def get_form_data(self):
        """
        Reads and validates the item form.
        Returns converted values if valid.
        Raises ValueError if inputs are invalid.
        """
        item_id = int(self.id_entry.get().strip())

        if item_id < 0:
            raise ValueError("Item ID cannot be negative.")
        
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price_gold = int(self.price_entry.get().strip())
        quantity = int(self.quantity_entry.get().strip())

        if not name:
            raise ValueError("Name cannot be empty.")
        if not category:
            raise ValueError("Category cannot be empty.")
        if price_gold < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        return item_id, name, category, price_gold, quantity

    def add_item(self):
        """Handles the Add Item button."""
        try:
            item_id, name, category, price_gold, quantity = self.get_form_data()
            item = Item(item_id, name, category, price_gold, quantity)
            success, message = self.inventory.add_item(item)

            if success:
                self.refresh_table(self.inventory.get_all_items())
                self.clear_fields()
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def update_item(self):
        """Handles the Update Item button."""
        try:
            item_id, name, category, price_gold, quantity = self.get_form_data()
            success, message = self.inventory.update_item(item_id, name, category, price_gold, quantity)

            if success:
                self.refresh_table(self.inventory.get_all_items())
                self.clear_fields()
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def remove_item(self):
        """Handles the Remove Item button using the current ID field."""
        try:
            item_id_text = self.id_entry.get().strip()
            if not item_id_text:
                messagebox.showerror("Input Error", "Enter or select an Item ID to remove.")
                return

            item_id = int(item_id_text)
            success, message = self.inventory.remove_item(item_id)

            if success:
                self.refresh_table(self.inventory.get_all_items())
                self.clear_fields()
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Input Error", "Item ID must be a valid integer.")

    def search_by_id(self):
        """Searches for one item by ID and shows only that result if found."""
        try:
            item_id_text = self.search_id_entry.get().strip()
            if not item_id_text:
                messagebox.showerror("Input Error", "Enter an ID to search.")
                return

            item_id = int(item_id_text)
            item = self.inventory.search_by_id(item_id)

            if item:
                self.refresh_table([item])
            else:
                self.refresh_table([])
                messagebox.showinfo("Search Result", "No item found with that ID.")

        except ValueError:
            messagebox.showerror("Input Error", "Search ID must be an integer.")

    def search_by_name(self):
        """Searches inventory items by name text."""
        name = self.search_name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Enter a name to search.")
            return

        results = self.inventory.search_by_name(name)
        self.refresh_table(results)

        if not results:
            messagebox.showinfo("Search Result", "No items matched that name.")

    def search_by_category(self):
        """Searches inventory items by category text."""
        category = self.search_category_entry.get().strip()
        if not category:
            messagebox.showerror("Input Error", "Enter a category to search.")
            return

        results = self.inventory.search_by_category(category)
        self.refresh_table(results)

        if not results:
            messagebox.showinfo("Search Result", "No items matched that category.")

    def sort_items(self):
        """Builds a BST and displays items in sorted order."""
        sort_by = self.sort_choice.get()
        results = self.inventory.get_sorted_items(sort_by)
        self.refresh_table(results)

    def refresh_table(self, items):
        """
        Clears the table and inserts the provided list of items.
        This is used after add, remove, update, search, and sort operations.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in items:
            self.tree.insert("", "end", values=item.to_tuple())

    def clear_fields(self):
        """Clears the form fields."""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def on_row_select(self, event):
        """
        When a row in the table is selected, load its values into the form.
        This makes updates easier because the user can click an existing row,
        edit the fields, and then press Update.
        """
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        # Values come from the GUI table, so we strip the text " gold ingots"
        # from the price before putting it back into the entry field.
        item_id = values[0]
        name = values[1]
        category = values[2]
        price = str(values[3]).replace(" gold ingots", "")
        quantity = values[4]

        self.clear_fields()
        self.id_entry.insert(0, item_id)
        self.name_entry.insert(0, name)
        self.category_entry.insert(0, category)
        self.price_entry.insert(0, price)
        self.quantity_entry.insert(0, quantity)


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================
# This is where the program starts.
# Tkinter requires us to create a root window and run mainloop().
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()
