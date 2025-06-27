class InitiativeTracker:
    """
    Tracks initiative order for a set of named entries, such as in a tabletop RPG.
    Supports adding, removing, swapping, and printing entries.
    """

    def __init__(self):
        """
        Initializes the InitiativeTracker with an empty entries dictionary.
        """
        self._entries = []
    
    def clear(self):
        """
        Clears all entries in the initiative tracker.
        Returns a success message.
        """
        self._entries = []
        return "Initiative tracker cleared."

    def add(self, name, value):
        """
        Adds or updates an entry with the given name and initiative value.
        Returns a success or error message.
        """
        inserted = False
        if self._entries == []:
            self._entries = [[name, value]]
            inserted = True
        else:
            for entry in self._entries:
                if value > entry[1]:
                    # Insert before the last entry with a lower value
                    self._entries.insert(self._entries.index(entry), [name, value])
                    inserted = True
                    break
            if not inserted:
                # If no higher value found, append to the end
                self._entries.append([name, value])
                inserted = True
        
        if not inserted:
            return f"Error: {name} already exists with a value of {value}."
        else:
            return f"Added {name} with initiative {value}."


    def remove(self, name):
        """
        Removes the entry with the given name.
        Returns a success or error message.
        """
        try:
            for entry in self._entries:
                if entry[0] == name:
                    self._entries.remove(entry)
                    return f"Removed {name}."
            return f"Error: {name} not found."
        except Exception as e:
            return f"Failed to remove {name}: {e}"

    def swap(self, name1, name2):
        """
        Swaps the initiative values of two entries by name.
        Returns a success or error message.
        """
        names = [n[0] for n in self._entries]
        try:
            if name1 in names and name2 in names:
                idx1 = names.index(name1)
                idx2 = names.index(name2)
                # Python double-swap!
                self._entries[idx1][0], self._entries[idx2][0] = self._entries[idx2][0], self._entries[idx1][0]
                return f"Swapped {name1} and {name2}."
            else:
                missing = [n for n in (name1, name2) if n not in names]
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
        
        self._sort_entries()
        return f"Initiative tracker created with {len(self._entries)} participants."

    def _sort_entries(self):
        """
        Sorts the entries list in descending order by initiative value.
        """
        self._entries.sort(key=lambda x: x[1], reverse=True)

    def __str__(self):
        """
        Returns the current entries in initiative order as a formatted string.
        """
        printed_entries = "\n".join(f"{name:>30} | {value:>3}" for name, value in self._entries)
        return f"```\n{printed_entries}\n```"
    
    
if __name__ == "__main__":
    tracker = InitiativeTracker()
    print(tracker.add("Alice", 15))
    print(tracker.add("Bob", 20))
    print(tracker.add("Charlie", 10))
    print(tracker)
    
    print(tracker.remove("Alice"))
    print(tracker)
    
    print(tracker.swap("Bob", "Charlie"))
    print(tracker)
    
    print(tracker.add("Diana", 18))
    print(tracker.add("Eve", 20))      # Value collision with Bob
    print(tracker.add("Frank", 10))    # Value collision with Charlie
    print(tracker.add("Grace", 15))    # Value collision with Alice (already removed)
    print(tracker.add("Heidi", 12))
    print(tracker.add("Ivan", 18))     # Value collision with Diana

    print(tracker.swap("Bob", "Diana"))  # Swapping Bob and Diana

    print(tracker)