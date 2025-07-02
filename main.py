from textual.app import App, ComposeResult
from textual.containers import Vertical, Center
from textual.widgets import Static
from textual.events import Key
from keyboard import get_key
import sqlite3
import os

class TitleScreen(App):
    CSS = """
    Screen {
        align: center middle;
    }
    
    .title {
        text-align: center;
        margin: 1 0;
        color: cyan;
        text-style: bold;
    }
    
    .menu-item {
        text-align: center;
        margin: 1 0;
        padding: 0 2;
    }
    
    .selected {
        background: white;
        color: black;
    }
    
    .disabled {
        color: gray;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.has_save_file = self.check_save_file()
        
    def check_save_file(self) -> bool:
        """Check if save file exists"""
        return os.path.exists("savegame.db")
    
    def compose(self) -> ComposeResult:
        with Center():
            with Vertical():
                yield Static("GAME TITLE", classes="title")
                yield Static("", id="spacer")
                yield Static("New Game", id="menu-0", classes="menu-item selected")
                
                if self.has_save_file:
                    yield Static("Load Game", id="menu-1", classes="menu-item")
                else:
                    yield Static("No Saved Games", id="menu-1", classes="menu-item disabled")
                    
                yield Static("Quit", id="menu-2", classes="menu-item")
    
    def update_selection(self):
        """Update the visual selection"""
        for i in range(3):
            menu_item = self.query_one(f"#menu-{i}")
            if i == self.selected_index:
                menu_item.add_class("selected")
            else:
                menu_item.remove_class("selected")
    
    def on_key(self, event: Key) -> None:
        """Handle key press events"""
        key_pressed = event.key
        
        if key_pressed in ['w', 'up']:
            self.selected_index = (self.selected_index - 1) % 3
            self.update_selection()
            
        elif key_pressed in ['s', 'down']:
            self.selected_index = (self.selected_index + 1) % 3
            self.update_selection()
            
        elif key_pressed == 'enter':
            self.handle_selection()
            
        elif key_pressed in ['q', 'escape']:
            self.exit()
    
    def handle_selection(self):
        """Handle menu selection"""
        if self.selected_index == 0:  # New Game
            self.start_new_game()
        elif self.selected_index == 1:  # Load Game
            if self.has_save_file:
                self.load_game()
            # Do nothing if no save file
        elif self.selected_index == 2:  # Quit
            self.exit()
    
    def start_new_game(self):
        """Start a new game"""
        # Here I need to transition to game screen
        # For now, just show a message and exit
        self.exit(message="Starting new game...")
    
    def load_game(self):
        """Load existing game"""
        # Will load from SQLite and transition to game screen
        # For now, just show a message and exit
        self.exit(message="Loading game...")

def main():
    app = TitleScreen()
    result = app.run()

    if hasattr(result, 'message'):
        print(result.message)

if __name__ == "__main__":
    main()