import reflex as rx
import requests as rq


class StateApi(rx.State):
    listPers: list[dict] = []  # lista de diccionarios inicializada vacia

    @rx.background  # se pone esto y el async por q es asincronico
    async def getListApi(self):
        async with (
            self
        ):  # marcador de contexto tb por q es async es una especie de synclock
            response = rq.get("https://rickandmortyapi.com/api/character")
            self.listPers = response.json()["results"]

    @rx.var
    def getListCard(self) -> list[dict]:
        listCard: list[dict] = []
        for item in self.listPers:
            listCard.append(
                {
                    "name": item["name"],
                    "location": item["location"]["name"],
                    "image": item["image"],
                }
            )
        return listCard


@rx.page(route="/_api", title="Una simple solicitud api", on_load=StateApi.getListApi)
def api_web() -> rx.Component:
    return rx.container(
        rx.center(
            rx.vstack(
                rx.heading("Api", size="lg"),
                rx.text("Una simple solicitud api", size="sm", margin_top="-1em"),
                rx.button(
                    "Console Log StateApi.getListCard",
                    on_click=rx.console_log(StateApi.getListCard),
                ),
                rx.foreach(StateApi.getListCard, cardItem),
                align="center",
            ),
            padding_top="2em",
            padding_bottom="2em",
        ),
        rx.logo()
    )


def cardItem(item: dict) -> rx.card:
    return rx.card(
        rx.link(
            rx.flex(
                rx.image(src=item["image"], max_width="5em"),
                rx.box(
                    rx.heading(item["name"]),
                    rx.text(item["location"]),
                ),
                spacing="2",
            ),
        ),
        as_child=True,
    )
