from cx_Freeze import setup, Executable


buildOptions = dict(
        include_files = ['images/icon.png','images/space-X.png']
        )
setup(name = "Launch App" ,
      version = "1.0" ,
      description = "Launch App" ,
      executables = [Executable("LaunchAPI.py", base = "Win32GUI")],
      options = dict(build_exe = buildOptions)
      )