# -*- coding: utf-8 -*-

"""
A module containing the controller-related functionality
"""

import getpass
from cmd import Cmd
import os
import sys

class Controller(Cmd):
    """
    Controller for trove. It is derived from the
    Cmd class for line-oriented command interpreters:
    http://docs.python.org/2/library/cmd.html
    """

    def __init__(self, model, view):
        """
        The constructor from Cmd is extended:
        Model and View objects are added as entities to the controller.
        A welcome message is printed and the prompt gets set.
        """
        Cmd.__init__(self)
        self.view = view
        self.model = model
        self.view.print_info("This is trove " + self.model.version)
        self.view.print_info("Use Ctrl+D to exit, type 'help' or '?' for help.")
        self.view.print_info("")
        self.prompt = "(" + self.model.program + ") "
        return None

    def default(self, line):
        """
        Print an error message if syntax is unknown
        """
        self.view.print_error("Unknown syntax: %s"%line)
        self.view.print_info("")
        return None

    def do_clear(self, s):
        """
        Calls the Linux 'clear' command to clear the screen.
        """
        os.system("clear")
        return None

    # XXX: what is 's' and why isn't it used in this method?
    # XXX: why does this method return true?
    def do_EOF(self, s):
        """
        Ctrl+D is one way to exit the loop.
        """
        self.view.print_info("\n")
        return True

    # XXX: what does this method do??
    def emptyline(self):
        """
        Don't do anything
        """
        pass
        return None

    # XXX: what is 'arg' and why isn't it used in this method?
    def do_testcolors(self, arg):
        """
        Print the colour test output to the screen
        """
        self.view.print_colors()

    # XXX: what is 'string' and why isn't it used in this method?
    # XXX: why does this method return true?
    def do_exit(self, string):
        """
        Exit the application
        """
        self.view.print_info("")
        return True

    # XXX: what is 'arg' and why isn't it used in this method?
    def do_help(self, arg):
        """
        Prints a help text to help the user remember the commands available.
        This method is also called then typing '?'.
        """
        self.view.print_help()
        return None

    # XXX: what is 's' and why isn't it used in this method?
    # XXX: this is just a repeat of do_exit().  Why is it here?
    # XXX: why does this method return true?  What is this value used for?
    def do_quit(self, string):
        """
        Quit the application
        """
        self.view.print_info("")
        return True

    def do_search(self, arg):
        """
        Performs a search for 'arg' in all entry names. If more than one result
        is found, the selection is presented and the user can choose the entry
        to be displayed. By default the password itself is not shown, only the help
        text. However, the user can choose to see the password in a second step.
        """
        if not arg:
            self.view.print_usage('search')
            return None
        result_list = self.model.search(self.entry_dict, arg)
        result_num = len(result_list)
        if (result_num == 0):
            self.view.print_no_results()
            return None
        if (result_num == 1):
            self.view.print_info("")
            self.view.print_info("There is only one result for this search:")
            entry = result_list[0]
        else:
            self.view.print_overview(result_list)
            choice = raw_input("Select item:  (1-" + str(result_num) + ") ")
            success = self.model.check_choice('integer', choice, result_num)
            if success:
                entry = result_list[int(choice) - 1]
            else:
                self.view.print_no_valid_choice()
                return None
        if (entry.helptext != ""):
            self.view.print_details(entry)
            choice = raw_input("Show password? (y/N) ")
            yes = self.model.check_choice('boolean', choice)
            if yes:
                self.view.print_password(entry)
        else:
            self.view.print_bold("There is no help text for this entry.")
            self.view.print_details(entry, passwd = True)
        self.view.print_info("")
        return None

    def get_passphrase(self):
        """
        Opens the bcrypted file 'passwd.bfe' in the current directory.
        The decrypted content is filled into self.entry_dict. This is a
        dictionary with SHA1 hashes as keys and TroveEntry objects as values. 
        """
        #TODO: Do not hard code passwd file name and make location configurable.
        encryptedfile = './passwd.bfe'
        self.view.print_info("Using encrypted file:")
        self.view.print_info("    " + encryptedfile)
        if os.path.isfile(encryptedfile):
            masterpwd = getpass.getpass('Please enter master passphrase: ')
            self.entry_dict = self.model.get_entries(encryptedfile, masterpwd)
        else:
            self.view.print_error("File not found.")
            self.view.print_info("")
            sys.exit(1)
        return None

    def check_db_for_entries(self):
        """
        Prints an error message if it finds no entries in self.entry_dict.
        Otherwise it informs how many entries were found.
        """
        # TODO: This should be done differently. The success of the decryption
        # process should be directly available. It should not be necessary to
        # count the number of entries to guess this. Unfortunately the bcrypt
        # program gives the same return value in both cases, so it cannot be used
        # right now. Perhaps the switch to GPG will help. 
        if len(self.entry_dict.keys()) == 0:
            self.view.print_info("")
            self.view.print_error("No entries found after decryption.")
            self.view.print_error("Perhaps the passphrase was wrong?")
            self.view.print_info("")
            sys.exit(1)
        else:
            self.view.print_info("Found total number of "
                              + str(len(self.entry_dict.keys())) + " entries.")
            self.view.print_info("")
        return None

# vim: expandtab shiftwidth=4 softtabstop=4
