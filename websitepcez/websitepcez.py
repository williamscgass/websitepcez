"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from reflex import Component
from dataclasses import dataclass
from rxconfig import config
from math import floor
import random

class State(rx.State):
    """The app state."""

    ...

class TextfieldControlled(rx.State):
    text: str = ""
    
    @rx.event
    def on_key_up(self, event):
        if event == "Enter":
            return self.redirect_to_results()
    
    @rx.event  
    def redirect_to_results(self):
        return rx.redirect("/results")

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading(
                "Welcome to Websitepcez!", 
                size="9",
                align="center",
                ),
            rx.hstack(
                rx.input(
                    placeholder="Paste a link to your prebuilt:",
                    size="3",
                    width="92%",
                    value=TextfieldControlled.text,
                    on_change=TextfieldControlled.set_text,
                    on_key_up=TextfieldControlled.on_key_up,
                ),
                rx.button(
                    "Go!",
                    size="3",
                    width="8%",
                    on_click=TextfieldControlled.redirect_to_results,
                    ),
                width="80%",
            ),
            spacing="5",
            align="center",
            justify="center",
            min_height="85vh",
        )
    )
    
results_heading_style: rx.style = {
     "padding-top": "50px",
 } 

card_header_style: rx.style = {
    "margin-bottom": "10px",
}

@dataclass
class ComputerPart:
    name: str
    
computer_part_names = ["Intel i7 12700KF", "Nvidia RTX 3080, 10GB", "32 GB DDR6", "1 TB SSD", "750W PSU"]
computer_parts = [ComputerPart(name=name) for name in computer_part_names] 
    
random_pc_names = ["HP Omen 35L", "Alienware Aurora R12", "MSI Cockslayer 9000"]
random_pc_prices = ["$1200", "$1500", "$2000"] 
random_pc_wizard_scores = ["93", "89", "85"] 
    
data = [
    {"date": "12/12/24", "Your Build": 1200, "Best Other Build": 1000, "Average Other Build": 1100},
    {"date": "12/13/24", "Your Build": 1200, "Best Other Build": 900, "Average Other Build": 1200},
    {"date": "12/14/24", "Your Build": 1200, "Best Other Build": 1000, "Average Other Build": 1150},
    {"date": "12/15/24", "Your Build": 1200, "Best Other Build": 1100, "Average Other Build": 1231},
    {"date": "12/16/24", "Your Build": 1200, "Best Other Build": 800, "Average Other Build": 1000},
]

def line_features():
    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key="Your Build",
            type_="monotone",
            stroke="white",
        ),
        rx.recharts.line(
            data_key="Best Other Build",
            type_="monotone",
            stroke="green",
        ),
        rx.recharts.line(
            data_key="Average Other Build",
            type_="monotone",
            stroke="#8884d8",
        ),
        rx.recharts.x_axis(data_key="date"),
        rx.recharts.y_axis(),
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(),
        data=data,
        width="100%",
        height=300,
    )
    
def results() -> rx.Component:
    # Results Page
    return rx.container(
        rx.vstack(
            rx.heading(f"Check out what we found!", size="8"),
            rx.text(
                "Displaying results for: ",
                TextfieldControlled.text,
                size="3",
                color_scheme="gray",
                margin="0"
            ),
            rx.flex(
                rx.vstack(
                    rx.card(
                        rx.heading(
                            "Wizard Score: ", 
                            rx.el.span(
                                "93",
                                style={"color": "green"},
                            ),
                            size="6",
                        ),
                        width="100%",
                    ),
                    rx.card(
                        rx.heading(
                            "Computer Parts", 
                            size="6",
                            style=card_header_style,
                        ),
                        rx.vstack(
                            rx.foreach(
                                computer_parts,
                                lambda part: rx.card(
                                    rx.hstack(
                                        rx.image(
                                                src="/gpu.png",
                                                height="24px",
                                                width="24px",
                                                border_radius="100%",
                                        ),
                                        rx.heading(
                                            part.name, 
                                            size="4",
                                            nowrap=True,
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                rx.vstack(
                    rx.card(
                        rx.heading(
                            "Price History", 
                            size="6",
                            style=card_header_style,
                        ),
                        line_features(),
                        width="100%",
                    ),
                    rx.card(
                        rx.heading(
                            "Better Alternatives",
                            size="6",
                            style=card_header_style,
                        ),
                        rx.vstack(
                            rx.foreach(
                                random_pc_names,
                                lambda name: rx.card(
                                    rx.heading(
                                        rx.link(
                                            name, 
                                            href="/results",
                                        ),
                                        " $",
                                        floor(random.random() * 1000),
                                        ": Wizard Score ",
                                        rx.el.span(
                                            floor(random.random() * 100),
                                            style={"color": "green"},
                                        ),
                                        size="4"
                                        ),
                                ),
                            ),
                        ),
                        width="100%",
                    ),
                    flex="1"
                ),
                width="100%",
                gap=20,
                align="stretch",
            ),
        ),
        style=results_heading_style,
        spacing="1",
        justify="center",
    )

app = rx.App()
app.add_page(index)
app.add_page(results)
