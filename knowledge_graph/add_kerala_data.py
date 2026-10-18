from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "IKSConnect123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

with driver.session(database="iks") as session:

    session.run("""
        MERGE (k:State {name: "Kerala"})

        MERGE (d:District {name: "Kannur"})
        SET d.state = "Kerala"

        MERGE (a:ArtForm {name: "Theyyam"})
        SET a.state = "Kerala"

        MERGE (d)-[:PART_OF]->(k)

        MERGE (a)-[:PRACTICED_IN {
            source: "kerala_economic_review_2024.pdf",
            page: 536
        }]->(d)
    """)

print("Kerala knowledge graph data added successfully!")

driver.close()