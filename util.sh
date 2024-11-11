#!/bin/bash

clear

echo "                                         "
echo "                                         "
echo "            _    _  _          _         "
echo "     _   _ | |_ (_)| |    ___ | |__      "
echo "    | | | || __|| || |   / __|| '_ \     "
echo "    | |_| || |_ | || | _ \__ \| | | |    "
echo "     \__,_| \__||_||_|(_)|___/|_| |_|    "
echo "                                         "
echo "U t i l i t i e s  f o r  e v e r y o n e"
echo "                                         "
echo "                      Welcome to util.sh!"
echo "                         Github: @dev-kas"
echo "                                         "

# Function to handle the process
startProcess() {
    case $answer in
    1)
        echo "Running..."
        python main.py
        ;;
    2)
        echo "Building..."
        pyinstaller --onefile --windowed main.py
        ;;
    3)
        echo "Installing..."
        pip install -r requirements.txt
        ;;
    *)
        echo "Invalid option - exiting."
        exit 1
        ;;
    esac
}

# Function to prompt for options if no argument is passed
optionPicker() {
    echo "    Select an option...                  "
    echo "[1] Run                         [2] Build"
    echo "[3] Install                              "

    read -p "(1/2/3): " answer
    startProcess
}

# Main logic to handle the command-line argument
case $1 in
    run)
        answer=1
        startProcess
        ;;
    build)
        answer=2
        startProcess
        ;;
    install)
        answer=3
        startProcess
        ;;
    *)
        optionPicker
        ;;
esac
