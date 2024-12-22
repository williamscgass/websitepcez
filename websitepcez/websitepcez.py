"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...

class TextfieldControlled(rx.State):
    text: str = "Hello World!"
    
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
     "margin-top": "50px",
 }   
    
def results() -> rx.Component:
    # Results Page
    return rx.container(
        rx.vstack(
            rx.heading(f"Check out what we found!", size="7"),
            rx.text(
                "Displaying results for: ",
                TextfieldControlled.text,
                size="3",
                color_scheme="gray",
                margin="0"
            ),
            style=results_heading_style,
        ),
        spacing="5",
        justify="center",
        min_height="85vh",
    )

app = rx.App()
app.add_page(index)
app.add_page(results)
