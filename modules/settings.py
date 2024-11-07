import pygame
import configparser
import json
from abc import ABC, abstractmethod
import os
import shutil
import ast

class Settings(ABC):
    """ Create a Settings singleton instance if not existing and return instance """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            super().__init__()
            self.config = configparser.ConfigParser()
            self.user_settings_filepath = "config/user_settings.ini"
            self.default_user_settings_filepath = "config\dev\default_user_settings.ini"
            self.dev_settings_filepath = "config/dev/dev_settings.json"
            self.load_settings()

    @abstractmethod   
    def load_settings(self):
        pass

    @abstractmethod
    def save_settings(self):
        pass

class UserSettings(Settings):
    def load_settings(self):
        if os.path.exists(self.user_settings_filepath):
            self.config.read(self.user_settings_filepath)
            for section in self.config.sections():
                for key, value in self.config.items(section):
                    # Check settings ini key value data type for conversion from string to number, bool, etc.
                    setattr(self, key, ast.literal_eval(value))

        else:
            print(f"{self.user_settings_filepath} does not exist. Creating...")
            try:
                shutil.copy(self.default_user_settings_filepath, self.user_settings_filepath)
                self.config.read(self.user_settings_filepath)
                print(f"{self.user_settings_filepath} created. Default user settings restored.")
                
            except Exception as e:
                print(f"Could not create file {self.user_settings_filepath}\nAn exception ocurred: {e}")
                pygame.QUIT
        

    def save_settings(self):
        """ Save class attribute settings to user_settings.ini file """
        # Get settings class variable attributes by removing inherited
        attrs = set(self.__dict__.keys())
        inherited_attrs = set(dir(Settings))
        settings_attrs = attrs - inherited_attrs - {'config', 'initialized'}

        # Set each config key value, with matching class attr, to class attr value
        for attr in settings_attrs:
            value = getattr(self, attr)
            for section in self.config.sections():
                for key, _ in self.config.items(section):
                    if str(attr) == str(key):
                        self.config.set(section, attr, value)
        
        # Write the updated configuration back to the .ini file
        try:
            with open(self.user_settings_filepath, 'w') as configfile:
                self.config.write(configfile)
            print(f"Settings saved to {self.user_settings_filepath}")
        except Exception as e:
            print(f"Could not save settings to {self.user_settings_filepath}\nAn exception occurred: {e}")        

class DevSettings(Settings):
    def load_settings(self):
        if os.path.exists(self.dev_settings_filepath):
            with open(self.dev_settings_filepath, "r") as file:
                settings_json = json.load(file)
                for key, value in settings_json.items():
                    setattr(self, key, value)
        else:
            print(f"{self.dev_settings_filepath} not found.")

    def save_settings(self):
        """ Save class attribute settings to dev_settings.json file """
        # Get settings class variable attributes by removing inherited
        attrs = set(self.__dict__.keys())
        inherited_attrs = set(dir(Settings))
        settings_attrs = attrs - inherited_attrs - {'config', 'initialized'}

        # Create a dictionary to store current attribute values
        settings_json = {}
        for attr in settings_attrs:
            value = getattr(self, attr)
            settings_json[attr] = value

        # Write updated settings to the JSON file
        try:
            with open(self.dev_settings_filepath, "w") as file:
                json.dump(settings_json, file, indent=4)
            print(f"Settings saved to {self.dev_settings_filepath}")
        except Exception as e:
            print(f"Could not save settings to {self.dev_settings_filepath}\nAn exception occurred: {e}")
        
