from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "IKSConnect123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

with driver.session(database="iks") as session:
    result = session.run("RETURN 'Neo4j connection successful!' AS message")

    for record in result:
        print(record["message"])

driver.close()