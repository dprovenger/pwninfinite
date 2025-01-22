import os
import cmd
import importlib.util

class PwnInfiniteShell(cmd.Cmd):
    intro = "\nWelcome to PwnInfinite - A Python-based framework for pentesting.\nType help or ? to list commands.\n "
    prompt = "PwnInfiniteShell> "

    def __init__(self, modules_dir="modules"):
        super().__init__()
        self.modules_dir = modules_dir
        self.modules = self.load_modules()

    def load_modules(self):
        """Load available modules in the modules directory."""
        if not os.path.exists(self.modules_dir):
            print(f"\nError: Modules directory '{self.modules_dir}' does not exist.\n")
            return []
      
        return [f[:-3] for f in os.listdir(self.modules_dir) if f.endswith(".py")]
  
    def do_list(self, arg):
        """\nList available modules.\nUsage: list\n"""
        if not self.modules:
            print("\nNo modules found under that module name.\n")
        else:
            print("\nAvailable modules to run:\n")
            for module in self.modules:
                print(f" - {module}\n")

    def do_run(self, module_name):
        """\nRun a module by name.\nUsage: run <module_name>\n"""
        if module_name not in self.modules:
            print(f"\nError: Module '{module_name}' not found.\n")
            return
      
        module_path = os.path.join(self.modules_dir, f"{module_name}.py")
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "main") and callable(module.main):
            print(f"\nRunning {module_name}...\n")
            module.main()
        else:
            print(f"Error:Module '{module_name}' does not have a callable 'main()' function.")

  
    def do_help(self, arg):
        "\nShow available commands or help for a specific command.\nUsage: help\nUsage: help <command>\n"
        super().do_help(arg)

  # Commands
    def do_exit(self, arg):
        """\nExit PwnInfiniteShell.\nUsage: exit\n"""
        print("\nExiting PwnInfiniteShell! ...\n")
        return True

if __name__ == "__main__":
  PwnInfiniteShell().cmdloop()