import seaborn as sns
from faicons import icon_svg
import folium
from shinywidgets import output_widget, render_widget

# Import data from shared.py
from shared import app_dir, df
from shiny import App, reactive, render, ui
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


app_dir = Path(__file__).parent

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Dashboard",
        ui.page_sidebar(
            ui.sidebar(
                ui.input_select(
                    "select",
                    "Select an option below:",
                    ["Choice 1", "Choice 2", "Choice 3"],
                ),
                ui.output_text("selected_value"),
                ui.input_checkbox_group(
                    "checkbox",
                    "Checkbox",
                    ["Checkbox1", "Checkbox2", "Checkbox3"],
                    selected=["Checkbox1", "Checkbox2", "Checkbox3"],
                ),
                title="Filter controls",
            ),
            # 🔹 PETA INDONESIA FULL-SCREEN
            ui.layout_columns(
                ui.card(
                    ui.card_header("Peta Indonesia"),
                    ui.output_ui("indonesia_map"),
                    style="flex-grow: 1; height: calc(100vh - 20px); width: 100%;",
                    full_screen=True,
                ),
                fill=True,
            ),
            ui.layout_column_wrap(
                ui.card(
                    ui.card_header("Plot Data"),
                    ui.output_plot("length_depth"),
                    style="height: 400px; width: 100%; overflow-y: auto;",
                    full_screen=True,
                ),
                width=1,
                fill=False,
            ),
            fillable=True,
        ),
    ),
    
    ui.nav_panel(
        "Tentang",
        ui.layout_columns(
            ui.card(
                ui.card_header("Informasi Aplikasi"),
                "Aplikasi ini menampilkan peta Indonesia dan visualisasi data",
                style="padding: 20px;",
            )
        ),
    ),
    title="Dashboard Indonesia Sehat",
    id="page",
)


def server(input, output, session):
    @output
    @render.text
    def selected_value():
        return f"Selected option: {input.select()}"

    @reactive.calc
    def filtered_df():
        return df  # Bisa ditambahkan filter sesuai kebutuhan

    @output
    @render.plot
    def length_depth():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=filtered_df(), x="bill_length_mm", y="bill_depth_mm", ax=ax
        )
        plt.tight_layout()
        return fig

    @output
    @render.ui
    def indonesia_map():
        m = folium.Map(location=[-2.5, 118], zoom_start=5, control_scale=True)

        map_html = f"""
        <div style="width: 100%; height: 100%; overflow: hidden;">
            {m._repr_html_()}
        </div>
        """
        return ui.HTML(map_html)


app = App(app_ui, server)
