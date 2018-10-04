# Simulator of Consumer Centric Markets

The purpose of this app is to ...

# Improvements for future versions

The following points will/need to be developed:
- Market tab:
    - Improvement of graph plot
    - Interaction between graph plot and side menu
- Simulation tab:
    - Implementation of other simulation options
    - Plot of graph through simulation progress
    - Save results
    - Deployment on a High Power Computing (HPC) such as on Amazon Web Services or DTU's HPC (optional)
    - Report generation: 
        - Show relevant results
        - create PDF from these results (optional)

# Required packages

To use this web based app the following python packages are required:
- dash
- dash-renderer 
- dash-core-components 
- dash-html-components 
- plotly
- igraph
- cairocffi
- pandas
- numpy
- Gurobi

To install them go to python terminal and enter the command:
```sh
$ pip install dash dash-renderer dash-core-components dash-html-components plotly igraph cairocffi
```
(Note that you might need to launch the terminal in administrator mode to be able to install them.)

# To start the web based app

- Launch python terminal
- Go to the folder homing app's python files using
```sh
$ cd ~/P2PMarket_App
```
- Launch the app with the command
```sh
$ python P2PMarket_App.py
```
- Dash local server will answer with
```sh
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 984-449-674
 * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```
- You can now open any web browser and enter the given URL address, i.e. http://127.0.0.1:8050 in this example

