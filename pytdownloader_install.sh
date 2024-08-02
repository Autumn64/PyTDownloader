#! /bin/bash

# Copyright (c) 2023 Monica Nayely Flores Gomez (Autumn64).
# This software is free software; you can copy, modify and redistribute it under 
# the terms of the BSD-3-Clause license. More information at https://opensource.org/license/BSD-3-clause/

panic(){
	>&2 echo "An error ocurred during the installation. Exiting..."
	exit 1
}

install_dependencies(){
	if [ -x "$(command -v apt)" ]; then #Ubuntu, Debian, Linux Mint...
		sudo apt update && sudo apt install -y python3 python3-tk python3-venv git binutils
		return
	elif [ -x "$(command -v dnf)" ]; then #Fedora, Ultramarine...
		sudo dnf update -y && sudo dnf install -y python3 python3-tkinter git binutils
		return
	elif [ -x "$(command -v zypper)" ]; then #openSUSE
		sudo zypper refresh && sudo zypper --non-interactive install python3 python3-tk git binutils
		return
	elif [ -x "$(command -v pacman)" ]; then #Arch, Manjaro, Endeavour...
		sudo pacman -Sy && sudo pacman -S --noconfirm python tk git binutils
		return
	else
		echo "No supported package manager was found. Please install Python 3, Tkinter, Git and Binutils manually."
		read -p "Do you want to continue? (Y/n): " choice
		if [ "$choice" != "y" ] && [ "$option" != "Y" ]; then
			echo "Exiting..."
			exit 0
		fi
		return
	fi
}

echo ""
echo "PyTDownloader Installer"
echo ""
echo "Copyright (c) 2023 Monica Nayely Flores Gomez (Autumn64)."
echo "This software is free software; you can copy, modify and redistribute it under"
echo "the terms of the BSD-3-Clause license. More information at https://opensource.org/license/BSD-3-clause/"
echo ""
echo "What this script will do:"
echo "  1. Install some dependencies (specifically Python 3, Tkinter, Git and Binutils; you can remove them later)."
echo "  2. Clone the Codeberg PyTDownloader repository into a temporary folder in ~/.cache/."
echo "  3. Create a virtual environment inside the temporary folder, and install the rest of dependencies."
echo "  4. Compile PyTDownloader from source."
echo "  5. Move the newly compiled binaries into /opt/pytdownloader."
echo "  6. Create a .desktop file for PyTDownloader."
echo "  7. Create a symbolic link in /usr/bin/ to PyTDownloader."
echo "  8. Create a file named \"pytdownloader_uninstall.sh\" so you can remove PyTDownloader later if you wish."
echo "  9. Delete the temporary folder, as it's no longer necessary, in order to save disk space."
echo "WARNING: This script requires an internet connection."
echo ""
read -p "Install PyTDownloader? [Y/n]: " option

if [ "$option" != "y" ] && [ "$option" != "Y" ]; then
	echo "Operation cancelled by user."
	exit 0
fi

echo ""
echo "Installing PyTDownloader, please wait..."
sleep 3
install_dependencies
if [ $? -ne 0 ]; then
	panic
fi
sleep 3
echo ""

# Create folders and clone repository
rm -rf $HOME/.cache/build-pytdownloader
mkdir $HOME/.cache/build-pytdownloader
cd $HOME/.cache/build-pytdownloader
git clone https://codeberg.org/Autumn64/PyTDownloader.git
sleep 1

# Create venv, install dependencies and compile
cd PyTDownloader
python3 -m venv ./
source ./bin/activate
if [ $? -ne 0 ]; then
	panic
fi

