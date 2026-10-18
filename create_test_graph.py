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
        CREATE (s:State {name: "Kerala"})
        CREATE (d:District {name: "Kannur"})
        CREATE (a:ArtForm {name: "Theyyam"})

        CREATE (d)-[:PART_OF]->(s)
        CREATE (a)-[:PRACTICED_IN]->(d)
    """)

print("Test knowledge graph created successfully!")

driver.close()