from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.app import App

class TicTacToeGUI(BoxLayout):
    def __init__(self, game_controller, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.game_controller = game_controller
        self.board_size = 3  
        self.is_ai_mode = False  # Default to Local Multiplayer mode

        # 🎨 UI Elements
        self.info_label = Label(
            text="Player X's Turn",
            font_size=28,
            bold=True,
            size_hint=(1, 0.15)
        )

        # 🎛 Board Size Selector
        self.size_selector = Spinner(
            text="3x3",
            values=["3x3", "4x4", "5x5"],
            size_hint=(1, 0.1)
        )
        self.size_selector.bind(text=self.change_board_size)

        # 🔘 Game Mode Selector (AI or Multiplayer)
        self.mode_selector = ToggleButton(
            text="Multiplayer",
            size_hint=(1, 0.1),
            group="mode"
        )
        self.mode_selector.bind(on_press=self.toggle_game_mode)

        # 🎮 Game Grid
        self.grid = GridLayout(cols=self.board_size, spacing=5, padding=10)
        self.create_board()

        # 🔘 Reset Button
        self.reset_button = Button(text="Restart", size_hint=(1, 0.1))
        self.reset_button.bind(on_press=self.reset_board)

        # Add widgets
        self.add_widget(self.info_label)
        self.add_widget(self.size_selector)
        self.add_widget(self.mode_selector)
        self.add_widget(self.grid)
        self.add_widget(self.reset_button)

        # 🎵 Sounds
        self.move_sound = SoundLoader.load('move.wav')
        self.win_sound = SoundLoader.load('win.wav')

    def create_board(self):
        """Creates the Tic-Tac-Toe board dynamically."""
        self.grid.clear_widgets()
        self.grid.cols = self.board_size
        self.board_buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                btn = Button(font_size=36, background_normal='', background_color=(0, 0, 0, 1))
                btn.bind(on_press=self.make_move)
                self.grid.add_widget(btn)
                self.board_buttons[row][col] = btn

    def toggle_game_mode(self, instance):
        """Switches between AI mode and Multiplayer mode."""
        self.is_ai_mode = not self.is_ai_mode
        self.mode_selector.text = "AI Mode" if self.is_ai_mode else "Multiplayer"
        self.reset_board()

    def change_board_size(self, instance, text):
        """Changes the board size dynamically."""
        size = int(text[0])
        self.board_size = size
        self.game_controller.reset_game(size)
        self.create_board()
        self.info_label.text = "Player X's Turn"

    def make_move(self, instance):
        """Handles player moves and AI moves if enabled."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board_buttons[row][col] == instance and self.game_controller.make_move(row, col):
                    instance.text = self.game_controller.current_player
                    self.animate_button(instance)

                    if self.game_controller.check_winner():
                        self.show_winner_popup(f"Player {self.game_controller.current_player} Wins!")
                        return
                    elif self.game_controller.is_draw():
                        self.show_winner_popup("It's a Draw!")
                        return

                    self.game_controller.switch_player()
                    self.info_label.text = f"Player {self.game_controller.current_player}'s Turn"

                    if self.is_ai_mode and self.game_controller.current_player == "O":
                        self.ai_move()
                    return

    def ai_move(self):
        """Executes AI move using Minimax."""
        move = self.game_controller.get_best_move()
        if move:
            row, col = move
            self.make_move(self.board_buttons[row][col])

    def show_winner_popup(self, message):
        """Displays the winner popup."""
        if self.win_sound:
            self.win_sound.play()

        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text=message, font_size=24))
        close_button = Button(text="Restart", size_hint=(1, 0.3))
        close_button.bind(on_press=self.reset_board)
        popup_content.add_widget(close_button)
        popup = Popup(title="Game Over", content=popup_content, size_hint=(0.6, 0.4))
        popup.open()

    def reset_board(self, instance=None):
        """Resets the board."""
        self.game_controller.reset_game(self.board_size)
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.board_buttons[row][col].text = ''
        self.info_label.text = "Player X's Turn"

    def animate_button(self, button):
        """Creates an animation when a move is made."""
        anim = Animation(background_color=(1, 1, 1, 1), duration=0.2) + Animation(background_color=(0, 0, 0, 1), duration=0.2)
        anim.start(button)
        if self.move_sound:
            self.move_sound.play()
