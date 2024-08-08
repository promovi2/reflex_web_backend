"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.hstack(
                rx.text("Ejemplo1: "),
                rx.link("Contador", href="/counter"),
            ),
            rx.hstack(
                rx.text("Ejemplo2: "),
                rx.link("Api", href="/_api"),
            ),
            rx.hstack(
                rx.text("Ejemplo3: "),
                rx.link("LogIn", href="/login"),
            ),
            spacing="2",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


app = rx.App()
app.add_page(index)
