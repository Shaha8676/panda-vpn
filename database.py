import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict

DB_PATH = "uzvpn.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY,
            username    TEXT DEFAULT '',
            full_name   TEXT DEFAULT '',
            lang        TEXT DEFAULT 'uz',
            ref_code    TEXT UNIQUE,
            referred_by INTEGER,
            created_at  TEXT DEFAULT (datetime('now')),
            is_banned   INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS subscriptions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            plan_months INTEGER NOT NULL,
            price_rub   INTEGER NOT NULL,
            started_at  TEXT DEFAULT (datetime('now')),
            expires_at  TEXT NOT NULL,
            is_active   INTEGER DEFAULT 1,
            wg_config   TEXT DEFAULT '',
            server      TEXT DEFAULT 'RU-1',
            devices     INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id        INTEGER NOT NULL,
            plan_id        TEXT NOT NULL,
            amount_rub     INTEGER NOT NULL,
            payment_method TEXT DEFAULT 'stars',
            status         TEXT DEFAULT 'pending',
            telegram_payload TEXT DEFAULT '',
            created_at     TEXT DEFAULT (datetime('now')),
            paid_at        TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS bonus_days (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            days       INTEGER NOT NULL,
            reason     TEXT DEFAULT 'referral',
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str, full_name: str, ref_code: str = None) -> bool:
    conn = get_conn()
    try:
        import hashlib, time
        my_ref = hashlib.md5(f"{user_id}{time.time()}".encode()).hexdigest()[:8]
        referred_by = None
        if ref_code:
            row = conn.execute(
                "SELECT id FROM users WHERE ref_code = ?", (ref_code,)
            ).fetchone()
            if row:
                referred_by = row["id"]

        conn.execute("""
            INSERT OR IGNORE INTO users
            (id, username, full_name, ref_code, referred_by)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, full_name, my_ref, referred_by))
        affected = conn.total_changes
        conn.commit()
        return affected > 0
    finally:
        conn.close()

def get_user_lang(user_id: int) -> Optional[str]:
    conn = get_conn()
    row = conn.execute("SELECT lang FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row["lang"] if row else None

def set_user_lang(user_id: int, lang: str):
    conn = get_conn()
    conn.execute("UPDATE users SET lang = ? WHERE id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def get_user_by_ref(ref_code: str) -> Optional[int]:
    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM users WHERE ref_code = ?", (ref_code,)
    ).fetchone()
    conn.close()
    return row["id"] if row else None

def get_referral_count(user_id: int) -> int:
    conn = get_conn()
    row = conn.execute(
        "SELECT COUNT(*) as cnt FROM users WHERE referred_by = ?", (user_id,)
    ).fetchone()
    conn.close()
    return row["cnt"] if row else 0

def add_bonus_days(user_id: int, days: int, reason: str = "referral"):
    conn = get_conn()
    conn.execute(
        "INSERT INTO bonus_days (user_id, days, reason) VALUES (?, ?, ?)",
        (user_id, days, reason)
    )
    conn.execute("""
        UPDATE subscriptions
        SET expires_at = datetime(expires_at, ? || ' days')
        WHERE user_id = ? AND is_active = 1
    """, (str(days), user_id))
    conn.commit()
    conn.close()

def get_active_subscription(user_id: int) -> Optional[Dict]:
    conn = get_conn()
    row = conn.execute("""
        SELECT *,
            CAST((julianday(expires_at) - julianday('now')) AS INTEGER) as days_left,
            0 as traffic_gb
        FROM subscriptions
        WHERE user_id = ? AND is_active = 1
          AND expires_at > datetime('now')
        ORDER BY expires_at DESC LIMIT 1
    """, (user_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def create_subscription(user_id: int, plan_months: int, price: int, days: int) -> int:
    conn = get_conn()
    expires = datetime.now() + timedelta(days=days)
    cursor = conn.execute("""
        INSERT INTO subscriptions (user_id, plan_months, price_rub, expires_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, plan_months, price, expires.strftime("%Y-%m-%d %H:%M:%S")))
    sub_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return sub_id

def create_payment(user_id: int, plan_id: str, amount: int) -> int:
    conn = get_conn()
    cursor = conn.execute("""
        INSERT INTO payments (user_id, plan_id, amount_rub)
        VALUES (?, ?, ?)
    """, (user_id, plan_id, amount))
    pay_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pay_id

def confirm_payment(payment_id: int):
    conn = get_conn()
    conn.execute("""
        UPDATE payments SET status = 'paid', paid_at = datetime('now')
        WHERE id = ?
    """, (payment_id,))
    conn.commit()
    conn.close()

def get_all_users() -> list:
    conn = get_conn()
    rows = conn.execute("SELECT id FROM users WHERE is_banned = 0").fetchall()
    conn.close()
    return [r["id"] for r in rows]

# Ishga tushganda DB yaratish
init_db()
