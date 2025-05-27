from collections import OrderedDict
import discord

class InitiativeTracker:
    """
    Tracks initiative order for a set of named entries, such as in a tabletop RPG.
    Supports adding, removing, swapping, and printing entries.
    """

    def __init__(self):
        """
        Initializes the InitiativeTracker with an empty entries dictionary.
        """
        self._entries = {}
    
    def clear(self):
        """
        Clears all entries in the initiative tracker.
        Returns a success message.
        """
        self._entries.clear()
        return "Initiative tracker cleared."

    def add(self, name, value):
        """
        Adds or updates an entry with the given name and initiative value.
        Returns a success or error message.
        """
        try:
            self._entries[name] = value
            self._sort_entries()
            return f"Added {name} with initiative {value}."
        except Exception as e:
            return f"Failed to add {name}: {e}"

    def remove(self, name):
        """
        Removes the entry with the given name.
        Returns a success or error message.
        """
        try:
            if name in self._entries:
                del self._entries[name]
                self._sort_entries()
                return f"Removed {name}."
            else:
                return f"Error: {name} not found."
        except Exception as e:
            return f"Failed to remove {name}: {e}"

    def swap(self, name1, name2):
        """
        Swaps the initiative values of two entries by name.
        Returns a success or error message.
        """
        try:
            if name1 in self._entries and name2 in self._entries:
                # Python double-swap!
                self._entries[name1], self._entries[name2] = self._entries[name2], self._entries[name1]
                self._sort_entries()
                return f"Swapped {name1} and {name2}."
            else:
                missing = [n for n in (name1, name2) if n not in self._entries]
                return f"Error: {', '.join(missing)} not found."
        except Exception as e:
            return f"Failed to swap {name1} and {name2}: {e}"
    
    async def new_initiative(self, message):
        """
        Creates a new initiative tracker based on the number of participants specified in the message.
        Expects the message content to be in the format "!init <number>" where <number> is the number of participants.
        Ignores entries that start with '!' and stops after the specified number of entries are saved.
        """
        number = int(message.content.split(' ', 1)[1])

        count = 0
        async for msg in message.channel.history(limit=50, oldest_first=False):
            content = msg.content.strip()
            if content.startswith('!'):
                continue
            if content.isdigit():
                self.add(str(msg.author.display_name), int(content))
                count += 1
            elif ':' in content:
                parts = content.split(':', 1)
                name = parts[0].strip()
                num_part = parts[1].strip()
                if num_part.isdigit():
                    self.add(name, int(num_part))
                    count += 1
            if count == number:
                break
                    
        return f"Initiative tracker created with {len(self._entries)} participants."

    def _sort_entries(self):
        """
        Sorts the entries dictionary in descending order by initiative value.
        """
        self._entries = dict(sorted(self._entries.items(), key=lambda item: item[1], reverse=True))

    def __str__(self):
        """
        Returns the current entries in initiative order as a formatted string.
        """
        printed_entries = "\n".join(f"{name}: {value}" for name, value in self._entries.items())
        return f"```\n{printed_entries}\n```"