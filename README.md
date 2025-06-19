
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

## 📋 Collections Overview

The following collections are defined and validated:

* `planets`: with fields like `name`, `climate`, `terrain`, `population`, and `species_ids`.
* `species`: including `name`, `classification`, `average_lifespan`, and `language`.
* `factions`: storing `name`, `type`, and `leader_name`.
* `locations`: with references to planets and optional `coordinates`.
* `weapons`, `vehicles`, `characters`, `starships`: each with their respective fields and references.
* `movies`: embeds participants (characters and starships) in structured arrays.
* `historical_events`: references movies and embeds factions, locations, and characters involved.

## ✅ Schema Validations

All collections are protected using **strict JSON Schema validation**, which enforces required fields, BSON types, and relationships via `ObjectId` references. These validation files are located in the `schema/` folder and should be applied when creating collections in MongoDB.

## 🚀 How to Use

1. Start a MongoDB instance.
2. Create collections using the schema validation files from the `schema/` folder.
3. Insert documents or test data (optionally from the `data/` folder).
4. Run aggregation or mapReduce queries (examples can be added to `queries/`).

