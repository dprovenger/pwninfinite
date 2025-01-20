import cmd

class PwnInfiniteShell(cmd.Cmd):
  intro = "\nWelcome to PwnInfinite - A Python-based framework for pentesting.\nType help or ? to list commands.\n "
  prompt = "PwnInfiniteShell> "

  # Commands
  def do_exit(self, arg):
      "\nExit PwnInfiniteShell.\nUsage: exit\n"
      print("\nExiting PwnInfiniteShell! ...\n")
      return True
  

  def do_help(self, arg):
      "\nShow available commands or help for a specific command.\nUsage: help <command>\n"
      super().do_help(arg)


  # Command to use a module
  def do_use(self, module):
      "\nSelect a module.\nUsage: use <module_name>\n"
      if module:
          print(f"\nModule '{module}' selected.\n")
      else:
          print("\nPlease specify a module to use.\n")


  def do_run(self, arg):
      "\nExecute the currently selected module.\nUsage: run\n"
      print("\nRunning the selected module ...\n")


if __name__ == "__main__":
    PwnInfiniteShell().cmdloop()