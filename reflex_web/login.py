import reflex as rx
import requests as rq
import re  # se requiere para usar expresiones regulares (comprobar el mail correcto)
import asyncio


class loginState(rx.State):
    loader: bool = False
    username: str = "example@mail.com"
    password: str = ""
    error = False
    response: dict = {}

    @rx.background
    async def loginService(self, data: dict):
        async with self:
            self.loader = True
            self.error = True
            self.loader = False
            self.error = True
            return
            response = rq.post(
                "http://0.0.0.0:8000/auth/login",
                json=data,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                self.response = response.json
                self.loader = False
                return rx.redirect("/")  # redirije al home
            else:
                self.error = True
                self.loader = False

    @rx.var
    def user_invalid(self) -> bool:
        return not (
            re.match(r"[^@]+@[^@]+.[^@]+", self.username) and "example@mail.com"
        )

    @rx.var
    def user_empty(self) -> bool:
        return not (self.username.strip())

    @rx.var
    def password_empty(self) -> bool:
        return not (self.password.strip())

    @rx.var
    def validate_fields(self) -> bool:
        return self.user_empty or self.user_invalid or self.password_empty


@rx.page(route="/login", title="Un simple LogIn")
def login_web() -> rx.Component:
    return rx.container(
        rx.flex(
            rx.image(src="/pm2_logo.png", max_width="200px"),
            rx.heading("LogIn", padding_top="2em"),
            rx.text("Inicio de sesíon"),
            rx.form.root(
                rx.flex(
                    field_form_component_general(
                        "Usuario",
                        "Ingrese su correo",
                        "Ingrese un correo válido",
                        "username",
                        loginState.set_username,  # no se declara, se genera solo y establece el valor por el nombre "set_" + variable
                        loginState.user_invalid,
                    ),
                    field_form_component(
                        "Contraseña",
                        "Ingrese su contraseña",
                        "password",
                        loginState.set_password,  # no se declara, se genera solo y establece el valor por el nombre "set_" + variable
                        "password",
                    ),
                    rx.form.submit(
                        rx.cond(  # esto es una especie de if
                            loginState.loader,  # condicion
                            rx.chakra.spinner(color="black", size="sm"),  # true
                            rx.button(  # false
                                "Iniciar sesión",
                                disabled=loginState.validate_fields,
                                width="30vw",
                            ),
                        ),
                        as_child=True,
                    ),
                    width="100%",
                    direction="column",
                    align="center",
                    justify="center",
                    spacing="2",
                ),
                rx.cond(
                    loginState.error,
                    rx.callout(
                        "Credenciales incorrectas",
                        icon="alert_triangle",
                        color_scheme="gray",
                        role="alert",
                        style={"margin_top": "10px"},
                    ),
                ),
                on_submit=loginState.loginService,
                reset_on_submit=True,
                width="80%",
            ),
            width="100%",
            direction="column",
            align="center",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
        style=style_section,
        justify="center",
        width="100%",
    )


def field_form_component(
    label: str, placeholder: str, name_var: str, on_change_function, type_field: str
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input.input(
                    placeholder=placeholder,
                    on_change=on_change_function,
                    name=name_var,
                    type=type_field,
                    required=True,
                ),
                as_child=True,
            ),
            rx.form.message(
                "El campo no puede ser nulo",
                match="valueMissing",
                color="red",
            ),
            direction="column",
            spacing="1",
            align="stretch",
        ),
        name=name_var,
        width="30vw",
    )


def field_form_component_general(
    label: str,
    placeholder: str,
    message_validate: str,
    name: str,
    on_change_function,
    show,
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input.input(
                    placeholder=placeholder,
                    on_change=on_change_function,
                    name=name,
                    required=True,
                ),
                as_child=True,
            ),
            rx.form.message(
                message_validate,
                name=name,
                force_match=show,
                match="valueMissing",
                color="red",
            ),
            direction="column",
            spacing="1",
            align="stretch",
        ),
        name=name,
        width="30vw",
    )


style_section = {
    "height": "90vh",
    "width": "80%",
    "margin": "auto",
}
