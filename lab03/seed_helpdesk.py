import time, random
from helpdesk_conn import get_redis
from models import *

r = get_redis()

def next_id(counter_key):
    return str(r.incr(counter_key))

def create_user(name,email,phone):
    uid = next_id(SEQ_USERS)
    r.hset(user_key(uid), mapping={
        "name":name, "email":email, "phone":phone, "joined_at":str(int(time.time()))
    })
    r.set(user_email_key(email), uid)
    return uid

def create_agent(name,email,skills):
    aid = next_id(SEQ_AGENTS)
    r.hset(agent_key(aid), mapping={"name":name,"email":email,"load":0})
    if skills:
        r.sadd(agent_skills(aid), *skills)
    return aid

def create_ticket(user_id, subject, priority, sla_due_secs=3600):
    tid = next_id(SEQ_TICKETS)
    r.hset(ticket_key(tid), mapping={
        "user_id":user_id,
        "subject":subject,
        "status":"open",
        "priority":priority,
        "created_at":str(int(time.time())),
        "assigned_agent":"",
        "sla_due_at":str(int(time.time())+sla_due_secs),
    })
    r.zadd(PRIORITY_Q, {as_member_ticket(tid): priority})
    r.sadd(ALL_TICKETS, tid)
    log(tid, f"created: subject='{subject}', priority={priority}")
    return tid

def log(tid, msg):
    ts = int(time.time())
    r.rpush(ticket_log(tid), f"{ts}: {msg}")

def assign_ticket(tid, aid):
    prev = r.hget(ticket_key(tid), "assigned_agent") or ""
    if prev:
        r.srem(agent_open(prev), as_member_ticket(tid))
        r.hincrby(agent_key(prev), "load", -1)
    r.hset(ticket_key(tid), mapping={"assigned_agent":aid})
    r.sadd(agent_open(aid), as_member_ticket(tid))
    r.hincrby(agent_key(aid), "load", 1)
    log(tid, f"assigned to agent:{aid}")

def update_status(tid, new_status):
    if new_status not in STATUSES:
        raise ValueError("invalid status")
    r.hset(ticket_key(tid), mapping={"status":new_status})
    log(tid, f"status -> {new_status}")

def extend_sla(tid, extra_secs):
    new_due = int(r.hget(ticket_key(tid),"sla_due_at")) + int(extra_secs)
    r.hset(ticket_key(tid), mapping={"sla_due_at": str(new_due)})
    log(tid, f"sla_due_at extended by {extra_secs}s")

def close_ticket(tid):
    update_status(tid, "closed")
    r.zrem(PRIORITY_Q, as_member_ticket(tid))
    aid = r.hget(ticket_key(tid), "assigned_agent")
    if aid:
        r.srem(agent_open(aid), as_member_ticket(tid))
        r.hincrby(agent_key(aid), "load", -1)
    log(tid, "closed")

def seed():
    users = [
        ("Aisha Khan","aisha@example.com","+92-300-1111111"),
        ("Bilal Ahmed","bilal@example.com","+92-300-2222222"),
        ("Sana Malik","sana@example.com","+92-300-3333333"),
        ("Danish Ali","danish@example.com","+92-300-4444444"),
        ("Hira Shah","hira@example.com","+92-300-5555555"),
    ]
    user_ids = [create_user(*u) for u in users]

    agents = [
        ("Agent Amna","amna@helpdesk.local",["returns","billing"]),
        ("Agent Umar","umar@helpdesk.local",["technical","warranty"]),
        ("Agent Zara","zara@helpdesk.local",["returns","shipping"]),
    ]
    agent_ids = [create_agent(*a) for a in agents]

    subjects = [
        "Order #1234 not delivered",
        "Refund request for damaged item",
        "Website login issue",
        "Change delivery address",
        "Warranty claim - headphone",
        "App shows wrong order history",
        "Return pickup reschedule",
        "Technical error during payment",
    ]
    priorities = [1,5,10,20,5,10,20,1]
    ticket_ids = []
    for subj, pr in zip(subjects, priorities):
        uid = random.choice(user_ids)
        tid = create_ticket(uid, subj, pr, sla_due_secs=random.choice([3600,7200,10800]))
        ticket_ids.append(tid)

    for tid in ticket_ids[:3]:
        assign_ticket(tid, random.choice(agent_ids))

    for tid in ticket_ids:
        log(tid, "user contacted support")
        log(tid, "agent responded")

    print("Seed complete.")
    print("Users:", user_ids)
    print("Agents:", agent_ids)
    print("Tickets:", ticket_ids)

if __name__ == "__main__":
    seed()
