import yaml
import os

print("Getting settings...")
currentDir = os.path.dirname(os.path.realpath(__file__))

with open(f"{currentDir}\\settings.yaml", "r+") as settings:
    data = yaml.safe_load(settings)

