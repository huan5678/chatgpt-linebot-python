import time
import flet as ft


def main(page: ft.Page):
    page.title = "Flet APP"

    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # def minus_click(e):
    #     txt_number.value = str(int(txt_number.value) - 1)
    #     page.update()

    # def plus_click(e):
    #     txt_number.value = str(int(txt_number.value) + 1)
    #     page.update()

    # page.add(
    #     ft.Row(
    #         [
    #             ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
    #             txt_number,
    #             ft.IconButton(ft.icons.ADD, on_click=plus_click),
    #         ],
    #         alignment=ft.MainAxisAlignment.CENTER,
    #     )
    # )

    t = ft.Text(value = "Hello World!", color="#99cc99")
    page.controls.append(t)
    page.update()

    t = ft.Text()
    page.add(t)  # it's a shortcut for page.controls.append(t) and then page.update()

    for i in range(4):
        t.value = f"Step {i}"
        page.update()
        time.sleep(0.5)

    page.add(
        ft.Row(controls=[
            ft.Text("A"),
            ft.Text("B"),
            ft.Text("C")
        ])
    )

    page.add(
        ft.Row(controls=[
            ft.TextField(label="Your name"),
            ft.ElevatedButton(text="Say my name!")
        ])
    )

    for i in range(10):
      page.controls.append(ft.Text(f"Line {i}"))
      if i > 4:
          page.controls.pop(0)
      page.update()
      time.sleep(0.3)

    def button_clicked(e):
        page.add(ft.Text("Clicked!"))

    page.add(ft.ElevatedButton(text="Click me", on_click=button_clicked))

    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        page.update()

    new_task = ft.TextField(hint_text="Whats needs to be done?", width=300)
    page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))
    
    first_name = ft.TextField()
    last_name = ft.TextField()
    first_name.disabled = True
    last_name.disabled = True
    page.add(first_name, last_name)
    
    c = ft.Column(controls=[
        first_name,
        last_name
    ])
    
    c.disabled = True
    page.add(c)
    
    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()

    def btn_click(e):
        greetings.current.controls.append(
            ft.Text(f"Hello, {first_name.current.value} {last_name.current.value}!", color="#778899")
        )
        first_name.current.value = ""
        last_name.current.value = ""
        page.update()
        first_name.current.focus()

    page.add(
        ft.TextField(ref=first_name, label="First name", autofocus=True),
        ft.TextField(ref=last_name, label="Last name"),
        ft.ElevatedButton("Say hello!", on_click=btn_click),
        ft.Column(ref=greetings),
    )

    def checkbox_changed(e):
        output_text.value = (
            f"You have learned how to ski :  {todo_check.value}."
        )
        page.update()

    output_text = ft.Text()
    todo_check = ft.Checkbox(label="ToDo: Learn how to use ski", value=False, on_change=checkbox_changed)
    page.add(todo_check, output_text)

    page.scroll = "always"
    page.update()

    # lv = ft.ListView(expand=True, spacing=10)
    # for i in range(5000):
    #     lv.controls.append(ft.Text(f"Line {i}"))
    # page.add(lv)
    # page.update()

    def drag_accept(e):
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
        # update text inside draggable control
        src.content.content.value = "0"
        # update text inside drag target control
        e.control.content.content.value = "1"
        page.update()

    r = ft.Row(wrap=True, scroll="always", expand=True)
    page.add(r)

    for i in range(20):
        r.controls.append(
            ft.Draggable(
                group="number",
                content=ft.Container(
                    width=50,
                    height=50,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.AMBER_100,
                    border=ft.border.all(1, ft.colors.AMBER_400),
                    content=ft.Text(f"{i}", size=20),
                    border_radius=5,
                ),
                content_when_dragging=ft.Container(
                    width=50,
                    height=50,
                    bgcolor=ft.colors.BLUE_GREY_200,
                    border_radius=5,
                ),
                content_feedback=ft.Text(f"{i}"),
            )
        )
    page.update()

    # gv = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
    # page.add(gv)

    # for i in range(36):
    #     gv.controls.append(
    #         ft.Container(
    #             ft.Text(f"Item {i}"),
    #             width=100,
    #             height=100,
    #             alignment=ft.alignment.center,
    #             bgcolor=ft.colors.AMBER_100,
    #             border=ft.border.all(1, ft.colors.AMBER_400),
    #             border_radius=ft.border_radius.all(5),
    #         )
    #     )
    # page.update()




ft.app(target=main)
