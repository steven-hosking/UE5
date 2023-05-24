import unreal
import getpass
import subprocess
import os


class ShotgunAuthScript:
    @staticmethod
    def validate_shotgrid_auth():
        """
        Validates the Shotgun authentication for the current user.
        Returns:
            bool: True if the authentication is valid, False otherwise.
        Raises:
            FileNotFoundError: If the authentication file is not found.
        """
        username = getpass.getuser()
        file_path = rf'C:\Users\{username}\AppData\Roaming\Shotgun\authentication.yml' #This is searching for a auth file created by sgtk
        search_data = 'session_token'
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r') as file:
            file_contents = file.read()
            if search_data in file_contents:
                return True
        return False

    @staticmethod
    def open_shell(commands):
        subprocess.Popen(["start", "cmd", "/K", commands], shell=True)

    @staticmethod
    def shotgrid_auth_main():
        """
        Main function for ShotGrid authentication.

        Prompts the user to validate their ShotGrid log in and performs authentication if selected.
        Handles different pipeline types and displays appropriate messages.

        Args:
            job_dir (str): Directory path for the job (optional).
        """
        check_shotgrid_auth = unreal.EditorDialog.show_message(
            "Log in to Shotgun",
            """Would you like to validate your log in to shotgun?""",
            unreal.AppMsgType.YES_NO
        )

        if check_shotgrid_auth == unreal.AppReturnType.YES:
            print("Checking Shotgun authentication!")

            auth_valid = ShotgunAuthScript.validate_shotgrid_auth()

            if not auth_valid:
                unreal.EditorDialog.show_message(
                    "Shotgun auth failed",
                    """Please log in to Shotgun using the terminal window.\n\nThis may take up to 10 seconds to populate the window""",
                    unreal.AppMsgType.OK,
                    unreal.AppReturnType.OK
                )
                commands_to_run = "run custom item"
                ShotgunAuthScript.open_shell(commands_to_run)
            else:
                unreal.EditorDialog.show_message(
                    "Success",
                    """You are logged in and validated to Shotgun""",
                    unreal.AppMsgType.OK
                )
        else:
            print("No Selection made")

    @staticmethod
    def main():
        """
        Main function for creating menus and adding a Shotgun authentication entry into Unreal Engine.
        """
        print("Creating Menus!")
        menus = unreal.ToolMenus.get()

        main_menu = menus.find_menu("LevelEditor.MainMenu")
        if not main_menu:
            print("Failed to find the 'Main' menu.")

        entry = unreal.ToolMenuEntry(
            name="Python.Tools",
            type=unreal.MultiBlockType.MENU_ENTRY,
            insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST)
        )
        entry.set_label("Shotgun Auth")
        entry.set_tool_tip('Checks if you are authorized in Shotgun')
        entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', string="ShotgunAuthScript.shotgrid_auth_main()")

        script_menu = main_menu.add_sub_menu(main_menu.get_name(), "", "CustomTools", "CustomTools") # CustomTools is a placeholder name
        script_menu.add_menu_entry("Scripts", entry)

        menus.refresh_all_widgets()


# Call the main method of the ShotgunAuthScript class
ShotgunAuthScript.main()
