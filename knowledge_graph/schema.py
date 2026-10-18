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
        CREATE CONSTRAINT state_name IF NOT EXISTS
        FOR (n:State)
        REQUIRE n.name IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT district_name IF NOT EXISTS
        FOR (n:District)
        REQUIRE n.name IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT heritage_name IF NOT EXISTS
        FOR (n:HeritageSite)
        REQUIRE n.name IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT artform_name IF NOT EXISTS
        FOR (n:ArtForm)
        REQUIRE n.name IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT festival_name IF NOT EXISTS
        FOR (n:Festival)
        REQUIRE n.name IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT traditional_name IF NOT EXISTS
        FOR (n:TraditionalKnowledge)
        REQUIRE n.name IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT person_name IF NOT EXISTS
        FOR (n:Person)
        REQUIRE n.name IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT literary_name IF NOT EXISTS
        FOR (n:LiteraryWork)
        REQUIRE n.name IS UNIQUE
    """)

print("Knowledge Graph schema created successfully!")

driver.close()