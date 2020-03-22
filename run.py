#! /usr/bin/env python3

from uuid import uuid4
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, SimpleStatement, ExecutionProfile, EXEC_PROFILE_DEFAULT

users = [
    ("Ivan", "Ivanov"),
    ("Petr", "Simonov"),
    ("Vasya", "Smirnov"),
    ("Fedor", "Sidorov"),
    ("Kolya", "Shpuck"),
    ("Denis", "Manalin"),
    ("Maria", "Yashina"),
    ("Alexey", "Konovalov"),
    ("Elena", "Bragina"),
    ("Oleg", "Denisov"),
    ("Stepan", "Parkan"),
]


def create_all(session, keyspace: str, profile: str):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % keyspace,
        execution_profile=profile)

    session.set_keyspace(keyspace)

    session.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID primary key,
            name varchar,
            surname varchar
        )
        """,
        execution_profile=profile)

    session.execute(f"CREATE INDEX IF NOT EXISTS users_surname_idx ON {keyspace}.users (surname)")


def load_data(session, profile: str):
    ttl = 24 * 60 * 60

    insert_query = session.prepare(f"INSERT INTO users (id, name, surname) VALUES (?, ?, ?) USING TTL {ttl}")
    # insert_query.consistency_level = ConsistencyLevel.LOCAL_QUORUM

    for name, surname in users:
        session.execute(
            insert_query,
            (uuid4(), name, surname),
            execution_profile=profile
        )


def select_surname(session, profile: str, surname: str):
    data = session.execute(
        "SELECT * FROM users WHERE surname=%s",
        (surname,)
    )
    for row in data:
        print(row)


if __name__ == '__main__':
    KEYSPACE = "test_users"
    profileName = 'localQuorum'

    myProfile = ExecutionProfile(consistency_level=ConsistencyLevel.LOCAL_QUORUM)
    cluster = Cluster(execution_profiles={profileName: myProfile})

    db_con = cluster.connect()
    create_all(db_con, KEYSPACE, profileName)

    db_con.set_keyspace(KEYSPACE)

    load_data(db_con, profileName)
    select_surname(db_con, profileName, "Smirnov")

    cluster.shutdown()
