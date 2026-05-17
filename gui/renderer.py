import tkinter as tk
from tkinter import LAST
from PIL import Image, ImageTk
import os

from core import constants


class BoardRenderer:

    def __init__(self, canvas):

        self.canvas = canvas
        self.piece_images = {}
        self.load_piece_images()

    def load_piece_images(self):
        """Load piece images from the pieces_images directory"""
        image_dir = os.path.join(os.path.dirname(__file__), "..", "pieces_images")
        piece_names = ["Warrior", "Mage", "Archer", "Tank", "Assassin"]

        for piece_name in piece_names:
            image_path = os.path.join(image_dir, f"{piece_name}.png")
            try:
                if os.path.exists(image_path):
                    # Load and resize image to fit in cell
                    image = Image.open(image_path)
                    # Resize to approximately 50% of cell size to prevent overlap
                    size = int(constants.CELL_SIZE * 0.5)
                    image = image.resize((size, size), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.piece_images[piece_name] = photo
                else:
                    print(f"Warning: Image not found for {piece_name} at {image_path}")
            except Exception as e:
                print(f"Error loading image for {piece_name}: {e}")

    def draw_board(self):

        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        board_pixel_size = (
            constants.BOARD_SIZE
            *
            constants.CELL_SIZE
        )

        offset_x = (
            canvas_width - board_pixel_size
        ) // 2

        offset_y = (
            canvas_height - board_pixel_size
        ) // 2

        # Draw cells
        for row in range(constants.BOARD_SIZE):

            for col in range(constants.BOARD_SIZE):

                x1 = (
                    offset_x
                    +
                    col * constants.CELL_SIZE
                )

                y1 = (
                    offset_y
                    +
                    row * constants.CELL_SIZE
                )

                x2 = x1 + constants.CELL_SIZE
                y2 = y1 + constants.CELL_SIZE

                bonus = constants.POSITION_BONUS[
                    row
                ][
                    col
                ]

                color = (
                    "#FFF8DC"
                    if bonus > 0
                    else "#DDDDDD"
                )

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="black"
                )

        # Draw Player and Enemy labels
        label_y_top = offset_y - 40
        label_y_bottom = offset_y + board_pixel_size + 40
        label_x = offset_x + board_pixel_size // 2

        self.canvas.create_text(
            label_x, label_y_top,
            text="Kẻ thù",
            fill="#FF0000",
            font=("Arial", 16, "bold")
        )
        self.canvas.create_text(
            label_x, label_y_bottom,
            text="Người chơi",
            fill="#00FF00",
            font=("Arial", 16, "bold")
        )

    def draw_message(self, message, size=24, color="black"):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        board_pixel_size = (
            constants.BOARD_SIZE
            *
            constants.CELL_SIZE
        )

        offset_x = (
            canvas_width - board_pixel_size
        ) // 2

        offset_y = (
            canvas_height - board_pixel_size
        ) // 2

        center_x = offset_x + board_pixel_size // 2
        center_y = offset_y + board_pixel_size // 2

        self.canvas.create_text(
            center_x,
            center_y,
            text=message,
            fill=color,
            font=("Arial", size, "bold")
        )

    def draw_team(
    self,
    battle_team,
    team_name,
    highlight_pos=None
    ):

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        board_pixel_size = (
            constants.BOARD_SIZE
            *
            constants.CELL_SIZE
        )

        offset_x = (
            canvas_width - board_pixel_size
        ) // 2

        offset_y = (
            canvas_height - board_pixel_size
        ) // 2

        for battle_unit in battle_team:

            if not battle_unit.alive:
                continue

            unit = battle_unit.unit

            piece = unit.piece
            pos = unit.position

            center_x = (
                offset_x
                +
                pos.col * constants.CELL_SIZE
                +
                constants.CELL_SIZE // 2
            )

            center_y = (
                offset_y
                +
                pos.row * constants.CELL_SIZE
                +
                constants.CELL_SIZE // 2
            )

            radius = (
                constants.CELL_SIZE // 3
            )
            if (
                highlight_pos
                and
                pos.row == highlight_pos[0]
                and
                pos.col == highlight_pos[1]
            ):

                outline_color = "yellow"

            else:
                # TEAM COLOR
                if team_name == "A":
                    
                    outline_color = (
                        constants.TEAM_A_COLOR
                    )

                else:

                    outline_color = (
                        constants.TEAM_B_COLOR
                    )

            fill_color = (
                constants.PIECE_COLORS[
                    piece.name
                ]
            )

            # PIECE IMAGE
            if piece.name in self.piece_images:
                self.canvas.create_image(
                    center_x,
                    center_y,
                    image=self.piece_images[piece.name]
                )
            else:
                # Fallback to colored circle if image not found
                self.canvas.create_oval(
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                    fill=fill_color,
                    outline=outline_color,
                    width=4
                )

                # TEXT
                self.canvas.create_text(
                    center_x,
                    center_y,
                    text=piece.name[0],
                    font=("Arial", 14, "bold"),
                    fill="white"
                )

            # PLAYER/ENEMY LABEL
            label_text = "Player" if team_name == "A" else "Enemy"
            label_color = "#00FF00" if team_name == "A" else "#FF0000"  # Green for Player, Red for Enemy
            self.canvas.create_text(
                center_x,
                center_y - radius - 2,  # Move down slightly (less negative)
                text=label_text,
                fill=label_color,
                font=("Arial", 9, "bold")
            )
            
            # HP BAR BG
            hp_bar_width = 70
            hp_bar_height = 10

            hp_x = center_x - hp_bar_width // 2
            hp_y = center_y + radius - 5  # Moved up a bit more

            self.canvas.create_rectangle(
                hp_x,
                hp_y,
                hp_x + hp_bar_width,
                hp_y + hp_bar_height,
                fill="red"
            )

            # HP BAR
            hp_ratio = (
                battle_unit.current_hp
                /
                piece.hp
            )

            self.canvas.create_rectangle(
                hp_x,
                hp_y,
                hp_x + hp_bar_width * hp_ratio,
                hp_y + hp_bar_height,
                fill="lime"
            )

            # HP TEXT WITH BACKGROUND FOR BETTER VISIBILITY
            hp_text = f"{battle_unit.current_hp}/{piece.hp}"
            # Text background (shadow effect)
            self.canvas.create_text(
                center_x + 1,
                hp_y + hp_bar_height + 8,  # Positioned below the HP bar
                text=hp_text,
                fill="black",
                font=("Arial", 10, "bold")
            )
    def draw_damage_popup(
        self,
        row,
        col,
        damage
    ):

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        board_pixel_size = (
            constants.BOARD_SIZE
            *
            constants.CELL_SIZE
        )

        offset_x = (
            canvas_width - board_pixel_size
        ) // 2

        offset_y = (
            canvas_height - board_pixel_size
        ) // 2

        center_x = (
            offset_x
            +
            col * constants.CELL_SIZE
            +
            constants.CELL_SIZE // 2
        )

        center_y = (
            offset_y
            +
            row * constants.CELL_SIZE
            +
            constants.CELL_SIZE // 2
        )

        if damage == 0:

            popup_text = "BLOCK"

            popup_color = "cyan"

        elif damage >= 5:

            popup_text = f"CRIT {damage}"

            popup_color = "orange"

        else:

            popup_text = f"-{damage}"

            popup_color = "red"

        self.canvas.create_text(
            center_x,
            center_y - 40,

            text=popup_text,

            fill=popup_color,

            font=("Arial", 16, "bold")
        )
    def draw_attack_line(
        self,
        attacker_row,
        attacker_col,
        defender_row,
        defender_col,
        attacker_team
    ):

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        board_pixel_size = (
            constants.BOARD_SIZE
            *
            constants.CELL_SIZE
        )

        offset_x = (
            canvas_width - board_pixel_size
        ) // 2

        offset_y = (
            canvas_height - board_pixel_size
        ) // 2

        x1 = (
            offset_x
            +
            attacker_col * constants.CELL_SIZE
            +
            constants.CELL_SIZE // 2
        )

        y1 = (
            offset_y
            +
            attacker_row * constants.CELL_SIZE
            +
            constants.CELL_SIZE // 2
        )

        x2 = (
            offset_x
            +
            defender_col * constants.CELL_SIZE
            +
            constants.CELL_SIZE // 2
        )

        y2 = (
            offset_y
            +
            defender_row * constants.CELL_SIZE
            +
            constants.CELL_SIZE // 2
        )
        line_color = (
            "#00FF00"
            if attacker_team == "A"
            else "#FF3333"
        )
        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=line_color,
            width=4,
            arrow=LAST,
            arrowshape=(10, 15, 5)
        )