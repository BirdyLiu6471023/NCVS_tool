# ncvs_tool

Package for accessing data of National Crime Victimization Survey. 

## Installation

```bash
$ pip install ncvs_tool
```

## License

`ncvs_tool` was created by Siqi Liu. It is licensed under the terms of the MIT license.


## Usage

- TODO

## Description

API Doc: https://bjs.ojp.gov/national-crime-victimization-survey-ncvs-api#zjwnq9

This is a new API of Bureau of Justice Statistics（BJS）just come out on June 23, 2022. The API provides full dataset of National Crime Victimization Survey (NCVS) from 1993 to 2021, collecting information on nonfatal personal crimes both reported and not reported to the police. The objective of this survey, according to BJD, is to "1) develop detailed information about the victims and consequences of crime; 2) estimate the number and types of crimes not reported to the police; 3) to provide uniform measures of selected types of crimes; and 4) to permit comparisons over time and types of areas."

Sodapy Socrata is the United State Government supported open data API, which simplifies the procedure of accessing to the all of government open data, but it does not customize for the data of BJS, and it is not simple for who only need the dataset and query data in a simple way through python.

The survey dataset includes basic demographic information such as age, race, gender and income, and also includes type of crime, location of crime, relationship between victim and offender, characteristics of the offender and whether the crime was reported to police, from 1993 to 2021. This dataset enables researchers do analysis related to crime and victim by various subpopulations.

Each row is a personal vicitmization, there are totally 63.5k rows and 37 columns. In the dataset, all of categorical data was enlabeled in the dataset (with a cookbook clarified name of each label).

## Credits

`ncvs_tool` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

NCVS BJS
