from datetime import time
from sqlite3.dbapi2 import Timestamp
# from models.entry import Entry
import sqlite3
import json
from models import Entry, Mood #Tag

def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.time,
            e.concepts,
            e.entry,
            e.mood_id,
            m.id mood_id,
            m.mood mood
        FROM JournalEntries e
        JOIN Moods m
            ON m.id = e.mood_id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset: 
            entry = Entry(row['id'], row['time'], row['concepts'], row['entry'], row['mood_id'])

            mood = Mood(row["mood_id"], row["mood"])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.time,
            e.concepts,
            e.entry,
            e.mood_id,
            m.id mood_id,
            m.mood mood
        FROM JournalEntries e
        JOIN Moods m
            ON m.id = e.mood_id
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['time'], data['concepts'], data['entry'], data['mood_id'])

        mood = Mood(data["mood_id"], data["mood"])

        entry.mood = mood.__dict__

    return json.dumps(entry.__dict__)

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO JournalEntries
            ( time, concepts, entry, mood_id)
        VALUES
            (?, ?, ?, ?);
        """,(new_entry['time'], new_entry['concepts'], new_entry['entry'], new_entry['mood_id']))

        id = db_cursor.lastrowid

        new_entry['id'] = id

    return json.dumps(new_entry)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM JournalEntries
        WHERE id = ?
        """, (id, ))


def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE JournalEntries
            SET
                time = ?,
                concepts = ?,
                entry = ?,
                mood_id = ?
        WHERE id = ?
        """,(new_entry['time'], new_entry['concepts'], new_entry['entry'], new_entry['mood_id'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def search_entry(search_terms):
        with sqlite3.connect("./dailyjournal.db") as conn:
        
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.time,
            e.concepts,
            e.entry,
            e.mood_id,
            m.id mood_id,
            m.mood mood
        FROM JournalEntries e
        JOIN Moods m
            ON m.id = e.mood_id
        WHERE e.concepts LIKE %?%
        """, (search_terms,))

        filtered_entries = []

        dataset = db_cursor.fetchall()

        for row in dataset: 
            entry = Entry(row['id'], row['time'], row['concepts'], row['entry'], row['mood_id'])

            mood = Mood(row["mood_id"], row["mood"])

            entry.mood = mood.__dict__

            filtered_entries.append(entry.__dict__)

        return json.dumps(filtered_entries)

