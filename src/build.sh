#!/bin/bash

## Combines everything into a single executable file.  This is nice and easy.
## Should be run from the same directory as the Python files though...

zip tcc_database_manager.zip __main__.py log_stuff.py >/dev/null
echo "#"'!'"/usr/bin/env python" > shebang.txt
cat shebang.txt tcc_database_manager.zip > ../tcc_database_manager
rm shebang.txt
rm tcc_database_manager.zip
chmod +x ../tcc_database_manager

echo "Now put 'tcc_database_manager' wherever you want it to go for easy access."
