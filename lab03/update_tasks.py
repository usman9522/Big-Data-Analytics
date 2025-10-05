from helpdesk_conn import get_redis
from models import *

r = get_redis()

def reassign_ticket(tid, new_aid):
    prev = r.hget(ticket_key(tid), "assigned_agent") or ""
    if prev:
        r.srem(agent_open(prev), as_member_ticket(tid))
        r.hincrby(agent_key(prev), "load", -1)
    r.hset(ticket_key(tid), mapping={"assigned_agent": new_aid})
    r.sadd(agent_open(new_aid), as_member_ticket(tid))
    r.hincrby(agent_key(new_aid), "load", 1)
    r.rpush(ticket_log(tid), "reassigned to agent:" + new_aid)

def fix_subject(tid, new_subject):
    r.hset(ticket_key(tid), mapping={"subject": new_subject})
    r.rpush(ticket_log(tid), "subject fixed")

if __name__ == "__main__":
    r.hset(ticket_key("1"), mapping={"status": "in_progress"})
    r.rpush(ticket_log("1"), "status -> in_progress")

    r.hset(ticket_key("1"), mapping={"status": "on_hold"})
    r.rpush(ticket_log("1"), "status -> on_hold")

    reassign_ticket("2", "2")

    new_due = int(r.hget(ticket_key("1"), "sla_due_at")) + 3600
    r.hset(ticket_key("1"), mapping={"sla_due_at": str(new_due)})
    r.rpush(ticket_log("1"), "sla_due_at extended by 3600s")

    fix_subject("2", "Refund request for damaged item (verified)")

    print("Update tasks done.")
