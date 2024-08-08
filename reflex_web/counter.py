import reflex as rx


class StateCounter(rx.State):
    index: int = 0

    def aumentar(self):
        self.index += 1

    def disminuir(self):
        self.index -= 1

    @rx.var
    def getIndex(self):
        return self.index


@rx.page(route="/counter", title="Un simple contador")
def counter_web() -> rx.Component:
    return rx.container(
        rx.center(
            rx.vstack(
                rx.heading("Contador", size="lg"),
                rx.text("Un simple contador", size="sm", margin_top="-1em"),
                rx.hstack(
                    rx.button(
                        "-", on_click=StateCounter.disminuir, background_color="red"
                    ),
                    rx.text(StateCounter.getIndex, padding_top=".2em"),
                    rx.button(
                        "+", on_click=StateCounter.aumentar, background_color="green"
                    ),
                ),
                padding_top="2em",
                align="center",
                min_height="85vh",
            ),
        ),
        rx.logo(),
    )
