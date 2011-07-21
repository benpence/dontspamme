import os
import sys

SOURCE_PATH = os.path.join(os.getcwd(),'src')

ENV_VARS_PATH = 'CONFIG'
ENV_VARS_PADDING = "<<%s>>"

UNINSTALL_DIRECTORY = os.path.join(os.getcwd(), '.uninstall')
UNINSTALL_SEPARATOR = '@'

class edit_and_save(object):
    """
    Makes database connections easier
    """
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        
    def __enter__(self):
        f = open(self.src, 'r')
        self.contents = f.read()
        f.close()
        return self
        
    def __exit__(self, type, value, traceback):
        f = open(self.dest, 'w')
        f.write(self.contents)
        f.close()

def env_vars():
    with open(ENV_VARS_PATH, 'r') as open_file:
        for line in open_file.readlines():
            if line.startswith('#') or line.strip() == '':
                continue
                        
            variable_name, variable_value, path = line.split(',')

            filepath = os.path.join(SOURCE_PATH, *path.split())
            backup_filepath = os.path.join(UNINSTALL_DIRECTORY, UNINSTALL_SEPARATOR.join(path.split()))
            
            yield filepath, backup_filepath, variable_name, variable_value

def install():
    paths_to_replacements = {}
    
    # Map file paths to a list of their changes
    for filepath, backup_filepath, variable_name, variable_value in env_vars():
        paths_to_replacements.setdefault(
            (filepath, backup_filepath),
            []
        ).append((
            variable_name.strip(),
            variable_value.strip()
        ))
    
    # A reinstall. Uses backup files for source content.
    if os.path.exists(UNINSTALL_DIRECTORY):
        # Open each file once and make the replacement
        print 'Configuring...'
        for filepath, backup_filepath in paths_to_replacements:
            print '\t%s' % filepath
        
            with edit_and_save(backup_filepath, filepath) as editor:            
                # Make changes to current file
                for variable_name, variable_value in paths_to_replacements[(filepath, backup_filepath)]:
                    editor.contents = editor.contents.replace(ENV_VARS_PADDING % variable_name, variable_value)
                    
    # Initial install
    else:
        os.mkdir(UNINSTALL_DIRECTORY)
    
        # Open each file once and make the replacement
        print 'Configuring...'
        for filepath, backup_filepath in paths_to_replacements:
            print '\t%s' % filepath
        
            with edit_and_save(filepath, filepath) as editor:
                # Copy file
                with open(backup_filepath, 'w') as backup_file:
                    backup_file.write(editor.contents)
            
                # Make changes to current file
                for variable_name, variable_value in paths_to_replacements[(filepath, backup_filepath)]:
                    editor.contents = editor.contents.replace(ENV_VARS_PADDING % variable_name, variable_value)

def uninstall():
    paths = {}

    for filepath, backup_filepath, variable_name, variable_value in env_vars():
        paths[filepath] = backup_filepath
    
    print 'Restoring...'
    for filepath, backup_filepath in paths.items():
        print '\t%s' % filepath
        # Restore/copy backup_filepath -> filepath
        with edit_and_save(backup_filepath, filepath) as editor:
            # Delete backup file
            os.remove(backup_filepath)
    
    # Remove uninstall directory
    os.rmdir(UNINSTALL_DIRECTORY)

ARGS = {
    'install': install,
    'uninstall': uninstall, 
}

def usage():
    print 'python setup.py', '{%s}' % '|'.join(ARGS.keys())
    exit(0)

def main():
    if len(sys.argv) != 2:
        usage()
    elif sys.argv[1] not in ARGS:
        usage()    
    
    ARGS[sys.argv[1]]()

if __name__ == '__main__':
    main()