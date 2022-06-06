"""
Create a graph database representation of 5 letter words

Hypothesis: graph representation can improve wordle hack algorithm
"""
from words_5_graphdb.neo4j_conn import Neo4jConnection

def main():

    conn = Neo4jConnection(uri="neo4j://localhost:7687", user="neo4j", pwd="neo4j")

    print("clear db")

    clear_db = 'MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r'

    conn.query(clear_db, db='neo4j')

    clear_db = 'match (a) delete a'

    conn.query(clear_db, db='neo4j')

    print("load words")

    load_words = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM
    'file:///words_5.csv'
    AS line FIELDTERMINATOR ','
    CREATE (:Word {word: line.word})
    """

    conn.query(load_words, db='neo4j')

    print("load alphabet")

    load_alphabet = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM
    'file:///alphabet.csv'
    AS line FIELDTERMINATOR ','
    CREATE (:Alphabet {alphabet: line.alphabet})
    """

    conn.query(load_alphabet, db='neo4j')


    print("load has relationship")

    load_has_relationship = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM
    'file:///words_5_graph.csv'
    AS line FIELDTERMINATOR ','
    MATCH (word:Word {word: line.word}),(alphabet:Alphabet {alphabet: line.alphabet})
    CREATE (word)-[h:HAS]->(alphabet)
    SET h.relationship = line.position
    """

    conn.query(load_has_relationship, db='neo4j')


if __name__ == "__main__":
    main()

    
# print("load belong relationship")

# load_belong_relationship = """
# USING PERIODIC COMMIT 500
# LOAD CSV WITH HEADERS FROM
# 'file:///words_5_graph.csv'
# AS line FIELDTERMINATOR ','
# MATCH (word:Word {word: line.word}),(alphabet:Alphabet {alphabet: line.alphabet})
# CREATE (alphabet)-[b:Belong]->(word)
# SET b.relationship = line.position
# """

# conn.query(load_belong_relationship, db='neo4j')

print("Done")