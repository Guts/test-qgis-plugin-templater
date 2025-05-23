# How to generate

> Commands on Ubuntu 22.04. Adapt to your system.

Requirements:

- Git
- Cookiecutter (preferally installed with pipx)
- Python >= 3.9
- rsync

Environment setup:

```sh
git clone git@github.com:Guts/test-qgis-plugin-templater.git ~/Git/Perso/qgis-plugin-templater-github
cd ~/Git/Perso/qgis-plugin-templater-github
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip setuptools wheel
```

Run templater:

```sh
cookiecutter --no-input --overwrite-if-exists https://gitlab.com/Oslandia/qgis/template-qgis-plugin plugin_name=qgis_plugin_templater_test_github plugin_processing=true plugin_description_short='Autogenerated QGIS plugin boilerplate using GitHub CI' qgis_version_min='3.40' ci_cd_tool=GitHub repository_default_branch=main repository_url_base=https://github.com/Guts/test-qgis-plugin-templater author_name='Julien M.' author_email='julien.moura@oslandia.com' publish_official_repository=false --output-dir /tmp/ && rsync --force --recursive /tmp/plugin_qgis_plugin_templater_test_github/ ~/Git/Perso/qgis-plugin-templater-github
```

Or from the local templater repository (i.e. to test against a branch):

```sh
cookiecutter --no-input --overwrite-if-exists ~/Git/Oslandia/QGIS/template-qgis-plugin/ plugin_name=qgis_plugin_templater_test_github plugin_processing=true plugin_description_short='Autogenerated QGIS plugin boilerplate using GitHub CI' qgis_version_min='3.40' ci_cd_tool=GitHub repository_default_branch=main repository_url_base=https://github.com/Guts/test-qgis-plugin-templater author_name='Julien M.' author_email='julien.moura@oslandia.com' publish_official_repository=false --output-dir /tmp/ && rsync --force --recursive /tmp/plugin_qgis_plugin_templater_test_github/ ~/Git/Perso/qgis-plugin-templater-github
```

> Note: The `--no-input` option is used to skip interactive prompts. If you want to customize the generated project, you can remove this option and provide the necessary inputs interactively.

Post actions:

```sh
python -m pip install -U --upgrade-strategy=eager -r requirements/development.txt
pre-commit install
git add .
pre-commit run -a
```

Push:

```sh
git add .
git commit -m "Testing QGIS plugin boilerplate from QGIS Plugin Templater (Oslandia). `date +'%Y-%m-%d %H:%M:%S'`"
git push -f -u origin main
```
