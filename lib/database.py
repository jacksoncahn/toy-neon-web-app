import os
from datetime import datetime, timezone
from uuid import UUID

import psycopg
from psycopg.rows import dict_row


def _connect(*, row_factory=None):
    kwargs = {}
    if row_factory is not None:
        kwargs["row_factory"] = row_factory
    return psycopg.connect(os.environ["DATABASE_POOL_URL"], **kwargs)


def add_task(user_id: str, task: str, due: datetime) -> UUID:
    due_utc = due.astimezone(timezone.utc)
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO todos(user_id, task, due) VALUES(%s, %s, %s) RETURNING task_id",
                (user_id, task, due_utc),
            )
            return cur.fetchone()[0]


def edit_task(
    user_id: str,
    task_id: UUID,
    task: str,
    due: datetime,
    complete: bool,
) -> UUID | None:
    due_utc = due.astimezone(timezone.utc)
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE todos SET task = %s, due = %s, complete = %s "
                "WHERE task_id = %s AND user_id = %s RETURNING task_id",
                (task, due_utc, complete, task_id, user_id),
            )
            row = cur.fetchone()
            return row[0] if row else None


def remove_task(user_id: str, task_id: UUID) -> UUID | None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM todos WHERE task_id = %s AND user_id = %s RETURNING task_id",
                (task_id, user_id),
            )
            row = cur.fetchone()
            return row[0] if row else None


def fetch_todos(user_id: str) -> list[dict]:
    with _connect(row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT task_id, task, due, complete FROM todos WHERE user_id = %s",
                (user_id,),
            )
            return cur.fetchall()