python3 -m pip install customtkinter packaging pytube pyinstaller
pyver=$(ls ./lib/)
pyinstaller --noconfirm --onedir --windowed --icon "$HOME/.cache/build-pytdownloader/PyTDownloader/icon.ico" --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/audioDownload.py:." --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/configFrame.py:." --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/ffmpeg:." --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/languages.json:." --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/mainFrame.py:." --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/Settings.py:." --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/videoDownload.py:." --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/lib/$pyver/site-packages/customtkinter:customtkinter/" --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/logo.png:."  --add-data "$HOME/.cache/build-pytdownloader/PyTDownloader/icon.ico:." "$HOME/.cache/build-pytdownloader/PyTDownloader/pytdownloader.py"
if [ $? -ne 0 ]; then
	panic
fi

sleep 2

# Clean any previous installations, move compiled binaries, and create .desktop and symlink
sudo rm -rf /opt/pytdownloader
sudo rm -f /usr/bin/pytdownloader
sudo rm -f /usr/share/applications/PyTDownloader.desktop
sudo mv -f ./dist/pytdownloader /opt

sleep 1

echo ""
echo "Fractional scaling can cause issues with PyTDownloader." 
echo "The recommended value for fractional scaling settings is 2. If you do not use fractional scaling, set the scaling value as 1 or 1.5."
read -p "Scaling value: " sv

if ! [[ $sv =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "The entered scaling value isn't a valid number. Using the default value 1.5"
	sv=1.5
fi

[[ -d /usr/share/applications ]] || sudo mkdir /usr/share/applications # TIL /usr/share/applications sometimes doesn't exist.

echo "
[Desktop Entry]
Type=Application
Name=PyTDownloader
GenericName=YouTube downloader
Comment=A free, open-source, modern, simple and portable YouTube downloader.
Exec=/opt/pytdownloader/pytdownloader scale=$sv
Path=/opt/pytdownloader
Icon=/opt/pytdownloader/_internal/logo.png
Type=Application
Categories=Utility;Network;AudioVideo;
" | sudo tee /usr/share/applications/PyTDownloader.desktop
sudo ln -s /opt/pytdownloader/pytdownloader /usr/bin/pytdownloader

sleep 3
# Remove temporary folder
cd $HOME
rm -rf $HOME/.cache/build-pytdownloader

# Create uninstall file and make it executable
echo "
#! /bin/bash

# Copyright (c) 2023 Monica Nayely Flores Gomez (Autumn64).
# This software is free software; you can copy, modify and redistribute it under 
# the terms of the BSD-3-Clause license. More information at https://opensource.org/license/BSD-3-clause/

echo \"\"
echo \"PyTDownloader Uninstaller\"
echo \"\"
echo \"Copyright (c) 2023 Monica Nayely Flores Gomez (Autumn64).\"
echo \"This software is free software; you can copy, modify and redistribute it under\"
echo \"the terms of the BSD-3-Clause license. More information at https://opensource.org/license/BSD-3-clause/\"
echo \"\"
echo \"What this script will do:\"
echo \" 1. Remove the folder /opt/pytdownloader\"
echo \" 2. Remove the files /usr/share/applications/PyTDownloader.desktop and /usr/bin/pytdownloader\"
echo \"\"
read -p \"Uninstall PyTDownloader? [Y/n]: \" option

if [ \"\$option\" != \"y\" ] && [ \"\$option\" != \"Y\" ]; then
	echo \"Operation cancelled by user.\"
	exit 0
fi

echo \"\"
echo \"Uninstalling PyTDownloader, please wait...\"
sleep 3

sudo rm -rf /opt/pytdownloader
sudo rm -f /usr/share/applications/PyTDownloader.desktop
sudo rm -f /usr/bin/pytdownloader

echo \"Uninstalled successfully!\"
" | sudo tee /opt/pytdownloader/pytdownloader_uninstall.sh
sudo chmod 777 /opt/pytdownloader/pytdownloader_uninstall.sh

echo ""
echo ""
echo ""
echo ""
echo ""
echo "Finishing..."

sleep 3

echo "Installed successfully!"
echo "If you wish to uninstall PyTDownloader, please run /opt/pytdownloader/pytdownloader_uninstall.sh".