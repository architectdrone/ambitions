import database as db
from tabulate import tabulate

databaseWrapper = db.databaseWrapper()
database = databaseWrapper.database

print("AMBITION V0.1")

class ambitionCLI():
    record_tables = ['ambitions', 'finite_projects', 'infinite_projects', 'negatives', 'positives', 'tasks', 'virtues']
    
    def menu(self):
        while True:
            command = input("Command > ").split()
            if command[0] == 'new':
                self.newEntry(command[1]+'s')
            elif command[0] == 'view':
                self._printAll(command[1])
            elif command[0] == 'relate':
                if command[1] == 'ambitions':
                    self.newEntry('ambition_ambition')
                elif command[:1] == ["finite_project","to","virtue"]:
                    self.newEntry('virtue_finite_project')
                elif command[:1] == ["infinite_project","to","virtue"]:
                    self.newEntry('virtue_infinite_project')
                else:
                    print("Relationship invalid.")
            elif command[0] == 'quit':
                break
            else:
                print("Huh?")
    
    def newEntry(self, table):
        '''
        Runs a command line prompt for creating a new entry.
        @param table The table to enter in to.
        '''
        to_enter = []
        for i in databaseWrapper.getColumnNames(table):
            if i+'s' in self.record_tables:
                self._printAll(i+'s')
                id = int(input(i.capitalize() + " ID > "))
                to_enter.append(id)
            elif i == 'parent' or i == 'child':
                if table == 'ambition_ambition':
                    self._printAll('ambitions')
                else:
                    self._printAll(table)
                id = int(input(i.capitalize() + " ID > "))
                to_enter.append(id)
            elif i == 'id':
                continue
            else:
                entry = input(i.capitalize() + " > ")
                to_enter.append(entry)
        
        comma_separated_keys = ",".join([i for i in databaseWrapper.getColumnNames(table) if i != 'id'])
        comma_separated_values = ",".join([(str(i) if type(i) != str else f'"{i}"') for i in to_enter])
        query = f'INSERT INTO {table} ({comma_separated_keys}) VALUES ({comma_separated_values})'
        database.run(query)
        print("Done\n")

    def _printAll(self, table):
        '''
        Prints all items in a table.
        '''
        to_show = databaseWrapper.search(table)
        print(list(to_show[0].keys()))
        print(tabulate(to_show, headers = {v: k for k, v in to_show[0].items()}))

cli = ambitionCLI()
cli.menu()