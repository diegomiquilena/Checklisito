import json
import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, TwoLineListItem, MDList
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty


class Category:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)


class ChecklistApp(MDApp):
    dialog = None
    categories = []

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file('kv/main.kv')

    def on_start(self):
        self.load_data()
        for category in self.categories:
            self.add_category_to_ui(category)

        example_category = Category("Categoría Ejemplo")
        example_category.add_item("Item Ejemplo 1")
        example_category.add_item("Item Ejemplo 2")
        self.categories.append(example_category)
        
        # Mostrar las categorías e items en la interfaz
        for category in self.categories:
            self.add_category_to_ui(category)

        # Añadir ejemplos de categorías e items cuando la aplicación inicia
        items = ["Ejemplo de Item 1", "Ejemplo de Item 2", "Ejemplo de Item 3"]
        for item in items:
            self.root.ids.container.add_widget(
                OneLineListItem(text=item)
            )

    def on_stop(self):
        self.save_data()

    def add_category_to_ui(self, category):
        category_item = TwoLineListItem(
            text=category.name,
            secondary_text=f"{len(category.items)} items"
        )
        self.root.ids.container.add_widget(category_item)
        
        for item in category.items:
            self.root.ids.container.add_widget(
                OneLineListItem(text=item, secondary_text=category.name)
            )

    def add_category(self, name):
        new_category = Category(name)
        self.categories.append(new_category)
        self.add_category_to_ui(new_category)

    def show_add_category_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Nueva Categoría",
                type="custom",
                content_cls=DialogContent(),
                buttons=[
                    MDRaisedButton(
                        text="CANCELAR",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="AÑADIR",
                        on_release=self.add_category_from_dialog
                    ),
                ],
            )
        self.dialog.open()

    def add_category_from_dialog(self, *args):
        category_name = self.dialog.content_cls.ids.category_name.text
        if category_name:
            self.add_category(category_name)
        self.dialog.dismiss()

    def save_data(self):
        data = [{
            'name': category.name,
            'items': category.items
        } for category in self.categories]
        
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.categories = [Category(category['name']) for category in data]
                for category, category_data in zip(self.categories, data):
                    category.items = category_data['items']

    def add_item(self):
        # Funcionalidad para añadir un nuevo item
        new_item_text = f"Nuevo Item {len(self.root.ids.container.children) + 1}"
        self.root.ids.container.add_widget(
            OneLineListItem(text=new_item_text)
        )

class DialogContent(BoxLayout):
    category_name = ObjectProperty(None)

if __name__ == "__main__":
    ChecklistApp().run()
