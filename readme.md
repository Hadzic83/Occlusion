# Occlusion
Copyright &copy; 2025 [Orobas](https://www.orobas.com.au)

## Instructions

Use the appropriate instructions below to install the required build tools.

```
Linux:
sudo apt-get install build-essential

macOS:
xcode-select --install

Windows:
https://visualstudio.microsoft.com
Install Visual Studio with "Desktop development with C++"
```

Once the build tools are available, create a virtual environment and install the necessary Python libraries.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The application should then be ready to run. Note that it will download the AI model for offline use the first time you run it.

```
python occlusion.py
```
