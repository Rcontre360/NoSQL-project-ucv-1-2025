
# NoSQL Star Wars Universe Database

This is a university project developed at **Universidad Central de Venezuela (UCV)** as part of the NoSQL coursework.
The goal of the project is to design and validate a rich, structured **MongoDB database** that models key entities and relationships in the *Star Wars* universe using JSON Schema validation.

## 📂 Project Structure

All variables, object fields on code/schemas must be in ENGLISH or SPANISH only, not a mix (said by Juan Pablo).

* `schema/`: Contains all the **MongoDB JSON Schema validation files**, one for each collection.
* `data/`: Optional folder where sample documents for initial inserts can be placed.
* `queries/`: You can include your MongoDB shell queries, aggregation pipelines, or mapReduce scripts here.

## 🛠 Technologies

* **MongoDB** (document-based NoSQL database)
* **JSON Schema validation** (for strict data structure enforcement)

## Data

We collected data from different sources. We used the following:

- [SWAPI](https://swapi.info/): A Star Wars API containing info about characters, planets, species, etc.
- [Kaggle Star Wars DB](https://www.kaggle.com/datasets/yixuanyeo/star-wars-dataset): A Kaggle dataset containing info about Star Wars.

First, our "fetch.py" script fetched the info from SWAPI, raw and without transformations. Then, we exported some tables from the Kaggle dataset; these tables were usually related to relationships we didn't have in the first API. All of this information was stored in the "raw" folder.

Next, our "start.py" script took all the raw info and parsed it into our schema. All of this new info is stored in the "clean" folder. Some data and relationships had to be created manually. Since our scripts rewrote every file in "clean," we put this data in the "manual" folder and imported it into our scripts.

The "convert" folder contains Python scripts to transform raw schemas into clean schemas.
