import logging
import types

from shiny import ui
from htmltools import div, p, a, tags
from typing import Optional,Union
from logs.logs import Logs

class Navbar(Logs):
    """
    Navbar object for FRED_GDP_UI
    """
    def __init__(
            self,
            nav_title:Optional[Union[str, ui. Tag, ui.TagList]] ="Go GDP",
            brand_class: str= "navbar-brand",
            links: Optional[list[dict]] = None

    ):
        """
        Initialize attributes for the navbar component
        """
        # Set default for navbar attributes.
        super().__init__(name="Navbar module",level= logging.INFO)
        self.info("Initializing navbar component.")


        nav_id:Optional[Union[str,None]] = None

        selected:Optional[Union[str,None]] =None

        sidebar:Optional[Union[ui.Sidebar,None]] =None

        fillable:Optional[Union[bool,list[str]]] =False

        fillable_mobile:bool = False

        gap:Optional[Union[ui.css.CssUnit,None]] = None

        padding:Optional[Union[ui.css.CssUnit,list[ui.css.CssUnit,None]]] =None

        header:Optional[Union[ui.TagChild,None]] =None

        footer:Optional[Union[ui.TagChild,None]] =None


        self._title = nav_title
        self._brand_class = brand_class
        self.links = links if links is not None else []
        self._id = nav_id
        self._selected = selected
        self._sidebar = sidebar
        self._fillable = fillable
        self._fillable_mobile = fillable_mobile
        self._gap = gap
        self._padding = padding
        self._header = header
        self._footer = footer

    @property
    def nav_title(self) ->Optional[Union[str,ui.Tag,ui.TagList]]:
        """
        Getter the title for the navbar
        :return: navbar title
        """
        return self._title
    @nav_title.setter
    def nav_title(self,value:str):
        """
        Setter for the navbar title
        :param value: Holds the value for title
        :type value: str
        :raise TypeError: If value is not of: Optional[Union[str,ui.Tag,ui.TagList]]
        """
        if value is not None and not isinstance(value,(str,ui.Tag,ui.TagList)):
            self.error(f"Incorrect type for value,types must be one of the following:(str,ui.Tag,ui.TagList).Type received:{type(value).__name__}.")
            raise TypeError("Please provide correct data type for navbar title")
        self._title = value
        self.info(f"Navbar title set to: {self._title}")


    def ui_generator(self):
        """
        Generate ui elements for the navbar
        """
        self.info("Rendering navbar elements.")
        return ui.nav_panel(
            "Home",
            ui.h3("Content"),
            div("This is the main panel body"),
        )








