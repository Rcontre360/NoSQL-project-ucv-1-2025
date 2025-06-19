
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

