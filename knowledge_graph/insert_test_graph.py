
from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "IKSConnect123"

SOURCE = "14th Five Year Plan 22-27 English.txt"
PAGE = 249

# Only the five relationships validated for our test.
facts = [
    {
        "place": "Raja Ravi Varma Art Gallery",
        "district": "Thiruvananthapuram"
    },
    {
        "place": "Pazhassi Raja Museum",
        "district": "Kozhikode"
    },
    {
        "place": "Sakthan Thampuran Palace Museum",
        "district": "Thrissur"
    },
    {
        "place": "Napier Museum",
        "district": "Thiruvananthapuram"
    },
    {
        "place": "Calicut City Museum",
        "district": "Kozhikode"
    }
]

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    with driver.session(database="iks") as session:

        for fact in facts:
            session.run("""
                MERGE (place:HeritageSite {name: $place})
                MERGE (district:District {name: $district})

                MERGE (place)-[r:LOCATED_IN]->(district)
                SET r.source = $source,
                    r.page = $page
            """,
                place=fact["place"],
                district=fact["district"],
                source=SOURCE,
                page=PAGE
            )

        print("Test graph insertion completed.")

        result = session.run("""
            MATCH (place:HeritageSite)-[r:LOCATED_IN]->(district:District)
            WHERE r.source = $source AND r.page = $page
            RETURN place.name AS place,
                   district.name AS district,
                   r.source AS source,
                   r.page AS page
            ORDER BY place
        """, source=SOURCE, page=PAGE)

        print("\nVerified test relationships:")
        for record in result:
            print(
                record["place"],
                "-- LOCATED_IN -->",
                record["district"],
                "| Source:", record["source"],
                "| Page:", record["page"]
            )

finally:
    driver.close()
