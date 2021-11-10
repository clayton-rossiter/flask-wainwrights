# Lake District Wainwright Fells API
            

## Table of Contents
1. [Installation](#installation)
2. [Running](#running)
3. [Schema](#schema)
4. [Endpoints](#endpoints)
5. [Testing](#testing)

## 1. Installation
Once you've cloned this git repo, simply install from the requirements.txt file:
```bash
pip install requirements.txt
```

## 2. Running
The API is launched from the ```main.py``` file.  The API can be launched by running the code snippet below from the main directory:
```bash
python main.py
```

By default, this will run on localhost port 5000, or URL ```http://localhost:5000/```

## 3. Schema
The data is presented as a list with the following 8 headings (case sensitive):     
- Name
- Height Rank
- Height (m)
- Height(ft)
- Prom. (ft)
- OS Grid Reference
- Longitude, 
- Latitude


## 4. Endpoints

Using the ```flask-restful``` API library, each of the 214 Wainwright fells can be reported from either of the two links:

### 4.1 BASE_URL/fell/
The first of the links only returns a single element of the fells and is sorted by Height Rank, e.g. the highest fell to the lowest.  These can be recalled using their ID:int between 0 and 213.  For example, running a ```GET``` request to ```BASE_URL/fell/0``` will be return Scafell Pike (being the tallest).  Example result schema is below:
```json
{
    "Name": "Scafell Pike",
    "Height Rank": 1,
    "Height (m)": 978,
    "Height (ft)": 3209,
    "Prom. (ft)": 2992,
    "OS Grid Reference": "NY215072",
    "Longitude": -3.2124289085,
    "Latitude": 54.4541010651,
    "Nearest": 15.8696659566
}
```

### 4.2 BASE_URL/fells/
The ```fells``` endpoint includes further capability, including returning multiple fells from name, height (in metres) and/or location.  

#### 3.2.1 By Name
The API accepts a singular name or multiple names (not case sensitive) and will also return partial name matches.  For example, searching 'scafell' will return 'Scafell Pike' and 'Scafell'.  An example URL for multiple names is as follows:
```html
http://127.0.0.1:5000/fells/?name=scafell&name=skiddaw
```

#### 3.2.2 By Height (In Metres)
It is also possible to search by height, such that the API will return all fells above or below a specified height.  An example URL for searching for all fells between 400m and 600m is as follows:
```html
http://127.0.0.1:5000/fells/?above=400&below=600
```

#### 3.2.3 By Location
There are two ways to search by location:
1. OS Grid Reference (gridref)
or
2. Longitude (longitude) AND latitude (latitude)    

The API will accept, by default, the grid reference.  If this is not provided, it will accept a supplied longitude AND latitude.  It will not accept a singular value of longitude or latitude.  See below for some example URLs:

Grid Reference:
```html
http://127.0.0.1:5000/fells/?gridref=NY342151
````

Longitude & Latitude:
```html
http://127.0.0.1:5000/fells/?longitude=-3.0182873723&latitude=54.5268929636
```

The results are returned in ascending distance from the supplied location reference, ie. the lower the index, the closer the fell is to the supplied location.  
The headers for the returned json also includes a 'Nearest' header.  An example schema is below:
```json
 {
    "Name": "Helvellyn",
    "Height Rank": 3,
    "Height (m)": 950,
    "Height (ft)": 3117,
    "Prom. (ft)": 2336,
    "OS Grid Reference": "NY342151",
    "Longitude": -3.0182873723,
    "Latitude": 54.5268929636,
    "Nearest": 5.3e-09
}
```

It is worth noting the extra "Nearest" heading here that dictates the distance in kilometres from the location specified.

## 5. Testing
All the tests are contained with the "tests" folder and are primarily based off the ```framework.py``` file to ensure consistency across the tests.  To run the tests, run the command below:
```bash
python -m unittest discover
```
And to get the coverage report on the tests, run the following:
```bash
coverage run -m unittest discover
coverage report
```
For more information on Python's unittest, follow the link [here](https://kapeli.com/cheat_sheets/Python_unittest_Assertions.docset/Contents/Resources/Documents/index), where this website contains an awesome cheat sheat to get started with unittesting, though [this website](https://edu.anarcho-copy.org/Programming%20Languages/Python/Python%20CheatSheet/beginners_python_cheat_sheet_pcc_testing.pdf) is also handy.