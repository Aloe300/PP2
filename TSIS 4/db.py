import psycopg2
from config import load_config

def get_connection():
    config = load_config()
    return psycopg2.connect(**config)

def setup_database():
    sql = """
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()

    if row:
        player_id = row[0]
    else:
        cur.execute(
            "INSERT INTO players(username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id

def save_result(username, score, level_reached):
    player_id = get_or_create_player(username)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s)
        """,
        (player_id, score, level_reached)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_personal_best(username):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(MAX(gs.score), 0)
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            WHERE p.username = %s
            """,
            (username,)
        )
        best = cur.fetchone()[0]
        cur.close()
        conn.close()
        return best
    except Exception:
        return 0

def get_top_scores(limit=10):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.username, gs.score, gs.level_reached,
                   TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI')
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception:
        return []
