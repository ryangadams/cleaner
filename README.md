# Node Modules Cleaner

Cleans up node_modules directories to reduce used disk space

Usage:

    python -m cleaner PATH


You can also install this using pipx

    pipx install git+https://github.com/ryangadams/cleaner.git

and run the command like

    cleaner PATH

Searches path for node_modules directories under `PATH` and prompts you to delete them 
(assuming) you have a package.json and associated lock file to re-install.

