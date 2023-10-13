from typing import Optional, Tuple, List, Dict
import os
from pathlib import Path
from time import sleep
import typer

# need to figure out how to do this: fga init, and so on...

app = typer.Typer()

type("Name")


def _generate_project_directory(path: Optional[str] = None) -> Path:
    """Creates a directory where the template project files will be stored.
    By default it will create a folder named fga at the current directory.
    """
    path = path or os.getcwd()
    try:
        os.mkdir(Path(os.path.join(path, "fga")))
    except FileExistsError as e:
        pass

    return Path(os.path.join(path, "fga"))



def _populate_project_files(working_dir):
    """Pull the project files from the specified GitHub repository using Cookiecutter."""
    print("Pulling down project files...")

    cookiecutter('https://github.com/itsbigspark/fga_poc.git --checkout development, output_dir=working_dir')

    print("Project files downloaded successfully.")


def _generate_tfvars_file(
    project_initial_values: dict[str, str], working_dir: Path
) -> None:
    """Creates a terraform.tfvars file given the inputs from the user."""

    print("Creating the terraform.tfvars file!!")

    with open(f"{working_dir}/terraform.tfvars", "w") as f:
        for key, value in project_initial_values.items():
            f.write(f'{key} = "{value}"\n')


# TODO: Add validation to these inputs...
# callbacks function to the validations methods.


@app.command()
def init(
    cloud_platform: str = typer.Option(prompt="Which cloud platform are you using?"),
    region: str = typer.Option(prompt="Which region should we create the resources?"),
    cluster_name: str = typer.Option(prompt="What should we call the cluster?"),
    resource_prefix: str = typer.Option(
        default="fga", prompt="What resource prefix should we use?"
    ),
    project_directory: Optional[str] = typer.Option(
        default=os.getcwd(),
        prompt="Provide a path where project should be initialized?",
    ),
) -> None:
    """
    Initializes project directory

    :param cloud_platform:
    :param region:
    :param cluster_name:
    :param resource_prefix:
    :param project_directory:
    :return:
    """

    # Maybe we don't need this flag at the moment...
    print("Initializing project dependencies")
    if cloud_platform == "aws":
        project_initial_values: dict[str, str] = {
            "eks_cluster_name": cluster_name,
            "aws_region": region,
            "aws_resource_prefix": resource_prefix,
        }
    else:
        project_initial_values: dict[str, str] = {}

    # create project directory
    working_directory = _generate_project_directory(project_directory)

    # download files from git
    _populate_project_files(working_directory)

    # store tfvars in directory
    _generate_tfvars_file(project_initial_values, working_directory)


@app.command()
def validate() -> None:
    """Validating passed credentials

    Assumption is the following prerequisites will be
    - the region and info needed for the setting up the k8s cluster.
    - postgres connection details
    """
    print("Validating resources created....")


import subprocess
import os

def run_terraform_command(command: str, working_dir: str) -> None:
    try:
        subprocess.run(command, shell=True, check=True, cwd=working_dir)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


@app.command()
def apply() -> None:
    """Provision the resources..."""
    print("Provisioning the following resources...")
    terraform_command = "terraform apply"
    terraform_dir = "/Users/cliffordfrempong/Desktop/Personal/fga-poc/cli/terraform"
    run_terraform_command(terraform_command, terraform_dir)

@app.command()
def destroy() -> None:
    """Destroy all the resources created and delete the cluster"""
    print("Destroying all the resources...")
    run_terraform_command("terraform destroy")
    sleep(5)
    print("Done!!")



if __name__ == "__main__":
    app()
