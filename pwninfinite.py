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
      "Show available commands or help for a specific command.\n"
      super().do_help(arg)


  # Command to use a module
  def do_use(self, module):
      "Select a module. Usage: use <module_name>.\n"
      if module:
          print(f"Module '{module}' selected.")
      else:
          print("Please specify a module to use.")


  def do_run(self, arg):
      "Execute the currently selected module.\n"
      print("Running the selected module ...")


if __name__ == "__main__":
    PwnInfiniteShell().cmdloop()